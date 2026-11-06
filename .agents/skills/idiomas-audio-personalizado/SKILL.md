---
name: idiomas-audio-personalizado
description: Cria uma conversa ou texto de estudo sobre um assunto do dia a dia do aluno e gera o áudio (mp3) com voz grátis. Repete ~50% das palavras do áudio anterior e traz ~50% novas. Use quando ele pedir "cria um áudio", "uma conversa sobre X" ou "mais um áudio".
---

# Áudio personalizado

Objetivo: contexto controlado. Mesmas palavras, situações diferentes.

1. Leia `estudo/perfil.md` (idioma, variante, nível, assuntos) e `estudo/log.md` (o que já foi criado).
2. Escolha o assunto: o que o dono pediu, ou o próximo do perfil. Um assunto por áudio.
3. **Regra dos 50%:** se existe áudio anterior em `estudo/audios/`, leia o JSON dele. O novo repete cerca de metade das palavras e expressões do anterior (em outra situação) e traz cerca de metade novas. Primeiro áudio: tudo novo.
4. Escreva a conversa (6 a 14 falas, 2 pessoas, frases que o dono diria/ouviria de verdade). Nível um degrau acima do que ele fala hoje; evite repetir o mesmo verbo em todas as falas.
5. **Mostre o texto com a tradução ao dono e espere o "sim".**
6. Grave `estudo/audios/<assunto>.json` no formato de `estudo/audios/exemplo-conversa.json` (`idioma`, `titulo`, `falas[{quem,texto,pt}]`; `vozes` só se ele quiser outra voz).
7. Rode `python scripts/audio.py estudo/audios/<assunto>.json` (padrão: velocidade -10%, pausa de 0,8 s; use `--rate -20%` se for iniciante). Entregue o caminho do `.mp3` e do `-roteiro.md`.
8. Ofereça os cards (skill `idiomas-anki`) e registre em `estudo/log.md`.

Para voz mais real (opcional, pago, do dono): só se ele pedir. Ver `AGENTS.md`.
