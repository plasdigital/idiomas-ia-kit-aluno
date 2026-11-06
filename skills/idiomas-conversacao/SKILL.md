---
name: idiomas-conversacao
description: Treina conversação com o aluno em contexto controlado, usando só os textos, frases e palavras que ele já estudou (texto ou modo voz). Use quando ele pedir "vamos treinar conversação" ou "simula uma conversa sobre X".
---

# Conversação em contexto controlado

Conversa aleatória não treina o que importa. Aqui você só usa o que ele já estudou.

1. Leia `estudo/perfil.md` e liste o que ele estudou: `estudo/audios/*.json`, `estudo/lotes/*.json`, `estudo/textos/*-estudo.md`, `estudo/log.md`. Opcional: `python scripts/anki.py revisadas --dias 14`.
2. Proponha a situação (ou use a que ele pediu), parecida com uma que ele estudou, **não idêntica**.
3. Conduza em turnos curtos, **no idioma**, na variante do perfil, uma pergunta ou fala por vez. Use vocabulário já estudado e no máximo uma ou duas palavras novas por rodada.
4. Ele errou? Deixe terminar a frase, corrija em uma linha ("Mais natural: ...") e continue. Sem aula de gramática, a não ser um andaime de uma linha se travou nisso.
5. No modo voz do app, o mesmo vale: você tem acesso a esse contexto, então conversa sobre o que ele estudou.
6. No fim: liste 3 a 5 frases que ele travou. Ofereça virar cards (skill `idiomas-anki`) só se ele aceitar; registre erros reais em `estudo/erros.md` e uma linha em `estudo/log.md`.

Começar a falar desde cedo vale mais do que esperar "saber tudo": incentive, sem forçar.
