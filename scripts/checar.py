# -*- coding: utf-8 -*-
"""Confere (so leitura) se o computador esta pronto para o kit. Nao instala nada, nao muda nada.

Uso:  python scripts/checar.py
"""
import json
import shutil
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")


def ok(msg):
    print(f"[ok]    {msg}")


def falta(msg, como):
    print(f"[falta] {msg}\n        -> {como}")


def main():
    problemas = 0

    if sys.version_info >= (3, 10):
        ok(f"Python {sys.version.split()[0]}")
    else:
        falta(f"Python {sys.version.split()[0]} (precisa 3.10+)", "instale o Python 3.10 ou mais novo em python.org")
        problemas += 1

    for modulo, pip in (("edge_tts", "edge-tts"), ("requests", "requests"), ("PIL", "pillow")):
        try:
            __import__(modulo)
            ok(f"biblioteca {pip}")
        except ImportError:
            falta(f"biblioteca {pip}", f"pip install {pip}")
            problemas += 1

    for exe, como in (("yt-dlp", "pip install yt-dlp"), ("ffmpeg", "instale o ffmpeg (Windows: winget install Gyan.FFmpeg)")):
        if shutil.which(exe):
            ok(exe)
        else:
            falta(exe, como)
            problemas += 1

    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8765",
            data=json.dumps({"action": "version", "version": 6}).encode(),
        )
        versao = json.load(urllib.request.urlopen(req, timeout=3)).get("result")
        ok(f"Anki aberto com AnkiConnect (versao {versao})")
    except Exception:
        falta(
            "Anki aberto com o complemento AnkiConnect",
            "abra o Anki; se continuar falhando: Ferramentas > Complementos > Obter complementos > codigo 2055492159 e reinicie o Anki",
        )
        problemas += 1

    print()
    if problemas:
        print(f"{problemas} item(ns) para resolver antes de usar tudo. O que esta [ok] ja funciona.")
        sys.exit(1)
    print("Tudo pronto.")


if __name__ == "__main__":
    main()
