# -*- coding: utf-8 -*-
"""Gera audio de estudo (gratis, sem chave) a partir de uma conversa ou texto em JSON, com voz do Edge TTS.

Formato do JSON (veja estudo/audios/exemplo-conversa.json):
  {
    "idioma": "es",                        # es, en, fr, it, de, pt
    "titulo": "No mercado",
    "falas": [
      {"quem": "A", "texto": "Hola, buenos días.", "pt": "Oi, bom dia."},
      {"quem": "B", "texto": "Buenos días, ¿en qué le puedo ayudar?", "pt": "Bom dia, em que posso ajudar?"}
    ],
    "vozes": {"A": "es-MX-JorgeNeural", "B": "es-MX-DaliaNeural"}   # opcional
  }

Saida (na pasta do JSON): <nome>.mp3 (conversa inteira, com pausa entre as falas), <nome>-roteiro.md (texto + traducao)
e <nome>-tempos.json (inicio e fim de cada fala, usado por scripts/video.py).
Os pedacos ficam em <nome>_tmp/ (apague quando quiser).

Uso:
  python scripts/audio.py estudo/audios/minha-conversa.json
  python scripts/audio.py estudo/audios/minha-conversa.json --rate -20%     # mais devagar
  python scripts/audio.py estudo/audios/minha-conversa.json --pausa 1.5     # pausa maior entre falas (segundos)
  python scripts/audio.py --vozes es                                        # lista as vozes de um idioma
"""
import argparse
import asyncio
import json
import shutil
import subprocess
import sys
from pathlib import Path

import edge_tts

sys.stdout.reconfigure(encoding="utf-8")

VOZES_PADRAO = {
    "es": ("es-MX-JorgeNeural", "es-MX-DaliaNeural"),
    "en": ("en-US-GuyNeural", "en-US-JennyNeural"),
    "fr": ("fr-FR-HenriNeural", "fr-FR-DeniseNeural"),
    "it": ("it-IT-DiegoNeural", "it-IT-ElsaNeural"),
    "de": ("de-DE-ConradNeural", "de-DE-KatjaNeural"),
    "pt": ("pt-BR-AntonioNeural", "pt-BR-FranciscaNeural"),
}


def vozes_da_conversa(dados):
    idioma = dados.get("idioma", "es")
    if idioma not in VOZES_PADRAO:
        sys.exit(f"Idioma '{idioma}' sem voz padrao. Use um de {list(VOZES_PADRAO)} ou informe 'vozes' no JSON.")
    pessoas = []
    for fala in dados["falas"]:
        if fala.get("quem", "A") not in pessoas:
            pessoas.append(fala.get("quem", "A"))
    padrao = VOZES_PADRAO[idioma]
    mapa = {p: padrao[i % 2] for i, p in enumerate(pessoas)}
    mapa.update(dados.get("vozes", {}))
    return mapa


async def falar(texto, voz, rate, destino):
    await edge_tts.Communicate(texto, voz, rate=rate).save(str(destino))


async def listar_vozes(prefixo):
    for v in await edge_tts.list_voices():
        if v["Locale"].lower().startswith(prefixo.lower()):
            print(f"{v['ShortName']:28} {v['Gender']:7} {v['Locale']}")


def silencio(segundos, destino):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", str(segundos), "-c:a", "libmp3lame", "-b:a", "48k", str(destino)],
        check=True,
    )


def duracao(arquivo):
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arquivo)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(saida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", nargs="?")
    ap.add_argument("--rate", default="-10%", help="velocidade da voz (padrao -10%%, ou seja, um pouco mais devagar)")
    ap.add_argument("--pausa", type=float, default=0.8, help="segundos de silencio entre as falas")
    ap.add_argument("--vozes", metavar="IDIOMA", help="so lista as vozes disponiveis (ex.: es, en-US)")
    args = ap.parse_args()

    if args.vozes:
        asyncio.run(listar_vozes(args.vozes))
        return
    if not args.arquivo:
        ap.error("informe o arquivo JSON da conversa")
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg nao encontrado. Rode: python scripts/checar.py")

    caminho = Path(args.arquivo)
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    vozes = vozes_da_conversa(dados)
    base = caminho.with_suffix("")
    tmp = Path(str(base) + "_tmp")
    tmp.mkdir(exist_ok=True)

    pausa = tmp / "pausa.mp3"
    silencio(args.pausa, pausa)

    lista = []
    tempos = []
    t = 0.0
    dur_pausa = duracao(pausa)
    for i, fala in enumerate(dados["falas"], 1):
        voz = vozes[fala.get("quem", "A")]
        parte = tmp / f"{i:03d}.mp3"
        asyncio.run(falar(fala["texto"], voz, args.rate, parte))
        lista += [parte, pausa]
        d = duracao(parte)
        tempos.append({"i": i, "inicio": round(t, 3), "fim": round(t + d + dur_pausa, 3)})
        t += d + dur_pausa
        print(f"{i:03d} {voz}: {fala['texto']}")

    arquivo_lista = tmp / "lista.txt"
    arquivo_lista.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in lista), encoding="utf-8")
    saida = Path(str(base) + ".mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(arquivo_lista),
         "-c:a", "libmp3lame", "-b:a", "96k", str(saida)],
        check=True,
    )

    Path(str(base) + "-tempos.json").write_text(json.dumps(tempos, indent=1), encoding="utf-8")

    linhas = [f"# {dados.get('titulo', caminho.stem)}", ""]
    for fala in dados["falas"]:
        linhas.append(f"**{fala.get('quem', 'A')}:** {fala['texto']}")
        if fala.get("pt"):
            linhas.append(f"> {fala['pt']}")
        linhas.append("")
    Path(str(base) + "-roteiro.md").write_text("\n".join(linhas), encoding="utf-8")
    print(f"\nPronto: {saida}")


if __name__ == "__main__":
    main()
