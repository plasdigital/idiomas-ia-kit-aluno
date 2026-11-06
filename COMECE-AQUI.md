# Comece aqui (uma vez só, ~20 minutos)

## 1. Instale o app

1. Tenha o **ChatGPT com plano pago** e instale o **app do Codex** no computador (procure "Codex ChatGPT download" no site oficial da OpenAI).
   Ele precisa rodar **dentro do computador**, não só na web, para criar arquivos e abrir o Anki por você.
   (Alternativa: Claude Code. Esta pasta funciona nos dois.)
2. Instale o **Anki**: apps.ankiweb.net.
3. No Anki: *Ferramentas → Complementos → Obter complementos* e cole o código **2055492159** (AnkiConnect). Reinicie o Anki.
   O Anki precisa estar **aberto** quando a IA for criar cards.

## 2. Baixe esta pasta

`git clone` do repositório, ou o botão **Code → Download ZIP** e descompacte onde quiser (Documentos, Área de Trabalho...).

## 3. Abra a pasta no Codex como projeto

No Codex: *Novo projeto* → escolha a pasta → mude para o **modo de código**. O projeto é só uma pasta no seu computador;
tudo que a IA registrar fica nela.

**Permissões:** com as permissões padrão o Codex pede aprovação a cada comando. Dar *acesso total* é mais rápido
(ele abre o Anki e roda os scripts sozinho), mas vale só se você entende que ele pode mexer em qualquer arquivo do
computador. Na dúvida, deixe pedir aprovação.

## 4. Primeira conversa

Cole:

> Leia o AGENTS.md e me ajude a configurar meu estudo. Rode `python scripts/checar.py` e instale o que faltar.

A IA vai instalar o que falta (Python, ffmpeg, bibliotecas), conferir o Anki e **te entrevistar** para preencher
[estudo/perfil.md](estudo/perfil.md): idioma, nível, por que você estuda e **os assuntos do seu dia a dia** (é com eles
que o conteúdo será montado).

## 5. Primeiro resultado

Peça: **"Crie uma conversa curta sobre [um assunto do meu dia a dia] com áudio e os cards do Anki."**
Em alguns minutos você tem um mp3 para ouvir e os cards nos decks `<Idioma> Output` e `<Idioma> Input`.
Quer em vídeo? Peça: *"faz um vídeo desse áudio"* (ou *"versão vertical para o celular"*).
O restante do dia a dia é conversar: *"adiciona as palavras desse vídeo no meu Anki"*, *"vamos treinar conversação"*.
