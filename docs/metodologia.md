# A metodologia

Três ideias se combinam: **texto com áudio**, **repetição espaçada** e **contexto controlado**. A IA tira o trabalho braçal de cada uma.

## 1. Compreensão é a base

Entender o que se ouve, vê ou lê é a base de aprender qualquer idioma. Dois hábitos treinam isso:

- **Mineração de sentenças**: pegar frases de conteúdo real e estudar frase a frase.
- **Texto com áudio**: ler a tradução e as expressões *antes* de assistir/ouvir o conteúdo; depois assistir várias vezes, até entender uns 60–80%. Só então passar para o próximo.

Com IA: você entrega a transcrição (vídeo, série, música) e ela devolve a tradução frase a frase com o significado das expressões. O trabalho que levava horas vira minutos.

## 2. Repetição espaçada (Anki)

O Anki mostra cada card em intervalos crescentes (hoje, daqui a 3 dias, uma semana, um mês). Ver uma palavra todo dia por uma semana e nunca mais é o pior caso: ela não fixa. A essência é **espaçar**.

Antes, minerar frases e montar os cards (frente, verso, descrição, áudio) tomava cerca de uma hora por dia. Com um agente dentro do computador, ele cria os cards e os áudios por script (`scripts/anki.py`).

## 3. O problema da repetição fraca, e o contexto controlado

Estudar só com conteúdo variado (um episódio hoje, outro amanhã, cada um com seu tema) tem um problema: **poucas palavras se repetem** (talvez 5% entre um conteúdo e outro). E memorizar exige ver a mesma palavra **em situações diferentes**, não só em tempos diferentes.

A solução: gerar com IA **áudios personalizados**, com um contexto que você controla:

1. Escolha assuntos do seu **dia a dia** (onde você vai realmente falar). Quem vai viajar não ganha nada estudando vocabulário de construção.
2. A IA cria um áudio (conversa) sobre o assunto.
3. O próximo áudio **repete ~50% das palavras** do anterior e traz ~50% novas, em outra situação.
4. Resultado: espaçamento *e* contexto variado, com um vocabulário pequeno e bem dominado. Saber 100 expressões de verdade vale mais do que conhecer mil de forma rasa.

Os áudios podem ficar numa pasta ou playlist particular (só no seu celular, ou num canal próprio).

## 4. Do seu idioma para o idioma estrangeiro

Estudar só do idioma estrangeiro para o seu (entender) deixa a memória frágil. **Lembrar de cabeça** ("como se diz X?") memoriza muito mais: é a recuperação ativa, estudada na ciência da aprendizagem.

O ideal seria os dois sentidos; na prática não é sustentável. A divisão do kit:

| Treino | Ferramenta | Sentido |
|---|---|---|
| Entender | áudios e textos com tradução | idioma → português |
| **Falar / lembrar** | **Anki `Output`**: frente em português, verso no idioma | português → idioma |
| Reconhecer ouvindo | Anki `Input` (opcional) | idioma → português |

## 5. Teste de memória

O Anki pode enganar: de tanto repetir, você decora a *estrutura* da frase, não o significado da palavra. Em outro contexto, o cérebro não associa. Teste: peça um áudio **só com as palavras que você revisou** e ouça sem olhar. Se não entende 100% de forma natural, você decorou, não memorizou. É o que a skill `idiomas-teste-de-memoria` faz.

## 6. Conversação em contexto controlado

Conversar com a IA (texto ou voz) sobre qualquer assunto aleatório não treina o que importa. Peça que ela use **os textos e as palavras que você já estudou**, com contextos parecidos (não idênticos). Você cresce dentro do que domina.

## 7. Falar desde o primeiro dia

Falar é difícil de qualquer jeito. Quem estuda seis meses só ouvindo séries sente a primeira conversa como a primeira vez. A compreensão é importante, mas a fala se treina falando, desde cedo.

## 8. Gramática: só como andaime

Explique um ponto de gramática **só quando ele destrava algo específico** que o aluno está estudando, no menor tamanho (uma linha). Gramática solta, sem uso, não entra.

## Crédito

Mineração de sentenças e estudo de textos com áudio: método que o autor deste kit aprendeu com Mário Vergara. O resto (áudios personalizados, Anki invertido, agente de IA) é a adaptação com IA.
