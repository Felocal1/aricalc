"""
Módulo operacoes — o motor matemático da AriCalc.

Este módulo é a parte mais importante da calculadora. Ele contém
todas as funções que fazem matemática de verdade. Nenhuma função
aqui imprime nada na tela: elas apenas RECEBEM números, calculam
e DEVOLVEM o resultado (ou levantam um erro com uma mensagem
clara, caso o cálculo seja impossível).

Isso é proposital! Separar o cálculo da interface permite:
    1. Testar cada função automaticamente (veja a pasta tests/);
    2. Reutilizar a mesma lógica em outros programas;
    3. Trocar a interface (termo "frontend") sem quebrar nada.

ERROS TRATADOS QUE ESTE MÓDULO TRATA:
    - ZeroDivisionError : divisão por zero (impossível na matemática)
    - ValueError        : domínio inválido (raiz de negativo, log de <= 0)
    - TypeError         : entrada que não é número (ex.: texto)
"""

import math

# ---------------------------------------------------------------------------
# OPERAÇÕES BÁSICAS
# ---------------------------------------------------------------------------


def soma(a: float, b: float) -> float:
    """
    Retorna a soma de dois números (a + b).

    Parâmetros
    ----------
    a : float — primeiro número.
    b : float — segundo número.

    Retorno
    -------
    float — o resultado de a + b.

    Exemplo
    -------
    >>> soma(2, 3)
    5
    """
    return a + b


def subtracao(a: float, b: float) -> float:
    """
    Retorna a diferença entre dois números (a - b).

    Parâmetros
    ----------
    a : float — número do qual se subtrai (minuendo).
    b : float — número que será subtraído (subtraendo).

    Retorno
    -------
    float — o resultado de a - b.

    Exemplo
    -------
    >>> subtracao(10, 4)
    6
    """
    return a - b


def multiplicacao(a: float, b: float) -> float:
    """
    Retorna o produto de dois números (a * b).

    Parâmetros
    ----------
    a : float — primeiro fator.
    b : float — segundo fator.

    Retorno
    -------
    float — o resultado de a * b.

    Exemplo
    -------
    >>> multiplicacao(7, 3)
    21
    """
    return a * b


def divisao(a: float, b: float) -> float:
    """
    Retorna a divisão de dois números (a / b).

    IMPORTANTE: dividir por zero é impossível na matemática.
    Se o divisor for zero, este método levanta uma exceção
    ZeroDivisionError com uma mensagem amigável, em vez de
    deixar o programa quebrar sozinho.

    Parâmetros
    ----------
    a : float — dividendo (o número que será dividido).
    b : float — divisor (pelo que vamos dividir).

    Retorno
    -------
    float — o quociente de a / b.

    Exceções
    --------
    ZeroDivisionError — se b for igual a zero.

    Exemplo
    -------
    >>> divisao(10, 2)
    5.0

    >>> divisao(10, 0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: Não é possível dividir por zero.
    """
    if b == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    return a / b


# ---------------------------------------------------------------------------
# OPERAÇÕES CIENTÍFICAS
# ---------------------------------------------------------------------------


def potencia(base: float, expoente: float) -> float:
    """
    Retorna a base elevada ao expoente (base ** expoente).

    Parâmetros
    ----------
    base     : float — o número que será multiplicado por si mesmo.
    expoente : float — quantas vezes a base será multiplicada.

    Retorno
    -------
    float — o resultado de base ** expoente.

    Exemplo
    -------
    >>> potencia(2, 10)
    1024
    >>> potencia(5, 2)
    25
    """
    return base**expoente


def raiz_quadrada(x: float) -> float:
    """
    Retorna a raiz quadrada de x (√x).

    A raiz quadrada de um número N é o número R tal que R * R = N.
    Só existe raiz quadrada REAL de números NÃO negativos.

    Parâmetros
    ----------
    x : float — número do qual se quer a raiz quadrada.

    Retorno
    -------
    float — o valor de √x.

    Exceções
    --------
    ValueError — se x for negativo (não existe raiz real de negativo).

    Exemplo
    -------
    >>> raiz_quadrada(16)
    4.0
    """
    if x < 0:
        raise ValueError("Não existe raiz quadrada de número negativo (no domínio dos reais).")
    return math.sqrt(x)


