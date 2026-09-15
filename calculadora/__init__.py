"""
Pacote calculadora — o "cérebro" (backend) da AriCalc.

Este pacote contém toda a lógica da calculadora, separada da
interface com o usuário. Isso é chamado de "separação de
responsabilidades":

    - operacoes  -> o motor matemático (somar, dividir, raiz, ...)
    - historico  -> registro das operações feitas
    - memoria    -> a memória da calculadora (M+, M-, MR, ...)
    - utils      -> utilitários de validação e leitura de dados

A interface (main.py) apenas pergunta ao usuário o que ele quer
fazer e usa essas funções para executar. Ela NUNCA calcula por
conta própria.
"""

from .operacoes import (
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
)
from .historico import Historico
from .memoria import Memoria
from .utils import ler_numero, ler_operador

__all__ = [
    "soma",
    "subtracao",
    "multiplicacao",
    "divisao",
    "potencia",
    "raiz_quadrada",
    "raiz_n_esima",
    "logaritmo",
    "seno",
    "cosseno",
    "tangente",
    "Historico",
    "Memoria",
    "ler_numero",
    "ler_operador",
]

__version__ = "1.0.0"