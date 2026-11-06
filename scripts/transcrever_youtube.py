# -*- coding: utf-8 -*-
"""Baixa a legenda de um video do YouTube (a do autor, ou a automatica) e salva como texto limpo.

Uso:
  python scripts/transcrever_youtube.py "https://www.youtube.com/watch?v=..." --idioma es
  python scripts/transcrever_youtube.py URL --idioma en --saida estudo/textos/meu-video.txt

Saida: um .txt com uma frase por linha, sem tempos. Entregue esse texto ao seu agente de IA para
traduzir frase a frase e explicar expressoes (veja skills/idiomas-texto-com-audio).
Nao baixa o video, so a legenda. Video sem legenda nenhuma: o script avisa.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def limpar_vtt(texto):
    linhas, anterior = [], ""
    for linha in texto.splitlines():
        linha = linha.strip()
        if (not linha or linha.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or "-->" in linha
                or re.fullmatch(r"\d+", linha)):
            continue
        linha = re.sub(r"<[^>]+>", "", linha).strip()
        if linha and linha != anterior:  # legenda automatica repete a linha anterior
            linhas.append(linha)
            anterior = linha
    return "\n".join(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--idioma", default="es", help="codigo do idioma da legenda (es, en, fr...)")
    ap.add_argument("--saida", help="arquivo .txt de saida (padrao: estudo/textos/<id-do-video>.txt)")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as d:
        arquivos, erro = [], ""
        # 1o tenta o idioma exato (poucas requisicoes); so depois as variantes (en-US, es-419...)
        for langs in (args.idioma, f"{args.idioma},{args.idioma}-.*"):
            r = subprocess.run(
                ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", langs,
                 "--sub-format", "vtt", "-o", str(Path(d) / "%(id)s"), args.url],
                capture_output=True, text=True, encoding="utf-8",
            )
            erro = r.stderr.strip()[-400:]
            arquivos = sorted(Path(d).glob("*.vtt"))
            if arquivos:
                break
        if not arquivos:
            sys.exit(f"Nenhuma legenda em '{args.idioma}' encontrada.\n{erro}")
        texto = limpar_vtt(arquivos[0].read_text(encoding="utf-8"))
        video_id = arquivos[0].name.split(".")[0]

    destino = Path(args.saida) if args.saida else Path("estudo/textos") / f"{video_id}.txt"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(texto, encoding="utf-8")
    print(f"Salvo: {destino} ({len(texto.splitlines())} linhas)")


if __name__ == "__main__":
    main()