def raiz_n_esima(x: float, n: int) -> float:
    """
    Retorna a raiz n-ésima de x (ⁿ√x).

    A raiz n-ésima de x é o número R tal que R ** n = x.

    Parâmetros
    ----------
    x : float — radicando (número que está dentro da raiz).
    n : int   — índice da raiz (ex.: 2 = quadrada, 3 = cúbica).

    Retorno
    -------
    float — o valor de ⁿ√x.

    Exceções
    --------
    ValueError — se o índice n for zero (raiz de índice zero é indefinida),
                 ou se x for negativo e o índice for par
                 (não existe raiz real).
    TypeError   — se n não for um inteiro.

    Exemplo
    -------
    >>> raiz_n_esima(8, 3)
    2.0
    >>> raiz_n_esima(81, 4)
    3.0
    """
    if not isinstance(n, int):
        raise TypeError("O índice da raiz (n) deve ser um número inteiro.")
    if n == 0:
        raise ValueError("A raiz de índice zero não está definida.")
    if x < 0 and n % 2 == 0:
        raise ValueError("Não existe raiz de índice par para número negativo.")
    return x ** (1 / n)


def logaritmo(x: float, base: float = 10) -> float:
    """
    Retorna o logaritmo de x em uma dada base.

    O logaritmo de x na base b é o número L tal que b ** L = x.
    Só existe logaritmo de números POSITIVOS, e a base precisa
    ser positiva e diferente de 1.

    Parâmetros
    ----------
    x    : float — o logaritmando (número do qual se quer o log).
    base : float — a base do logaritmo (padrão: 10).

    Retorno
    -------
    float — o valor de log base(x).

    Exceções
    --------
    ValueError — se x <= 0 (não existe log de zero/negativo),
                 se base <= 0, ou se base == 1.

    Exemplo
    -------
    >>> logaritmo(1000)            # log na base 10
    3.0
    >>> logaritmo(8, 2)            # log de 8 na base 2
    3.0
    """
    if x <= 0:
        raise ValueError("Não existe logaritmo de zero ou número negativo.")
    if base <= 0:
        raise ValueError("A base do logaritmo deve ser um número positivo.")
    if base == 1:
        raise ValueError("A base do logaritmo não pode ser 1.")
    return math.log(x, base)


def seno(x: float) -> float:
    """
    Retorna o seno de um ângulo dado em RADIANOS.

    Lembrete: o Python trabalha com radianos, não graus.
    Para converter graus em radianos, multiplique por math.pi / 180.

    Parâmetros
    ----------
    x : float — ângulo em radianos.

    Retorno
    -------
    float — o seno de x (sempre entre -1 e 1).

    Exemplo
    -------
    >>> seno(0)
    0.0
    >>> seno(math.pi / 2)
    1.0
    """
    return math.sin(x)


def cosseno(x: float) -> float:
    """
    Retorna o cosseno de um ângulo dado em RADIANOS.

    Parâmetros
    ----------
    x : float — ângulo em radianos.

    Retorno
    -------
    float — o cosseno de x (sempre entre -1 e 1).

    Exemplo
    -------
    >>> cosseno(0)
    1.0
    >>> cosseno(math.pi)
    -1.0
    """
    return math.cos(x)


def tangente(x: float) -> float:
    """
    Retorna a tangente de um ângulo dado em RADIANOS.

    A tangente é o quociente entre seno e cosseno:
        tan(x) = sen(x) / cos(x)
    Por isso ela não existe para ângulos onde cos(x) == 0
    (ex.: 90° = π/2 radianos). Nesse caso, o Python retorna
    um valor muito grande (resultado da divisão por quase-zero).

    Parâmetros
    ----------
    x : float — ângulo em radianos.

    Retorno
    -------
    float — a tangente de x.

    Exemplo
    -------
    >>> tangente(0)
    0.0
    >>> tangente(math.pi / 4)
    1.0
    """
    return math.tan(x)