"""
main.py — Ponto de entrada da AriCalc.

Este arquivo é a INTERFACE (o "frontend") da calculadora. Ele usa
as funções do pacote calculadora para conversar com o usuário.

Arquitetura (resumo):
    main.py  <--->  calculadora (backend)
    - menu, impressão,  - cálculo em si
      leitura de dados    - histórico, memória

Por que dividir assim? Imagine que amanhã você queira colocar
a AriCalc dentro de um site ou de uma janela gráfica: você apenas
troca o main.py; todo o motor continua funcionando sem mudanças.

Como rodar:
    python main.py
"""

# ---------------------------------------------------------------------------
# Lição de codificação de caracteres (encoding)
#
# O console do Windows, por padrão, usa a tabela de caracteres cp1252,
# que NÃO possui símbolos como √ (raiz) e ⁿ (n-ésima). Se não fizermos
# nada, o programa quebra ao exibir o menu. A solução é pedir ao Python
# para usar a codificação universal UTF-8 na saída (stdout).
# ---------------------------------------------------------------------------

import sys

utf8 = getattr(sys.stdout, "reconfigure", None)
if utf8 is not None and getattr(sys.stdout, "encoding", "").lower() != "utf-8":
    utf8(encoding="utf-8")  # força a saída aceitar todos os caracteres

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
from calculadora.utils import (
    ler_numero,
    ler_numero_int,
    ler_escolha,
    formatar_numero,
)

# ---------------------------------------------------------------------------
# Constantes do menu
# ---------------------------------------------------------------------------

MENU_PRINCIPAL = """
==========================================
            ARI CALC — Calculadora
==========================================
  [1] Soma            (+)
  [2] Subtração       (-)
  [3] Multiplicação   (*)
  [4] Divisão         (/)
  [5] Potência        (**)
  [6] Raiz quadrada   (√)
  [7] Raiz n-ésima    (ⁿ√)
  [8] Logaritmo       (log)
  [9] Trigonometria   (sen / cos / tan)
 [10] Histórico
 [11] Memória
 [12] Sair
------------------------------------------
"""

MENU_TRIGONOMETRIA = """
  [1] Seno      [2] Cosseno      [3] Tangente
"""

MENU_MEMORIA = """
  M+  -> somar o resultado atual à memória
  M-  -> subtrair o resultado atual da memória
  MS  -> guardar o resultado atual na memória
  MR  -> mostrar o valor guardado
  MC  -> limpar a memória
"""


def pausar():
    """Pausa o programa até o usuário apertar ENTER (didático)."""
    input("\nPressione ENTER para continuar...")


def opcoes_basico(operador: str) -> None:
    """
    Executa uma operação básica (+ , - , * , /) entre dois números.

    O parâmetro `operador` indica a conta a fazer. Assim, o menu
    principal chama esta função já sabendo a operação escolhida
    (ex.: opção 1 chama com "+", opção 4 chama com "/").

    Parâmetros
    ----------
    operador : str — um dos símbolos "+", "-", "*" ou "/".

    Se a operação for impossível (ex.: divisão por zero),
    a exceção ZeroDivisionError é capturada e mostrada na tela.
    """
    a = ler_numero("Digite o primeiro número: ")
    b = ler_numero("Digite o segundo número: ")

    if operador == "+":
        resultado = soma(a, b)
    elif operador == "-":
        resultado = subtracao(a, b)
    elif operador == "*":
        resultado = multiplicacao(a, b)
    else:  # operador == "/"
        try:
            resultado = divisao(a, b)
        except ZeroDivisionError as erro:
            print(f"Erro: {erro}")
            pausar()
            return

    print(f"\n  {formatar_numero(a)} {operador} {formatar_numero(b)} = {formatar_numero(resultado)}")
    historico.adicionar(f"{formatar_numero(a)} {operador} {formatar_numero(b)}", resultado)
    pausar()


def opcoes_potencia() -> None:
    """Executa a operação de potência (base ** expoente)."""
    base = ler_numero("Digite a base: ")
    expoente = ler_numero("Digite o expoente: ")
    resultado = potencia(base, expoente)
    print(f"\n  {formatar_numero(base)} ** {formatar_numero(expoente)} = {formatar_numero(resultado)}")
    historico.adicionar(f"{formatar_numero(base)} ** {formatar_numero(expoente)}", resultado)
    pausar()


def opcoes_raiz() -> None:
    """
    Executa a raiz quadrada de um número.

    Trata o erro de raiz de número negativo, mostrando uma
    mensagem amigável em vez de deixar o programa quebrar.
    """
    x = ler_numero("Digite o número: ")
    try:
        resultado = raiz_quadrada(x)
        print(f"\n  √{formatar_numero(x)} = {formatar_numero(resultado)}")
    except ValueError as erro:
        print(f"Erro: {erro}")
        pausar()
        return

    historico.adicionar(f"√{formatar_numero(x)}", resultado)
    pausar()


def opcoes_raiz_n() -> None:
    """Executa a raiz n-ésima de um número."""
    x = ler_numero("Digite o radicando (número): ")
    n = ler_numero_int("Digite o índice (inteiro, ex.: 2, 3, 4...): ")
    try:
        resultado = raiz_n_esima(x, n)
        print(f"\n  {n}√{formatar_numero(x)} = {formatar_numero(resultado)}")
    except (ValueError, TypeError) as erro:
        print(f"Erro: {erro}")
        pausar()
        return

    historico.adicionar(f"{n}√{formatar_numero(x)}", resultado)
    pausar()


