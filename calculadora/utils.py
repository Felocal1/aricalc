"""
Módulo utils — utilitários de leitura e validação de dados.

Este módulo concentra as funções que "conversam" com quem está
usando o programa. São elas que leem o que o usuário digita,
validam se faz sentido e, se não fizer, pedem para digitar de novo.

Por que colocar isso em um módulo separado?
    - O main.py fica mais limpo (só usa as funções);
    - Qualquer mudança na forma de pedir dados é feita aqui;
    - Ensina o conceito de ENTRADA VALIDADA: nunca confiar
      cegamente no que o usuário digita.
"""

from typing import Optional


def ler_numero(mensagem: str) -> float:
    """
    Lê um número digitado pelo usuário no terminal.

    Se o usuário digitar algo que não é número (letras, símbolos,
    texto vazio), o programa NÃO quebra: exibe uma mensagem clara
    e pede o número novamente.

    Parâmetros
    ----------
    mensagem : str — texto exibido antes de ler o número.

    Retorno
    -------
    float — o número digitado, já convertido para float.
    """
    while True:
        entrada = input(mensagem).strip()
        # A trilha: remover espaços em branco antes/depois
        # e tentar converter para float.
        try:
            return float(entrada)
        except ValueError:
            print(f"'{entrada}' não é um número válido. Tente novamente.")

def ler_numero_int(mensagem: str) -> int:
    """
    Lê um número INTEIRO digitado pelo usuário no terminal.

    Igual a ler_numero(), mas garante que o valor convertido
    seja um int (usado, por exemplo, para o índice da raiz).

    Parâmetros
    ----------
    mensagem : str — texto exibido antes de ler o número.

    Retorno
    -------
    int — o número inteiro digitado.
    """
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print(f"'{entrada}' não é um número inteiro válido. Tente novamente.")


def ler_operador(operadores_validos: tuple[str, ...]) -> str:
    """
    Lê um símbolo de operação (+, -, *, /, ...) e VALIDA se é
    um dos permitidos.

    Parâmetros
    ----------
    operadores_validos : tuple — símbolos aceitos, ex.: ("+", "-", "*", "/").

    Retorno
    -------
    str — um dos símbolos aceitos.
    """
    while True:
        op = input("Digite o operador: ").strip()
        if op in operadores_validos:
            return op
        print(f"'{op}' não é um operador válido. Use um destes: {' '.join(operadores_validos)}")


def ler_escolha(mensagem: str, lista_de_escolhas: Optional[list] = None) -> str:
    """
    Lê a escolha do usuário em um menu e valida se está nas opções.

    Esta função é usada nos menus além da calculadora fazer cálculos
    (ex.: o menu principal, o menu de memória, etc.).

    Parâmetros
    ----------
    mensagem : str — texto exibido como pergunta.
    lista_de_escolhas : list, optional — opções aceitas. Se None,
        aceita qualquer texto (modo "digite à vontade").

    Retorno
    -------
    str — o texto digitado (sem espaços extras) quando validado.
    """
    while True:
        escolha = input(mensagem).strip()
        if lista_de_escolhas is None or escolha in lista_de_escolhas:
            return escolha
        print(
            "Opção inválida. Escolha uma destas: "
            + ", ".join(str(opcao) for opcao in lista_de_escolhas)
        )


def formatar_numero(valor: float) -> str:
    """
    Converte um número para texto de forma amigável para exibição.

    Números inteiros (10.0) são mostrados sem ".0", deixando a
    saída mais limpa: "10" em vez de "10.0".

    Parâmetros
    ----------
    valor : float — número a ser formatado.

    Retorno
    -------
    str — o número como texto (ex.: "10" ou "3.14").
    """
    if valor == int(valor):
        return str(int(valor))
    return str(valor)