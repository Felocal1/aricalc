"""
Módulo memoria — a memória da calculadora (MC, MR, M+, M-, MS).

Da mesma forma que uma calculadora física tem botões de memória,
a AriCalc também guarda um único valor "guardado". As operações
disponíveis são:

    MC  (Memory Clear)   -> limpa a memória.
    MR  (Memory Recall)  -> mostra o valor guardado.
    M+  (Memory Add)     -> somar o resultado atual ao valor guardado.
    M-  (Memory Subtract)-> subtrair o resultado atual do valor guardado.
    MS  (Memory Store)   -> guardar o valor atual substituindo o anterior.

Isso é uma excelente forma de aprender sobre ESTADO em programação:
a memória é um valor que "vive" dentro do objeto e muda ao longo
do tempo conforme chamamos seus métodos.
"""


class Memoria:
    """
    Classe que representa a memória da calculadora.

    Atributos
    ---------
    valor : float | None — o número guardado (None quando vazia).

    Métodos
    -------
    limpar()   — apaga o valor da memória (MC).
    recall()   — devolve o valor guardado (MR).
    somar(x)   — soma x ao valor guardado (M+).
    subtrair(x)— subtrai x do valor guardado (M-).
    armazenar(x)— guarda x substituindo o valor anterior (MS).
    tem_valor()— diz se há algo guardado.
    """

    def __init__(self):
        """Cria a memória vazia (nenhum valor guardado)."""
        self.valor = None

    def tem_valor(self) -> bool:
        """
        Informa se há um valor guardado na memória.

        Retorno
        -------
        bool — True se houver valor guardado; False se estiver vazia.
        """
        return self.valor is not None

    def limpar(self) -> None:
        """
        Apaga o valor guardado (MC — Memory Clear).
        Funciona mesmo que a memória já esteja vazia.
        """
        self.valor = None

    def recall(self) -> float:
        """
        Devolve o valor guardado (MR — Memory Recall).

        Retorno
        -------
        float — o valor que está na memória.

        Exceções
        --------
        ValueError — se a memória estiver vazia (não há o que mostrar).
        """
        if self.valor is None:
            raise ValueError("A memória está vazia. Nada para recuperar.")
        return self.valor

    def armazenar(self, x: float) -> None:
        """
        Guarda um novo valor, substituindo o anterior (MS — Memory Store).

        Parâmetros
        ----------
        x : float — o valor a ser guardado.
        """
        self.valor = float(x)

    def somar(self, x: float) -> float:
        """
        Soma um valor ao que já está na memória (M+ — Memory Add).

        Se a memória estiver vazia, o comportamento é o de uma
        calculadora real: começa do zero (0 + x = x).

        Parâmetros
        ----------
        x : float — o valor a somar.

        Retorno
        -------
        float — o novo valor da memória após a soma.
        """
        base = self.valor if self.valor is not None else 0.0
        self.valor = base + float(x)
        return self.valor

    def subtrair(self, x: float) -> float:
        """
        Subtrai um valor do que está na memória (M- — Memory Subtract).

        Parâmetros
        ----------
        x : float — o valor a subtrair.

        Retorno
        -------
        float — o novo valor da memória após a subtração.
        """
        base = self.valor if self.valor is not None else 0.0
        self.valor = base - float(x)
        return self.valor