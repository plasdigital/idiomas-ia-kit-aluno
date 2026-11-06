# Ferramentas e custos

| Ferramenta | Custo | Papel | Alternativa |
|---|---|---|---|
| ChatGPT + app Codex | plano pago | o agente que cria arquivos, roda scripts e abre o Anki | Claude Code (plano pago); Antigravity e Cursor leem o mesmo `AGENTS.md` |
| Anki + AnkiConnect | grátis | repetição espaçada; o AnkiConnect deixa o agente criar cards | CSV importado à mão (mais trabalho) |
| Edge TTS (biblioteca `edge-tts`) | grátis, sem chave | voz dos áudios | ElevenLabs (voz mais real, pago, permite clonar sua voz) |
| `yt-dlp` | grátis | baixa legenda de vídeos do YouTube | colar o texto à mão |
| `ffmpeg` | grátis | junta os pedaços de áudio e monta o vídeo | — |
| `pillow` (biblioteca Python) | grátis | desenha os slides do vídeo (`scripts/video.py`) | — |
| HyperFrames (opcional) | grátis | vídeo com animação, a partir de HTML (`npx hyperframes`); só se você quiser algo além do vídeo simples | — |

**Único gasto obrigatório: o plano da IA.** Voz paga só se você está em nível avançado e precisa de áudio mais natural.
Sobre chaves de API: nunca cole chave em arquivos do repositório; se usar uma, mantenha em variável de ambiente.
