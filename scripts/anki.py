# -*- coding: utf-8 -*-
"""Fala com o Anki (complemento AnkiConnect) para criar cards de frase inteira com audio e ler o que voce revisou.

Sempre em Python (acento vira lixo em varios terminais do Windows). O Anki precisa estar ABERTO.

Comandos:
  python scripts/anki.py decks                              lista os decks (so leitura)
  python scripts/anki.py sobe estudo/lotes/cafe.json --dry-run   mostra o que seria criado, sem criar nada
  python scripts/anki.py sobe estudo/lotes/cafe.json        cria os cards (output + input) com audio
  python scripts/anki.py sobe estudo/lotes/cafe.json --eixo output     so o deck de FALAR
  python scripts/anki.py revisadas --dias 7 [--deck "Espanhol Output"]  frases que voce revisou nos ultimos dias (JSON)

Formato do lote (veja estudo/lotes/exemplo.json):
  {"idioma": "es", "deck_base": "Espanhol", "tag": "cafe",
   "cards": [{"id": "001", "alvo": "Quiero un café, por favor.", "pt": "Quero um café, por favor.", "nota": "opcional"}]}

Os dois eixos (decks criados a partir de deck_base):
  "<deck_base> Output": frente = portugues, verso = frase no idioma + audio   (treina FALAR, lembrar de cabeca)
  "<deck_base> Input" : frente = frase no idioma + audio, verso = portugues   (treina ENTENDER ouvindo)
"""
import argparse
import asyncio
import base64
import hashlib
import json
import re
import sys
import tempfile
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

URL = "http://127.0.0.1:8765"
MODELO = "Estudo IA"
VOZ = {"es": "es-MX-DaliaNeural", "en": "en-US-JennyNeural", "fr": "fr-FR-DeniseNeural",
       "it": "it-IT-ElsaNeural", "de": "de-DE-KatjaNeural", "pt": "pt-BR-FranciscaNeural"}


def anki(acao, **params):
    corpo = json.dumps({"action": acao, "version": 6, "params": params}).encode("utf-8")
    try:
        resp = json.load(urllib.request.urlopen(urllib.request.Request(URL, data=corpo), timeout=30))
    except Exception as e:
        sys.exit(f"Nao consegui falar com o Anki ({e}).\nAbra o Anki e rode: python scripts/checar.py")
    if resp.get("error"):
        raise RuntimeError(resp["error"])
    return resp["result"]


def garantir_modelo():
    if MODELO in anki("modelNames"):
        return
    anki(
        "createModel",
        modelName=MODELO,
        inOrderFields=["Frente", "Verso"],
        css=".card{font-family:Arial;font-size:22px;text-align:center}",
        cardTemplates=[{"Name": "Cartao 1", "Front": "{{Frente}}",
                        "Back": "{{FrontSide}}<hr id=answer>{{Verso}}"}],
    )
    print(f"Tipo de nota '{MODELO}' criado no Anki (campos Frente e Verso).")


def gerar_audio(texto, idioma):
    """Devolve o nome do arquivo no Anki. Um mp3 por frase, reaproveitado pelos dois cards."""
    import edge_tts

    nome = f"ia-{idioma}-{hashlib.sha1(texto.encode('utf-8')).hexdigest()[:10]}.mp3"
    if nome in anki("getMediaFilesNames", pattern=nome):
        return nome
    with tempfile.TemporaryDirectory() as d:
        destino = Path(d) / nome
        asyncio.run(edge_tts.Communicate(texto, VOZ.get(idioma, VOZ["es"]), rate="-5%").save(str(destino)))
        anki("storeMediaFile", filename=nome, data=base64.b64encode(destino.read_bytes()).decode())
    return nome


def limpar(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>|\[sound:[^\]]+\]", " ", html)).strip()


def cmd_decks(_):
    for nome in sorted(anki("deckNames")):
        print(nome)


def cmd_sobe(args):
    lote = json.loads(Path(args.lote).read_text(encoding="utf-8"))
    idioma, base, tag = lote.get("idioma", "es"), lote["deck_base"], lote.get("tag", "lote")
    eixos = ["output", "input"] if args.eixo == "ambos" else [args.eixo]
    deck = {"output": f"{base} Output", "input": f"{base} Input"}

    if args.dry_run:
        for c in lote["cards"]:
            print(f"{c['id']}: {c['pt']}  <->  {c['alvo']}")
        print(f"\n{len(lote['cards'])} frase(s) -> decks {[deck[e] for e in eixos]} (nada foi criado: --dry-run)")
        return

    garantir_modelo()
    for e in eixos:
        anki("createDeck", deck=deck[e])
    criados = ja_existiam = 0
    for c in lote["cards"]:
        som = f"[sound:{gerar_audio(c['alvo'], idioma)}]"
        nota = f"<br><small>{c['nota']}</small>" if c.get("nota") else ""
        campos = {
            "output": {"Frente": c["pt"], "Verso": f"{c['alvo']} {som}{nota}"},
            "input": {"Frente": f"{c['alvo']} {som}", "Verso": f"{c['pt']}{nota}"},
        }
        for e in eixos:
            try:
                nid = anki("addNote", note={
                    "deckName": deck[e], "modelName": MODELO, "fields": campos[e],
                    "options": {"allowDuplicate": False}, "tags": [f"{base.lower()}::{tag}", e],
                })
            except RuntimeError as erro:
                if "duplicate" in str(erro).lower():
                    ja_existiam += 1
                    continue
                raise
            # o addNote as vezes ignora o deck: confere e corrige
            for card in anki("cardsInfo", cards=anki("findCards", query=f"nid:{nid}")):
                if card["deckName"] != deck[e]:
                    anki("changeDeck", cards=[card["cardId"]], deck=deck[e])
            criados += 1
        print(f"{c['id']}: {c['alvo']}")
    print(f"\n{criados} card(s) criado(s); {ja_existiam} ja existiam (ignorados).")


def cmd_revisadas(args):
    consulta = f"rated:{args.dias}" + (f' "deck:{args.deck}"' if args.deck else "")
    ids = anki("findCards", query=consulta)
    saida, vistos = [], set()
    for info in anki("notesInfo", notes=list({c["note"] for c in anki("cardsInfo", cards=ids)})):
        campos = [limpar(v["value"]) for v in info["fields"].values()]
        chave = tuple(campos[:2])
        if len(campos) >= 2 and chave not in vistos:
            vistos.add(chave)
            saida.append({"frente": campos[0], "verso": campos[1]})
    print(json.dumps(saida, ensure_ascii=False, indent=1))
    print(f"\n# {len(saida)} nota(s) revisada(s) nos ultimos {args.dias} dia(s)", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("decks").set_defaults(f=cmd_decks)
    s = sub.add_parser("sobe")
    s.add_argument("lote")
    s.add_argument("--eixo", choices=["ambos", "output", "input"], default="ambos")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(f=cmd_sobe)
    r = sub.add_parser("revisadas")
    r.add_argument("--dias", type=int, default=7)
    r.add_argument("--deck")
    r.set_defaults(f=cmd_revisadas)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
