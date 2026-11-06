---
name: idiomas-texto-com-audio
description: Transforma um vídeo, série ou música em material de estudo "texto com áudio": pega a transcrição, traduz frase a frase e explica as expressões, para o aluno ler antes de assistir. Use quando ele pedir "estuda esse vídeo", "traduz esse episódio" ou mandar um link do YouTube.
---

# Texto com áudio (traduzir antes de assistir)

1. Conteúdo vem de: link do YouTube → `python scripts/transcrever_youtube.py "<url>" --idioma <cod>` (grava em `estudo/textos/<id>.txt`); ou texto que o dono colar/arquivo que ele indicar. Sem legenda no idioma: peça o texto.
2. Leia `estudo/perfil.md`. Se o conteúdo é de um assunto que o dono não usa no dia a dia (ex.: vídeo de construção para quem vai viajar), avise: vocabulário pouco útil. A escolha continua dele.
3. Crie `estudo/textos/<nome>-estudo.md` com, para cada frase: o original, a tradução em português e, **só onde houver**, a explicação curta de expressão ou significado de palavra difícil. Trechos longos: divida em blocos de ~20 frases.
4. Entregue assim: "Leia isso, depois assista ao conteúdo várias vezes até entender uns 60–80%, só então passe para o próximo."
5. Ofereça levar ao Anki as frases/expressões que ele marcar como difíceis (skill `idiomas-anki`). Nunca todas: só as escolhidas.
6. Registre em `estudo/log.md`.

Não reescreva o que foi dito no conteúdo original: traduza fiel. Tradução incerta: marque `(?)` e diga por quê.
