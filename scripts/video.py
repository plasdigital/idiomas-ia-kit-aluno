# -*- coding: utf-8 -*-
"""Transforma um audio de estudo em video simples (um slide por fala: frase no idioma grande, traducao embaixo).

Precisa que o audio ja tenha sido gerado com scripts/audio.py (ele cria o .mp3 e o -tempos.json ao lado do JSON).
Usa so ffmpeg e Pillow (pip install pillow). Sem chave, sem custo.

Uso:
  python scripts/video.py estudo/audios/minha-conversa.json
  python scripts/video.py estudo/audios/minha-conversa.json --sem-traducao     # esconde o portugues (treino de escuta)
  python scripts/video.py estudo/audios/minha-conversa.json --vertical         # 1080x1920 (Reels/Shorts/celular)

Saida: <nome>.mp4 ao lado do JSON. Os slides ficam em <nome>_tmp/ (apague quando quiser).
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

FUNDO = (7, 24, 51)
BRANCO = (255, 255, 255)
AMARELO = (253, 212, 16)
CINZA = (159, 176, 200)

FONTES = [
    "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONTES_FINAS = [
    "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def fonte(lista, tamanho):
    for caminho in lista:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    sys.exit("Nao achei uma fonte do sistema. Instale o Arial ou o DejaVu Sans.")


def quebrar(draw, texto, fnt, largura):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if draw.textlength(teste, font=fnt) <= largura:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def slide(destino, w, h, quem, texto, pt, titulo):
    img = Image.new("RGB", (w, h), FUNDO)
    d = ImageDraw.Draw(img)
    margem = int(w * 0.08)
    util = w - 2 * margem
    esc = h / 1080
    f_titulo = fonte(FONTES_FINAS, int(34 * esc))
    f_quem = fonte(FONTES, int(40 * esc))
    f_texto = fonte(FONTES, int(86 * esc))
    f_pt = fonte(FONTES_FINAS, int(48 * esc))

    d.text((margem, int(60 * esc)), titulo, font=f_titulo, fill=CINZA)
    linhas = quebrar(d, texto, f_texto, util)
    alt_texto = len(linhas) * int(106 * esc)
    linhas_pt = quebrar(d, pt, f_pt, util) if pt else []
    alt_pt = len(linhas_pt) * int(62 * esc) + (int(50 * esc) if pt else 0)
    y = (h - (alt_texto + alt_pt)) // 2

    d.text((margem, y - int(70 * esc)), quem, font=f_quem, fill=AMARELO)
    for linha in linhas:
        d.text((margem, y), linha, font=f_texto, fill=BRANCO)
        y += int(106 * esc)
    y += int(50 * esc)
    for linha in linhas_pt:
        d.text((margem, y), linha, font=f_pt, fill=CINZA)
        y += int(62 * esc)
    img.save(destino)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", help="JSON da conversa (o mesmo do audio.py)")
    ap.add_argument("--sem-traducao", action="store_true", help="nao mostra o portugues")
    ap.add_argument("--vertical", action="store_true", help="1080x1920 em vez de 1920x1080")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg nao encontrado. Rode: python scripts/checar.py")

    caminho = Path(args.arquivo)
    base = caminho.with_suffix("")
    mp3 = Path(str(base) + ".mp3")
    tempos_json = Path(str(base) + "-tempos.json")
    if not mp3.exists() or not tempos_json.exists():
        sys.exit(f"Falta o audio. Rode antes: python scripts/audio.py {args.arquivo}")

    dados = json.loads(caminho.read_text(encoding="utf-8"))
    tempos = json.loads(tempos_json.read_text(encoding="utf-8"))
    w, h = (1080, 1920) if args.vertical else (1920, 1080)
    titulo = dados.get("titulo", caminho.stem)

    tmp = Path(str(base) + "_tmp")
    tmp.mkdir(exist_ok=True)
    linhas_lista = []
    for fala, t in zip(dados["falas"], tempos):
        png = tmp / f"slide{t['i']:03d}.png"
        pt = None if args.sem_traducao else fala.get("pt")
        slide(png, w, h, f"Pessoa {fala.get('quem', 'A')}", fala["texto"], pt, titulo)
        linhas_lista.append(f"file '{png.resolve().as_posix()}'\nduration {t['fim'] - t['inicio']:.3f}\n")
    # o ffmpeg ignora a duracao do ultimo item se ele nao se repetir
    linhas_lista.append(f"file '{png.resolve().as_posix()}'\n")
    lista = tmp / "slides.txt"
    lista.write_text("".join(linhas_lista), encoding="utf-8")

    saida = Path(str(base) + ".mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista), "-i", str(mp3),
         "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "128k", "-shortest", str(saida)],
        check=True,
    )
    print(f"Pronto: {saida}")


if __name__ == "__main__":
    main()
