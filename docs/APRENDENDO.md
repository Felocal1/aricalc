# ARI CALC — Manual de Aprendizagem

Este manual explica a AriCalc passo a passo. Ele foi escrito para quem está começando a programar e quer entender o *porquê* de cada decisão no código, não apenas o *como*.

---

## Índice

1. [O objetivo do projeto](#1-o-objetivo-do-projeto)
2. [Como a AriCalc está organizada](#2-como-a-ariccalc-está-organizada)
3. [Módulo por módulo](#3-módulo-por-módulo)
   - [operacoes.py — o motor matemático](#operacoespy--o-motor-matemático)
   - [historico.py — registrando as contas](#historicopy--registrando-as-contas)
   - [memoria.py — a memória da calculadora](#memoriapy--a-memória-da-calculadora)
   - [utils.py — validando o que o usuário digita](#utilspy--validando-o-que-o-usuário-digita)
   - [main.py — a interface no terminal](#mainpy--a-interface-no-terminal)
4. [A versão web — FastAPI + navegador](#4-a-versão-web--fastapi--navegador)
   - [servidor.py — a API](#servidorpy--a-api)
   - [static/ — o navegador (HTML, CSS, JS)](#static--o-navegador-html-css-js)
   - [A grande ideia: mesmo motor, duas interfaces](#a-grande-ideia-mesmo-motor-duas-interfaces)
5. [Testes unitários](#5-testes-unitários)
6. [Exercícios propostos](#6-exercícios-propostos)

---

## 1. O objetivo do projeto

A AriCalc é uma calculadora escrita em Python para **terminal e navegador web**. Mas ela é mais do que isso: é um **projeto de apoio ao aprendizado** de programação.

A ideia central é separar o que o programa **faz** (a matemática) de como ele **conversa com o usuário** (terminal ou navegador). Em inglês isso se chama *separation of concerns* (separação de responsabilidades), e é uma das boas práticas mais importantes da programação.

```
┌──────────────────────┐        ┌───────────────────────────┐
│   FRONTEND           │       │    BACKEND                 │
│   (main.py OU web)   │        │   (calculadora/)          │
│                      │        │                           │
│  - mostra o menu/    │  usa   │  - soma(), divisao()      │
│    a calculadora     │ ─────► │  - raiz_quadrada()        │
│  - lê o que o        │        │  - Historico (salvar)     │
│    usuário digita    │        │  - Memoria (M+, M-, MR)   │
│  - mostra o          │        │                           │
│    resultado         │        │                           │
└──────────────────────┘        └───────────────────────────┘
```

**Vantagem para o aprendiz:** a AriCalc já tem **duas** interfaces usando o **mesmo** motor — o terminal (`main.py`) e a web (`servidor.py` + `static/`). Isso prova na prática que o motor não sabe (nem precisa saber) como o usuário está interagindo.

---

## 2. Como a AriCalc está organizada

```
AriCalc/
│
├── main.py                    # 1a. INTERFACE TERMINAL — menu no console
├── servidor.py                # 1b. INTERFACE WEB — API FastAPI
├── static/                    # 1b. INTERFACE WEB — página do navegador
│   ├── index.html             #    estrutura da página
│   ├── style.css              #    visual
│   └── script.js              #    lógica do navegador (chama a API)
├── calculadora/               # 2. BACKEND — a lógica que funciona sozinha
│   ├── __init__.py
│   ├── operacoes.py
│   ├── historico.py
│   ├── memoria.py
│   └── utils.py
├── tests/                     # 3. TESTES — verifica se o backend está certo
│   └── test_operacoes.py
├── requirements.txt           # dependências da versão web
└── docs/
    └── APRENDENDO.md          # 4. DOCUMENTAÇÃO — este arquivo
```

Cada arquivo tem **um único papel**. Quando se aprende a programar, dividir bem o problema pela metade faz com que cada peça seja fácil de entender e de corrigir.

---

## 3. Módulo por módulo

### `operacoes.py` — o motor matemático

Este é o arquivo mais importante. Ele contém funções puras de matemática: recebem números, devolvem números.

```python
def soma(a: float, b: float) -> float:
    """Retorna a soma de dois números (a + b)."""
    return a + b
```

**O que cada parte significa:**

| Parte do código | O que é |
|---|---|
| `def soma` | Estamos definindo (criando) uma função chamada `soma`. |
| `(a: float, b: float)` | A função recebe dois parâmetros `a` e `b`, e a anotação `: float` documenta que esperamos números. |
| `-> float` | A função **retorna** um número (o resultado). |
| `"""..."""` | A *docstring*: texto explicando o que a função faz e como usá-la. |
| `return a + b` | Calcula e devolve a soma. |

**Por que `return` e não `print`?**

Isso é um conceito-chave. Uma função com `print` apenas mostra algo na tela; uma função com `return` **devolve um valor que pode ser usado por outros códigos**. Como o motor precisa devolver resultados (para depois guardar no histórico, por exemplo), todas as funções de `operacoes.py` usam `return`.

**Tratamento de erros:**

Nem todas as contas são possíveis. O módulo cuida de três casos:

| Caso | Erro levantado | Exemplo |
|---|---|---|
| Dividir por zero | `ZeroDivisionError` | `divisao(10, 0)` |
| Raiz de número negativo | `ValueError` | `raiz_quadrada(-4)` |
| Logaritmo de zero ou negativo | `ValueError` | `logaritmo(0)` |

No lugar de deixar o Python quebrar com uma "stack trace" gigante, a AriCalc levanta **exceções com mensagem clara** e a interface as mostra educadamente:
```python
if b == 0:
    raise ZeroDivisionError("Não é possível dividir por zero.")
```

**Trigonometria em radianos:**

Lembre-se: o Python trabalha com ângulos em radianos. No `main.py`, a conversão graus → radianos acontece com a fórmula:
```
radianos = graus * (π / 180)
```

---

### `historico.py` — registrando as contas

O histórico guarda cada operação em um **dicionário**:

```python
{
    "expressao": "5 + 3",          # o que foi feito (texto)
    "resultado": 8,                # o resultado (número)
    "momento": "15/09/2026 10:30"  # quando foi feito (data/hora)
}
```

E a lista de todos esses dicionários é **salva em um arquivo** chamado `historico.json`. Isso demonstra o conceito de **persistência**: os dados sobrevivem e estão disponíveis na próxima vez que o programa rodar.

```
MEMÓRIA (RAM)                          DISCO (arquivo)
┌──────────────┐   salvar()   ┌───────────────────────┐
│  registros   │ ───────────► │  historico.json       │
│  [ {..}, ..] │ ◄─────────── │  [
└──────────────┘  carregar()  │    {"expressao": ...}
                              │  ]
                              └───────────────────────┘
```

**Por que JSON?** Porque é um formato de texto que qualquer linguagem de programação consegue ler. É o "esperanto" da troca de dados entre programas.

---

### `memoria.py` — a memória da calculadora

Uma calculadora física tem botões de memória; a AriCalc também. O estado (o número guardado) fica **dentro do objeto** `Memoria`:

```python
m = Memoria()
m.armazenar(10)   # guarda 10   (MS)
m.somar(5)        # agora 15    (M+)
m.recall()        # devolve 15  (MR)
m.limpar()        # apaga       (MC)
```

Isso demonstra o conceito de **objeto com estado**: o mesmo objeto guarda informações e as modifica ao longo do tempo. É a base da Programação Orientada a Objetos (POO).

---

### `utils.py` — validando o que o usuário digita

Um usuário pode digitar qualquer coisa: letras onde esperamos números, símbolos desconhecidos, nada... A função `ler_numero` resolve isso e faz com que o programa **peça de novo** até receber um número válido:

```python
def ler_numero(mensagem):
    while True:
        entrada = input(mensagem).strip()
        try:
            return float(entrada)      # conseguiu converter?
        except ValueError:
            print("Não é um número válido. Tente novamente.")
```

**Padrão `while True` + `try/except`:** a repetição indefinida só termina quando `float(entrada)` funciona; se falhar, o laço continua pedindo. Esse padrão é super comum em programas reais.

---

### `main.py` — a interface no terminal

Este arquivo **não calcula nada**. Ele:
1. mostra o menu;
2. lê as escolhas do usuário;
3. chama as funções de `calculadora/`;
4. imprime os resultados;
5. captura os erros e os mostra de forma amigável.

Um bom exemplo (o laço principal):

```python
while True:
    print(MENU_PRINCIPAL)
    escolha = ler_escolha(...)
    if escolha == "1":
        opcoes_basico("+")
    elif escolha == "5":
        opcoes_potencia()
    ...
    elif escolha == "12":
        break
```

A lógica de "mostrar um menu e repetir até o usuário sair" é um padrão chamado **menu loop**, presente em quase todos os programas de terminal.

---

## 4. A versão web — FastAPI + navegador

A AriCalc também roda no navegador. E aqui está a parte mais bonita do projeto:

> **Nenhuma linha do motor (`calculadora/`) foi alterada para a web existir.**

O mesmo `soma()`, `divisao()`, `Historico` e `Memoria` são reutilizados. Apenas a **interface mudou**: em vez de menu de terminal, agora temos um servidor web com uma página.

### `servidor.py` — a API

O servidor usa o **FastAPI**, um framework web para Python. A função dele é escutar pedidos HTTP e responder com JSON:

```
Navegador ──POST /api/calcular──► servidor.py ──► calculadora/ (motor)
   ▲                                   │
   └───────── JSON { resultado } ◄─────┘
```

**Exemplo real** — quando o aluno clica em `5 + 3 =`, o navegador envia:

```json
{ "operacao": "soma", "a": 5, "b": 3 }
```

O servidor recebe, chama `soma(5, 3)` e devolve:

```json
{ "resultado": 8.0, "expressao": "5.0 + 3.0" }
```

**Conceitos novos que a web introduz:**

| Conceito | O que é | Onde aparece |
|---|---|---|
| **Rota / endpoint** | um "endereço" que responde a um pedido | `@app.post("/api/calcular")` |
| **Método HTTP** | o verbo do pedido (GET lê, POST cria, DELETE apaga) | `POST`, `GET`, `DELETE` |
| **JSON** | formato de texto que vira objeto nas duas pontas | corpo da requisição e resposta |
| **Pydantic** | ferramenta que valida o JSON antes de chegar ao motor | `RequisicaoCalculo` |
| **Status code** | número que diz se deu certo (200) ou errado (400/500) | `HTTPException(status_code=400)` |
| **Servidor** | programa que fica rodando esperando pedidos | `uvicorn servidor:app` |

**Por que os erros voltam como 400?**

Quando o motor levanta `ZeroDivisionError` (divisão por zero), o servidor o "engole" e responde:

```json
{ "detail": "Não é possível dividir por zero." }
```

com status 400 (pedido inválido). O navegador recebe, mostra essa mensagem na tela, e o programa **continua vivo**. Descobrir esse padrão — *nunca deixar a exceção quebrar o servidor* — é uma habilidade central de backend.

**Dica:** acesse `http://127.0.0.1:8000/docs` e clique em um endpoint. O FastAPI gera sozinho uma documentação interativa onde você pode testar os pedidos sem escrever nada!

### `static/` — o navegador (HTML, CSS, JS)

A página que o navegador abre é feita de três arquivos, na pasta `static/`:

| Arquivo | Papel | Analogia com a AriCalc |
|---|---|---|
| `index.html` | a **estrutura** (botões, tela, painéis) | "o esqueleto" |
| `style.css` | o **visual** (cores, tamanhos) | "a roupa e a maquiagem" |
| `script.js` | a **lógica** do clique | "o maestro" (mas sem calcular!) |

O `script.js` é o mais interessante: ele mantém o estado (qual número está sendo digitado, qual operador foi escolhido) e, quando o usuário aperta `=`, **monta o JSON e chama o servidor**:

```javascript
const corpo = { operacao, a, b };

const resposta = await fetch("/api/calcular", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(corpo),
});
const dados = await resposta.json();
```

Perceba que **nem HTML nem JS sabem somar**. Eles sabem apenas pedir a soma. A matemática é responsabilidade de quem a entende bem ocupar-se: o motor Python.

### A grande ideia: mesmo motor, duas interfaces

```
        ┌─────────────────────────────────────────┐
        │            calculadora/ (motor)         │
        │   soma(), divisao(), Historico, Memoria │
        └──────────────┬────────────┬────────────┘
                       │            │
        (terminal)     │            │     (web)
                       ▼            ▼
                ┌────────────┐  ┌──────────────────────────┐
                │   main.py  │  │  servidor.py + static/   │
                │  menu CLI  │  │  FastAPI + HTML/CSS/JS   │
                └────────────┘  └──────────────────────────┘
```

Se amanhã você quiser uma interface com janelas (ex.: Tkinter) ou um app de celular, o motor continua igual. Essa separação é o que empresas chamam de **arquitetura de software**: escolher *onde* cada responsabilidade mora.

---

## 5. Testes unitários

Na pasta `tests/` existem 34 testes que verificam o motor automaticamente:

```python
def test_divisao_por_zero_lanca_erro(self):
    with self.assertRaises(ZeroDivisionError):
        divisao(10, 0)
```

Esse teste diz: "Não importa onde o código corra — se `divisao(10, 0)` não levantar `ZeroDivisionError`, está quebrado."

**Por que testar o motor e não a interface?** Porque a interface é difícil de automatizar (exige digitação). O motor é previsível: dados os mesmos números, devolve o mesmo resultado. Testá-lo isoladamente é a essência dos **testes unitários**.

Para rodar:
```bash
python -m unittest tests.test_operacoes -v
```

---

## 6. Exercícios propostos

Para praticar (sugestões em ordem de dificuldade):

1. **Fácil:** altere a formatação da lista do histórico para mostrar em ordem inversa (do mais recente ao mais antigo).
2. **Fácil:** no menu, adicione um atalho para encerrar digitando `s` ou `fim`, além do número 12.
3. **Fácil (web):** adicione um botão `C` duplo ("limpou duas vezes = limpar memória também").
4. **Médio:** crie uma operação nova, `potencia_de_10`, que calcula `10 ** x`, e adicione ao menu (terminal, API e botão web).
5. **Médio:** modifique `Historico.salvar` para salvar em um arquivo com o nome composto pela data atual (ex.: `historico-2026-09-15.json`).
6. **Médio (web):** no `script.js`, faça o histórico mostrar também a data/hora de cada operação (o campo `momento` já vem do servidor).
7. **Difícil:** adicione uma operação de porcentagem (`5 % de 200 = 10`) com testes unitários.
8. **Difícil (web):** crie um novo endpoint `POST /api/historico/{id}/reutilizar` que devolve a expressão daquele registro, e um botão na lista com "usar de novo".
9. **Desafio:** escreva testes automáticos para a API usando o `TestClient` do FastAPI (sobre HTTP, e não unitários diretos).

> **Dica de ouro:** sempre que encontrar um problema, tente **dividi-lo em pedaços menores**. Cada função pequena e bem documentada — como as deste projeto — é muito mais fácil de entender, testar e corrigir do que um programa gigante monolítico.