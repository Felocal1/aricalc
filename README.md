# ARI CALC — Calculadora Educacional em Python

Uma calculadora completa construída como projeto de aprendizagem, separando o motor matemático (backend) da interface com o usuário (frontend).

**O mesmo backend roda em duas interfaces: terminal e web.**

---

## Como rodar

### 1. Modo terminal

```bash
python main.py
```

### 2. Modo web (navegador)

A primeira vez é preciso instalar as dependências no ambiente virtual:

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Depois, ligue o servidor:

```bash
.\.venv\Scripts\python -m uvicorn servidor:app --reload
```

Abra no navegador: **http://127.0.0.1:8000**

Experimente também a documentação interativa da API em **http://127.0.0.1:8000/docs**

## Como rodar os testes

```bash
python -m unittest tests.test_operacoes -v
```

---

## Estrutura do projeto

```
AriCalc/
│
├── main.py                    # Interface 1: menu interativo no terminal
├── servidor.py                # Interface 2: API web (FastAPI)
├── static/                    # Interface 2: páginas do navegador
│   ├── index.html             #   estrutura da página
│   ├── style.css              #   visual
│   └── script.js              #   lógica do navegador (chama a API)
│
├── calculadora/               # BACKEND — a lógica que funciona sozinha
│   ├── __init__.py
│   ├── operacoes.py           # Motor matemático (básico + científico)
│   ├── historico.py           # Salva operações em arquivo JSON
│   ├── memoria.py             # Memória (MC, MR, M+, M-, MS)
│   └── utils.py               # Validação de entrada (usada no terminal)
│
├── tests/
│   └── test_operacoes.py      # 34 testes unitários do motor
│
├── requirements.txt           # Dependências da versão web
└── docs/
    └── APRENDENDO.md          # Manual passo a passo com explicações
```

## Funcionalidades

| Categoria | O que faz |
|---|---|
| **Operações básicas** | +, −, ×, ÷ |
| **Científicas** | potência, √, ⁿ√, log, sen, cos, tan |
| **Histórico** | registra todas as contas, salva em `historico.json`, disponível no terminal e na web |
| **Memória** | MC (limpar), MR (recuperar), M+ (somar), M- (subtrair), MS (guardar) |

## Conceitos ensinados

- Separar backend (motor) de frontend (interface) e **reutilizar o mesmo motor em duas interfaces**
- Funções com docstrings (documentação inline)
- Tratamento de exceções com `try/except`
- Persistência de dados com arquivos JSON
- Testes unitários com `unittest`
- Validação de entrada do usuário
- Programação orientada a objetos (classes `Historico` e `Memoria`)
- API REST com FastAPI (rotas, JSON, validação com Pydantic)
- HTTP na web: `fetch` no JavaScript chamando os endpoints