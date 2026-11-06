---
name: idiomas-video
description: Transforma um áudio de estudo já gerado em vídeo simples (um slide por fala, frase no idioma grande e tradução embaixo), para assistir no computador ou no celular. Use quando o dono pedir "faz um vídeo disso", "quero em vídeo" ou "versão pro celular/Reels".
---

# Vídeo do áudio de estudo

Simples de propósito: fundo escuro, uma fala por tela, texto grande. Serve para estudar lendo e ouvindo ao mesmo tempo, ou para postar.

1. O vídeo sai de um áudio que já existe. Confirme que há `estudo/audios/<nome>.mp3` e `estudo/audios/<nome>-tempos.json`. Se não houver, rode antes `python scripts/audio.py estudo/audios/<nome>.json` (a skill `idiomas-audio-personalizado`).
2. Rode `python scripts/video.py estudo/audios/<nome>.json`. Opções:
   - `--sem-traducao`: esconde o português (treino de escuta).
   - `--vertical`: 1080x1920, para celular, Reels e Shorts.
3. Entregue o caminho do `.mp4`. Os slides ficam em `<nome>_tmp/` (pode apagar).
4. Precisa de `pillow` (`pip install pillow`) e `ffmpeg`. `python scripts/checar.py` confere.

**Vídeo com animação, imagem ou legenda palavra a palavra** não faz parte do kit. Se o dono pedir, existe a ferramenta HyperFrames (HTML vira vídeo, `npx hyperframes`), mas ela é opcional e mais complexa: explique isso, diga o que vai instalar e só siga se ele quiser. O caminho padrão é o `video.py`.

Nunca publique o vídeo em nenhuma plataforma sem o dono ver e mandar.