def opcoes_log() -> None:
    """Executa o logaritmo de um número em uma base."""
    x = ler_numero("Digite o logaritmando (x): ")
    base = ler_numero("Digite a base (padrão é 10; digite 10 se não souber): ")

    try:
        resultado = logaritmo(x, base)
        print(f"\n  log{formatar_numero(base)}({formatar_numero(x)}) = {formatar_numero(resultado)}")
    except ValueError as erro:
        print(f"Erro: {erro}")
        pausar()
        return

    historico.adicionar(f"log{formatar_numero(base)}({formatar_numero(x)})", resultado)
    pausar()


def opcoes_trigonometria() -> None:
    """Executa as funções trigonométricas (seno, cosseno, tangente).

    OBSERVAÇÃO IMPORTANTE PARA O ALUNO:
    O Python calcula trigonometria com ângulos em RADIANOS.
    Para converter graus -> radianos, usa-se a fórmula:
        radianos = graus * (π / 180)
    """

    print(MENU_TRIGONOMETRIA)
    escolha = ler_escolha("Escolha a função (1, 2 ou 3): ", ["1", "2", "3"])

    graus = ler_numero("Digite o ângulo em GRAUS: ")
    radianos = graus * (3.141592653589793 / 180)  # π com precisão didática

    if escolha == "1":
        resultado = seno(radianos)
        nome = "sen"
    elif escolha == "2":
        resultado = cosseno(radianos)
        nome = "cos"
    else:
        resultado = tangente(radianos)
        nome = "tan"

    print(f"\n  {nome}({formatar_numero(graus)}°) = {formatar_numero(resultado)}")
    historico.adicionar(f"{nome}({formatar_numero(graus)}°)", resultado)
    pausar()


def opcoes_historico() -> None:
    """Mostra o histórico de operações em ordem cronológica."""
    if not historico.tem_registros():
        print("\nO histórico está vazio. Faça alguns cálculos primeiro!")
        pausar()
        return

    print("\n" + "=" * 50)
    print("            HISTÓRICO DE OPERAÇÕES")
    print("=" * 50)
    for i, registro in enumerate(historico.listar(), start=1):
        print(f"{i:>3}. {registro['expressao']:<25} = {registro['resultado']:<15} ({registro['momento']})")
    print("=" * 50)

    opcao = ler_escolha(
        "\n[V] Ver um resultado\n[C] Limpar histórico\n[Q] Voltar\n\nEscolha: ",
        ["v", "V", "c", "C", "q", "Q"],
    )

    if opcao in ("c", "C"):
        historico.limpar()
        print("\nHistórico limpo!")
    elif opcao in ("v", "V"):
        buscar = ler_numero_int("Digite o número do registro para abrir seu resultado: ")
        registros = historico.listar()
        if 1 <= buscar <= len(registros):
            registro = registros[buscar - 1]
            print(f"  Você quer ver o resultado de: {registro['expressao']}")
            ver_resultado = ler_escolha("Usar esse resultado como base para uma nova conta? (s/n): ", ["s", "S", "n", "N"])
            if ver_resultado in ("s", "S"):
                print(f"  O resultado é {formatar_numero(registro['resultado'])}. Anote este valor!")
                pausar()
                return
        else:
            print("Registro não encontrado.")
    pausar()


def opcoes_memoria() -> None:
    """Menu da memória da calculadora (MC, MR, M+, M-, MS)."""
    while True:
        print(MENU_MEMORIA)
        if memoria.tem_valor():
            print(f"  Memória atual: {formatar_numero(memoria.recall())}")
        else:
            print("  Memória atual: (vazia)")

        opcao = ler_escolha("\nEscolha uma opção (MC, MR, M+, M-, MS) ou [Q] para voltar: ")

        # Normaliza a entrada para letras maiúsculas: "m+" vira "M+",
        # assim aceitamos tanto minúsculas quanto maiúsculas.
        opcao = opcao.upper()

        if opcao == "MC":
            memoria.limpar()
            print("\nMemória limpa (MC).")
        elif opcao == "MR":
            try:
                print(f"\nO valor na memória é: {formatar_numero(memoria.recall())}")
            except ValueError as erro:
                print(f"Erro: {erro}")
        elif opcao == "M+":
            valor = ler_numero("Quanto somar à memória? ")
            novo = memoria.somar(valor)
            print(f"\nMemória agora é: {formatar_numero(novo)}")
        elif opcao == "M-":
            valor = ler_numero("Quanto subtrair da memória? ")
            novo = memoria.subtrair(valor)
            print(f"\nMemória agora é: {formatar_numero(novo)}")
        elif opcao == "MS":
            valor = ler_numero("Qual valor guardar na memória? ")
            memoria.armazenar(valor)
            print(f"\nValor {formatar_numero(valor)} guardado na memória.")
        elif opcao == "Q":
            break
        else:
            print(f"Opção desconhecida: {opcao!r}")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

historico = Historico()  # cria (ou carrega) o histórico
memoria = Memoria()      # cria a memória (começa vazia)

if __name__ == "__main__":
    print("\nBem-vindo à ARI CALC — sua calculadora educacional em Python!")

    while True:
        print(MENU_PRINCIPAL)
        escolha = ler_escolha("Escolha uma opção (1 a 12): ", [str(i) for i in range(1, 13)])

        if escolha == "1":
            opcoes_basico("+")
        elif escolha == "2":
            opcoes_basico("-")
        elif escolha == "3":
            opcoes_basico("*")
        elif escolha == "4":
            opcoes_basico("/")
        elif escolha == "5":
            opcoes_potencia()
        elif escolha == "6":
            opcoes_raiz()
        elif escolha == "7":
            opcoes_raiz_n()
        elif escolha == "8":
            opcoes_log()
        elif escolha == "9":
            opcoes_trigonometria()
        elif escolha == "10":
            opcoes_historico()
        elif escolha == "11":
            opcoes_memoria()
        else:  # escolha == "12"
            print("\nObrigado por usar a ARI CALC! Até a próxima.")
            break