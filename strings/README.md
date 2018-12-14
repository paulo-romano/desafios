# Desafio 1: Strings

Após ler o coding style do kernel Linux, você descobre a mágica que é
ter linhas de código com no máximo 80 caracteres cada uma.

Assim, você decide que de hoje em diante seus e-mails enviados também
seguirão um padrão parecido e resolve desenvolver um plugin para te ajudar
com isso. Contudo, seu plugin aceitará no máximo 40 caracteres por linha.

Implemente uma função que receba:
1. um texto qualquer
2. um limite de comprimento

e seja capaz de gerar os outputs dos desafios abaixo.

## Exemplo input

`In the beginning God created the heavens and the earth. Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters.`

`And God said, "Let there be light," and there was light. God saw that the light was good, and he separated the light from the darkness. God called the light "day," and the darkness he called "night." And there was evening, and there was morning - the first day.`

O texto deve ser parametrizável e se quiser, pode utilizar um texto de input de sua preferência.

### Parte 1 (Básico) - limite 40 caracteres
Você deve seguir o exemplo de output [deste arquivo](https://github.com/idwall/desafios/blob/master/strings/output_parte1.txt), onde basta o texto possuir, no máximo, 40 caracteres por linha. As palavras não podem ser quebradas no meio.

### Parte 2 (Intermediário) - limite 40 caracteres
O exemplo de output está [neste arquivo](https://github.com/idwall/desafios/blob/master/strings/output-parte2.txt), onde além de o arquivo possuir, no máximo, 40 caracteres por linha, o texto deve estar **justificado**.

## Notas de desenvolvimento
Na biblioteca padrão do python 3.4+, existe o modulo [textwrap](https://docs.python.org/3.4/library/textwrap.html) que será utilizado para quebrar as linhas do texto.
Para facilitar a implementação de comandos administrativos será utilizado a biblioteca [click](https://click.palletsprojects.com/en/7.x/).

## Como executar
1. Crie um ambiente virtual.
2. Ative o ambiente virtual.
3. Instale as dependências.
4. Execute o comando.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python textwrapper text '<long_ugly_text>' [--max-length 40]
python textwrapper file <file_path> [--max-length 40]
```

## Como executar os testes
1. Siga os passos 1 e 2 da sessão "Como executar" acima.
2. Instale as dependências de desenvolvimento.
3. Execute o tox.
```bash
pip install -r requirements-dev.txt
tox
```
