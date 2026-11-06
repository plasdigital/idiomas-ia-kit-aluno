# Estudo de idiomas com IA — manual do agente

Esta pasta é o **laboratório de estudo do dono**. Você (Codex, Claude Code, Antigravity, Cursor) monta o conteúdo; ele estuda.
O dono conversa em português. Responda em português. Ele não decora comando: **você roda os scripts**.

## Regras que não se pulam

1. **Leia `estudo/perfil.md` antes de criar qualquer conteúdo.** Perfil vazio → entreviste o dono (idioma, nível, motivo, assuntos do dia a dia, variante/sotaque) e preencha o arquivo. Nada de conteúdo genérico.
2. **Conteúdo é do dia a dia dele.** Toda frase tem que ser algo que ele diria ou ouviria de verdade. Frase de livro didático, turismo ou formalidade que ele não vive: não entra.
3. **Frase inteira, nunca palavra solta.** Poucas frases usáveis, não lista gigante de vocabulário.
4. **Consolidar vence expandir.** Antes de criar conteúdo novo, leia `estudo/erros.md` e `estudo/log.md`. Se há erro não resolvido ou ilha `🔄 em uso`, reforce o que travou (variação da frase, outro contexto) em vez de abrir assunto novo.
5. **Um assunto por vez, sem repetir o mesmo verbo.** No máximo 2 cards com o mesmo verbo central por lote. Card precisa de carga (uma expressão, preposição ou verbo que ele não montaria sozinho).
6. **Registre.** Depois de cada sessão acrescente uma linha em `estudo/log.md`. Quando o dono trouxer uma correção real, `estudo/erros.md`. Quando ele disser "registra isso", escreva em `estudo/` (ou neste arquivo, se for regra de como trabalhar).
7. **Nunca** apague nem sobrescreva cards, decks ou arquivos do dono sem ele ver o que será apagado. Erro dele só vira card se ele mandar.
8. **Nunca** gere ou apague coisas fora desta pasta (exceto o Anki, via `scripts/anki.py`).

## O que o dono pede → o que você faz

| Pedido | Skill | Comando principal |
|---|---|---|
| "configura meu estudo", primeira conversa | `idiomas-comecar` | `python scripts/checar.py` + preencher `estudo/perfil.md` |
| "cria uma conversa/áudio sobre X" | `idiomas-audio-personalizado` | escrever `estudo/audios/<nome>.json` → `python scripts/audio.py estudo/audios/<nome>.json` |
| "põe no Anki", "cria os cards" | `idiomas-anki` | escrever `estudo/lotes/<nome>.json` → `python scripts/anki.py sobe estudo/lotes/<nome>.json` |
| "estuda esse vídeo/série/música" | `idiomas-texto-com-audio` | `python scripts/transcrever_youtube.py <url> --idioma <cod>` → traduzir frase a frase |
| "faz um vídeo desse áudio" | `idiomas-video` | `python scripts/video.py estudo/audios/<nome>.json` (precisa do áudio já gerado) |
| "vamos treinar conversação" | `idiomas-conversacao` | sem script: você conversa só com o que ele já estudou |
| "testa se eu memorizei" | `idiomas-teste-de-memoria` | `python scripts/anki.py revisadas --dias 7` → áudio com essas frases |

As skills estão em `skills/` (cópias em `.claude/skills/` e `.agents/skills/` para o Claude Code e o Codex acharem sozinhos).

## Leitura (pode rodar sem perguntar)

| Comando | O que faz |
|---|---|
| `python scripts/checar.py` | confere Python, bibliotecas, yt-dlp, ffmpeg e Anki. Não instala nada |
| `python scripts/anki.py decks` | lista os decks |
| `python scripts/anki.py sobe <lote.json> --dry-run` | mostra os cards, sem criar |
| `python scripts/anki.py revisadas --dias N [--deck D]` | frases revisadas nos últimos N dias |
| `python scripts/audio.py --vozes es` | lista vozes de um idioma |

## Escrevem (mostre o conteúdo ao dono e só rode depois do "sim")

| Comando | Muda o quê |
|---|---|
| `python scripts/anki.py sobe <lote.json>` | cria notas no Anki (decks `<base> Output` e `<base> Input`, tipo de nota `Estudo IA`). Duplicata é ignorada, nunca sobrescrita |
| `python scripts/audio.py <conversa.json>` | cria mp3 e roteiro ao lado do JSON (a pasta `_tmp` pode ser apagada) |
| `python scripts/transcrever_youtube.py <url>` | cria um `.txt` em `estudo/textos/` |
| `python scripts/video.py <conversa.json>` | cria um `.mp4` ao lado do JSON (precisa do mp3 e do `-tempos.json` do `audio.py`) |

`pip install`/`winget install` para configurar o computador: diga ao dono o que vai instalar antes.

## Os dois eixos do Anki (não misture)

| Deck | Frente | Verso | Treina |
|---|---|---|---|
| `<base> Output` | português | idioma + áudio | **falar**: lembrar de cabeça (recuperação ativa) |
| `<base> Input` | idioma + áudio | português | **entender** ouvindo |

Os dois eixos **não precisam ter a mesma frase nem o mesmo nível**: o Input pode ser um degrau acima do que o dono fala hoje (ele entende mais do que produz). O padrão do `anki.py sobe` é subir a mesma frase nos dois; use `--eixo input` ou `--eixo output` quando o lote for só de um lado.

## Armadilhas

| O que aparece | O que significa |
|---|---|
| `Nao consegui falar com o Anki` | Anki fechado, ou sem o AnkiConnect (código 2055492159). Peça para abrir/instalar; não tente de novo em loop |
| `duplicate` / "ja existiam" | a frase já está no deck. Normal; não é erro |
| acento virando `?` ou lixo no terminal | você escreveu o JSON por PowerShell. Grave arquivos com a ferramenta de edição de arquivos e rode o Python direto |
| `Nenhuma legenda em 'xx'` | o vídeo não tem legenda nesse idioma. Peça outro vídeo ou o texto colado |
| áudio com a voz errada | `audio.py` escolhe a voz pelo `idioma` do JSON; para outra, use `"vozes"` no JSON (`--vozes <idioma>` lista) |
| `ffmpeg nao encontrado` | rode `python scripts/checar.py` e instale (Windows: `winget install Gyan.FFmpeg`) |

## Voz natural (opcional)

A voz padrão é a do Edge TTS (grátis, sem chave). Para voz mais real, o dono pode assinar uma API de voz (ex.: ElevenLabs, a partir de ~US$ 5/mês) e clonar a própria voz. **Só proponha se o dono está em nível avançado e pediu mais realismo; é gasto dele: nunca assine nem coloque chave sem ele pedir.**

## Onde está o porquê

`docs/metodologia.md` (o método e por que cada passo existe) · `docs/ferramentas.md` (custos e alternativas) · `skills/` (o passo a passo de cada pedido).
