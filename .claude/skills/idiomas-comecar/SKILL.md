---
name: idiomas-comecar
description: Primeira conversa do aluno: confere o computador (Python, ffmpeg, Anki) e entrevista o dono para preencher estudo/perfil.md. Use quando o perfil estiver vazio, quando ele disser "configura meu estudo" ou "estou começando".
---

# Começar: configurar o computador e o perfil

1. Rode `python scripts/checar.py`. Para cada `[falta]`, diga ao dono o que vai instalar e instale (`pip install ...`, `winget install Gyan.FFmpeg`). O Anki precisa estar aberto com o AnkiConnect (código 2055492159): peça para ele abrir/instalar, não dá para fazer por ele.
2. Rode de novo até só restar o que depende dele.
3. Entreviste o dono, uma pergunta de cada vez, e preencha `estudo/perfil.md`:
   - idioma(s) e variante/sotaque (ex.: espanhol do México);
   - nível hoje: o que entende e o que consegue falar;
   - por que estuda e com quem vai falar de verdade;
   - **5 a 10 assuntos do dia a dia** em que ele quer falar (casa, trabalho, mercado, família, viagem marcada...);
   - tempo por dia; nome do deck base no Anki (ex.: `Espanhol`).
4. Proponha o primeiro conteúdo: **uma conversa curta sobre o assunto mais usado** (skill `idiomas-audio-personalizado`) com os cards (`idiomas-anki`). Mostre o texto antes de gerar.
5. Anote em `estudo/log.md`.

Não crie conteúdo antes do perfil estar preenchido.
