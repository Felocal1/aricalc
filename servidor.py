"""
servidor.py — A AriCalc na WEB (interface no navegador).

Este arquivo cria um servidor web usando o FastAPI. Ele faz a ponte
entre o navegador (frontend) e o motor matemático (backend):

    Navegador ──HTTP──► servidor.py ──► calculadora/ (backend)
        ▲                                    │
        └────────────── JSON ◄───────────────┘

O detalhe mais importante para aprender:

    NENHUMA matemática acontece aqui! O servidor apenas:
      1. recebe o pedido do navegador (qual operação e os números);
      2. chama a função certa do pacote calculadora;
      3. devolve o resultado em formato JSON.

Como rodar LOCALMENTE (na sua máquina):
    .venv\\Scripts\\python -m uvicorn servidor:app --reload
    Depois abra no navegador:  http://127.0.0.1:8000

Como rodar publicado (ex.: Render.com):
    O servidor é iniciado pelo comando definido no render.yaml. Ele
    lê a variável de ambiente PORT (definida pela própria plataforma)
    e escuta em "0.0.0.0" (todas as interfaces) — veja o bloco
    execucao_principal() no fim do arquivo.

A FastAPI ainda gera uma documentação interativa da API em:
    http://127.0.0.1:8000/docs
"""

import os
import sys

# ---------------------------------------------------------------------------
# Codificação UTF-8 (mesma lição do main.py, agora para o servidor)
# ---------------------------------------------------------------------------
utf8 = getattr(sys.stdout, "reconfigure", None)
if utf8 is not None and getattr(sys.stdout, "encoding", "").lower() != "utf-8":
    utf8(encoding="utf-8")

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from calculadora import (
    soma,
    subtracao,
    multiplicacao,
    divisao,
    potencia,
    raiz_quadrada,
    raiz_n_esima,
    logaritmo,
    seno,
    cosseno,
    tangente,
    Historico,
    Memoria,
)

# ---------------------------------------------------------------------------
# Constantes globais (compartilhadas entre requisições)
# ---------------------------------------------------------------------------
historico = Historico()   # o mesmo histórico do modo terminal (mesmo .json)
memoria = Memoria()       # a memória (recriada a cada reinício do servidor)

# ---------------------------------------------------------------------------
# MODELOS — descrevem o formato dos dados que o navegador envia
# ---------------------------------------------------------------------------
# O Pydantic usa type hints (mesmo conceito que já usamos) para
# VALIDAR automaticamente o que chega. Se o navegador mandar texto
# onde esperamos número, o FastAPI rejeita antes de tocar no motor.


class RequisicaoCalculo(BaseModel):
    """Corpo de um cálculo genérico.

    Nem todo cálculo usa os mesmos campos:
        soma(a, b)          → usa "a" e "b"
        raiz_quadrada(x)    → usa "x"
        raiz_n_esima(x, n)  → usa "x" e "n"
        logaritmo(x, base)  → usa "x" e "base" (base opcional)
        seno(graus)         → usa "graus" (informamos em graus!)

    Campos que não se aplicam ficam como None (vazio).
    """

    operacao: str                  # ex.: "soma", "raiz_quadrada", "seno"...
    a: Optional[float] = None
    b: Optional[float] = None
    x: Optional[float] = None
    n: Optional[int] = None
    base: Optional[float] = None
    graus: Optional[float] = None


class ValorMemoria(BaseModel):
    """Corpo das operações de memória (MS, M+, M-)."""

    valor: float


# ---------------------------------------------------------------------------
# Criação da aplicação FastAPI
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AriCalc API",
    description="Calculadora educacional (mesmo motor do terminal, agora na web).",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# MÉTODO PRINCIPAL — o "mapeador" de operações
