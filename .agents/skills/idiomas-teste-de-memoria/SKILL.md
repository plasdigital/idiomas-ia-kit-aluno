---
name: idiomas-teste-de-memoria
description: Testa se o aluno memorizou de verdade o que revisou no Anki: gera um áudio só com as frases revisadas recentemente, para ele ouvir sem olhar. Use quando ele pedir "testa se eu memorizei" ou "será que eu aprendi mesmo isso?".
---

# Teste de memória

De tanto repetir no Anki, o aluno pode decorar a estrutura da frase sem fixar o significado. Em outro contexto, não reconhece. O teste mostra isso.

1. `python scripts/anki.py revisadas --dias 7` (ou o `--deck "<base> Output"` e outro período que ele pedir). Saída: lista de `{frente, verso}`.
2. Junte as frases **no idioma** (o lado do idioma pode ser a frente ou o verso, conforme o deck). Se forem muitas, pegue até 20.
3. Monte uma conversa curta que use essas frases, **em contexto diferente do original** (outra situação, outras pessoas), no formato de `estudo/audios/exemplo-conversa.json`. Salve como `estudo/audios/teste-memoria-<data>.json` e rode `python scripts/audio.py` nele.
4. Instrua: "Ouça sem ler. Se entender tudo de forma natural, memorizou. Onde travou, anote."
5. Quando ele trouxer as frases em que travou: sugira reforço (outro contexto com `idiomas-audio-personalizado`; card com variação só se ele pedir) e registre em `estudo/log.md`.

Não altere cards nem agendamentos do Anki neste teste: ele só lê.
