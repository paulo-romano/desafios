# Desafio 2: Crawlers

Parte do trabalho na IDwall inclui desenvolver *crawlers/scrapers* para coletar dados de websites.
Como nós nos divertimos trabalhando, às vezes trabalhamos para nos divertir!

O Reddit é quase como um fórum com milhares de categorias diferentes. Com a sua conta, você pode navegar por assuntos técnicos, ver fotos de gatinhos, discutir questões de filosofia, aprender alguns life hacks e ficar por dentro das notícias do mundo todo!

Subreddits são como fóruns dentro do Reddit e as postagens são chamadas *threads*.

Para quem gosta de gatos, há o subreddit ["/r/cats"](https://www.reddit.com/r/cats) com threads contendo fotos de gatos fofinhos.
Para *threads* sobre o Brasil, vale a pena visitar ["/r/brazil"](https://www.reddit.com/r/brazil) ou ainda ["/r/worldnews"](https://www.reddit.com/r/worldnews/).
Um dos maiores subreddits é o "/r/AskReddit".

Cada *thread* possui uma pontuação que, simplificando, aumenta com "up votes" (tipo um like) e é reduzida com "down votes".

Sua missão é encontrar e listar as *threads* que estão bombando no Reddit naquele momento!
Consideramos como bombando *threads* com 5000 pontos ou mais.

## Entrada
- Lista com nomes de subreddits separados por ponto-e-vírgula (`;`). Ex: "askreddit;worldnews;cats"

### Parte 1
Gerar e imprimir uma lista contendo número de upvotes, subreddit, título da thread, link para os comentários da thread, link da thread.
Essa parte pode ser um CLI simples, desde que a formatação da impressão fique legível.

### Parte 2
Construir um robô que nos envie essa lista via Telegram sempre que receber o comando `/NadaPraFazer [+ Lista de subrredits]` (ex.: `/NadaPraFazer programming;dogs;brazil`)

### Dicas
 - Use https://old.reddit.com/
 - Qualquer método para coletar os dados é válido. Caso não saiba por onde começar, procure por JSoup (Java), SeleniumHQ (Java), PhantomJS (Javascript) e Beautiful Soup (Python).
 
 ## Notas de desenvolvimento
Utilizei Beautiful Soup para parsear a resposta gerada pela biblioteca [requests](http://docs.python-requests.org/en/master/).

Cada requisição à um subreddit é feita em paralelo utilizanod asyncio e thread pool.

Para facilitar a implementação de comandos administrativos será utilizado a biblioteca [click](https://click.palletsprojects.com/en/7.x/).

Como nunca criei um bot de telegram, vou seguir [este](https://medium.freecodecamp.org/how-to-build-a-server-less-telegram-bot-227f842f4706) artigo para criar o bot do telegram. 

Implementei alguns parâmetros opcionais:
- [--log / -l] Ativa a exibição e logs.
- [--min-upvotes 5000] Muda o valor do filtro do valor de up votes (o valor padrão é 5000). 

## Como executar
1. Crie um ambiente virtual.
2. Ative o ambiente virtual.
3. Instale as dependências.
4. Execute o comando.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python reddit '<name_of_subreddit>' [--log / -l] [--min-upvotes 5000]
```

## Como executar os testes
1. Siga os passos 1 e 2 da sessão "Como executar" acima.
2. Instale as dependências de desenvolvimento.
3. Execute o tox.
```bash
pip install -r requirements-dev.txt
tox
```


## Como rodar e configurar o bot do telegram

### Configurando instancia
1. Copie o exemplo do arquivo .env para a raiz do projeto.
2. Crie um telegram bot via [BotFather](https://telegram.me/botfather) e salve o token na variável BOT_TOKEN do arquivo .env.
```bash
cp contrib/env.sample .env
``` 

### Execute o NGROK
1. Faça login no NGROK. Crie conta / token em [aqui](https://dashboard.ngrok.com/get-started).
2. Execute o tunel na porta 8000. Salve o endereço (algo como "https://c0cf0a5e.ngrok.io/") https na variável NGROK_URL do arquivo .env.
```bash
./contrib/ngrok authtoken <token>
./contrib/ngrok http 8000
```

### Execute o web app.
1. Execute utilizando o gunicorn.
```bash
gunicorn reddit:app -t 5000
```

### Chame o bot
1. Na janela do chat com seu bot, simplesmente escreva (e envie) /NadaPraFazer cats;dogs e receba todos os threads com mais de 5000 upvotes dos subreddits indicados.


