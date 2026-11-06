---
name: idiomas-anki
description: Cria cards de frase inteira no Anki, com áudio, em dois decks (Output para falar, Input para entender), a partir de uma conversa, texto ou lista de frases. Use quando o aluno pedir "põe no Anki", "cria os cards" ou "adiciona essas palavras".
---

# Cards no Anki

Requisito: Anki aberto com AnkiConnect (`python scripts/checar.py` confere).

1. Reúna as frases (da conversa em `estudo/audios/`, do texto em `estudo/textos/` ou do que o dono mandou). **Frase inteira, nunca palavra solta.**
2. Filtre: só o que o dono diria ou ouviria de verdade; no máximo 2 cards com o mesmo verbo central por lote; cada card com alguma carga (expressão, preposição, verbo novo). Cortou frase? Diga qual e por quê.
3. Grave `estudo/lotes/<nome>.json` no formato de `estudo/lotes/exemplo.json`:
   `{"idioma","deck_base","tag","cards":[{"id","alvo","pt","nota"}]}`. `deck_base` vem do `estudo/perfil.md`.
4. Rode `python scripts/anki.py sobe estudo/lotes/<nome>.json --dry-run` e **mostre ao dono**. Só depois do "sim": `python scripts/anki.py sobe estudo/lotes/<nome>.json`.
   - O padrão sobe os dois eixos. `--eixo output` sobe só o deck de **falar** (frente em português); `--eixo input` só o de **entender**.
   - O áudio é gerado por frase (um mp3 que serve aos dois cards).
5. Confira: `python scripts/anki.py decks` mostra os decks `<base> Output` e `<base> Input`. Diga quantos cards foram criados e quantos já existiam.
6. Registre em `estudo/log.md`.

Nunca apague cards nem decks. Para remover algo, o dono faz no Anki, ou mostre exatamente o que sairia e espere o "sim".
Erro corrigido por um nativo só vira card se o dono mandar: ele vai para `estudo/erros.md` primeiro.