# ---------------------------------------------------------------------------
def executar_calculo(req: RequisicaoCalculo):
    """
    Recebe uma requisição e chama a função certa do motor.

    Esta função devolve um dicionário contendo:
        "resultado" : o número calculado.
        "expressao" : texto descrevendo a conta (para o histórico).

    Se a operação for impossível (ex.: divisor zero), levanta
    HTTPException com status 400 (pedido inválido) e a mensagem
    clara vinda do próprio motor.
    """
    try:
        if req.operacao == "soma":
            resultado = soma(req.a, req.b)
            expressao = f"{req.a} + {req.b}"

        elif req.operacao == "subtracao":
            resultado = subtracao(req.a, req.b)
            expressao = f"{req.a} - {req.b}"

        elif req.operacao == "multiplicacao":
            resultado = multiplicacao(req.a, req.b)
            expressao = f"{req.a} * {req.b}"

        elif req.operacao == "divisao":
            resultado = divisao(req.a, req.b)
            expressao = f"{req.a} / {req.b}"

        elif req.operacao == "potencia":
            resultado = potencia(req.a, req.b)
            expressao = f"{req.a} ** {req.b}"

        elif req.operacao == "raiz_quadrada":
            resultado = raiz_quadrada(req.x)
            expressao = f"√({req.x})"

        elif req.operacao == "raiz_n_esima":
            resultado = raiz_n_esima(req.x, req.n)
            expressao = f"{req.n}√({req.x})"

        elif req.operacao == "logaritmo":
            base = req.base if req.base is not None else 10
            resultado = logaritmo(req.x, base)
            expressao = f"log({req.x}) na base {base}"

        elif req.operacao == "seno":
            # O motor trabalha em RADIANOS; o usuário digita GRAUS.
            # A conversão mora aqui no servidor (assim o motor não muda).
            rad = req.graus * (3.141592653589793 / 180)
            resultado = seno(rad)
            expressao = f"sen({req.graus}°)"

        elif req.operacao == "cosseno":
            rad = req.graus * (3.141592653589793 / 180)
            resultado = cosseno(rad)
            expressao = f"cos({req.graus}°)"

        elif req.operacao == "tangente":
            rad = req.graus * (3.141592653589793 / 180)
            resultado = tangente(rad)
            expressao = f"tan({req.graus}°)"

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Operação '{req.operacao}' desconhecida.",
            )

        return {"resultado": resultado, "expressao": expressao}

    except ZeroDivisionError as erro:
        # Divisão por zero → 400 com mensagem amigável.
        raise HTTPException(status_code=400, detail=str(erro))

    except ValueError as erro:
        # Raiz de negativo, log de zero, etc. → 400 com mensagem clara.
        raise HTTPException(status_code=400, detail=str(erro))

    except TypeError as erro:
        # Índice de raiz não inteiro, por exemplo.
        raise HTTPException(status_code=400, detail=str(erro))


# ---------------------------------------------------------------------------
# ROTAS DA API
# ---------------------------------------------------------------------------


@app.post("/api/calcular")
def calcular(req: RequisicaoCalculo):
    """
    Executa um cálculo e o registra no histórico.

    Corpo do pedido (JSON):
    {
        "operacao": "soma",
        "a": 5,
        "b": 3
    }

    Resposta (JSON):
    {
        "resultado": 8,
        "expressao": "5 + 3"
    }
    """
    matematica = executar_calculo(req)
    # Sucesso? Registra no histórico e devolve o resultado.
    historico.adicionar(matematica["expressao"], matematica["resultado"])
    return matematica


@app.get("/api/historico")
def obter_historico():
    """Devolve a lista completa de operações já feitas."""
    return {"registros": historico.listar()}


@app.delete("/api/historico")
def limpar_historico():
    """Apaga todos os registros do histórico."""
    historico.limpar()
    return {"ok": True}


@app.get("/api/memoria")
def obter_memoria():
    """Devolve o valor guardado na memória (ou null se vazia)."""
    if memoria.tem_valor():
        return {"valor": memoria.recall()}
    return {"valor": None}


@app.post("/api/memoria/armazenar")
def memoria_armazenar(body: ValorMemoria):
    """MS — guarda um valor na memória, substituindo o anterior."""
    memoria.armazenar(body.valor)
    return {"valor": memoria.recall()}


@app.post("/api/memoria/somar")
def memoria_somar(body: ValorMemoria):
    """M+ — soma um valor ao que está na memória."""
    novo = memoria.somar(body.valor)
    return {"valor": novo}


@app.post("/api/memoria/subtrair")
def memoria_subtrair(body: ValorMemoria):
    """M- — subtrai um valor do que está na memória."""
    novo = memoria.subtrair(body.valor)
    return {"valor": novo}


@app.delete("/api/memoria")
def memoria_limpar():
    """MC — apaga o valor da memória."""
    memoria.limpar()
    return {"valor": None}


# ---------------------------------------------------------------------------
# FRONTEND — servir as páginas (HTML, CSS, JavaScript)
# ---------------------------------------------------------------------------
# O navegador acessa "http://127.0.0.1:8000/" e recebe o index.html.
# Os arquivos estáticos ficam na pasta static/.
app.mount("/", StaticFiles(directory="static", html=True), name="static")


# ---------------------------------------------------------------------------
# PONTO DE EXECUÇÃO DIRETA
# ---------------------------------------------------------------------------
# Permite rodar com:  .venv\Scripts\python servidor.py
#
# Lição de publicação:
#   Em produção, quem informa a porta é a PLATAFORMA (Render, por
#   exemplo) através da variável de ambiente PORT. E para o mundo
#   acessar, o servidor precisa escutar em 0.0.0.0 (todas as
#   interfaces), não só em 127.0.0.1 (a própria máquina).
def selecionar_porta() -> int:
    """
    Devolve a porta em que o servidor deve escutar.

    Prioridade:
      1. A variável de ambiente PORT (definida pela plataforma de
         hospedagem em produção);
      2. 8000 (padrão local de desenvolvimento).

    Retorno
    -------
    int — número da porta.
    """
    try:
        return int(os.environ.get("PORT", "8000"))
    except ValueError:
        # Se algo estranho vier, não quebramos o servidor.
        return 8000


def execucao_principal() -> None:
    """Inicia o servidor com host e porta certos para o ambiente."""
    import uvicorn

    porta = selecionar_porta()
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"

    print(f"AriCalc web em: http://{host}:{porta}")
    uvicorn.run(app, host=host, port=porta)


if __name__ == "__main__":
    execucao_principal()