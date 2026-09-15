# ARI CALC — Calculadora Educacional em Python

Uma calculadora completa construída como projeto de aprendizagem, separando o motor matemático (backend) da interface com o usuário (frontend).

**O mesmo backend roda em duas interfaces: terminal e web.**

---

## Como rodar

### 1. Modo terminal

```bash
python main.py
```

### 2. Modo web (navegador — local)

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

A documentação interativa da API fica em **http://127.0.0.1:8000/docs**

### 3. Publicar na web (Render.com)

1. Acesse [render.com](https://render.com) e faça login (conta gratuita).
2. Clique em **"New +"** → **"Blueprint"**.
3. Conecte a conta GitHub e selecione o repositório **aricalc**.
4. O Render detecta o arquivo `render.yaml` e cria tudo automaticamente.
5. Aguarde o primeiro deploy (1~2 min). A URL pública será algo como `https://aricalc.onrender.com`.

> **Nota:** no plano gratuito, o serviço dorme após 15 minutos sem tráfego; na primeira visita ele leva ~30s para "acordar". O histórico de operações é volátil (reinicia a cada deploy).

## Como rodar os testes

```bash
python -m unittest tests.test_operacoes -v
```

---

## Repositório

**GitHub:** https://github.com/Felocal1/aricalc

```
AriCalc/
│
├── main.py                    # Interface 1: menu interativo no terminal
├── servidor.py                # Interface 2: API web (FastAPI)
├── render.yaml                # Receita de publicação no Render.com
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