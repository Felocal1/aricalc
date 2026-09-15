"""
Testes do motor matemático (calculadora.operacoes).

Para rodar, na pasta do projeto digite:

    python -m pytest tests/ -v

ou, se preferir testar sem pytest:

    python tests/test_operacoes.py

O objetivo é verificar automaticamente que cada função do
motor responde corretamente para entradas válidas E que
levanta os erros certos para entradas impossíveis.
"""

import math

# Importação local (funciona tanto com pytest quanto rodando este
# arquivo diretamente).
try:
    from ..calculadora.operacoes import (
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
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from calculadora.operacoes import (
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

import unittest


def quase_igual(a: float, b: float, tolerancia: float = 1e-9) -> bool:
    """
    Compara dois números de ponto flutuante com tolerância.

    Números com vírgula no computador podem ter pequenas diferenças
    de precisão (ex.: 0.1 + 0.2 = 0.30000000000000004). Esta função
    ajuda a comparar dizendo "são iguais se a diferença for mínima".
    """
    return abs(a - b) < tolerancia


class TesteOperacoesBasicas(unittest.TestCase):
    """Testa +, -, *, /."""

    def test_soma_positivos(self):
        self.assertEqual(soma(2, 3), 5)

    def test_soma_negativos(self):
        self.assertEqual(soma(-5, -5), -10)

    def test_soma_zeros(self):
        self.assertEqual(soma(0, 0), 0)

    def test_subtracao(self):
        self.assertEqual(subtracao(10, 4), 6)

    def test_subtracao_resultado_negativo(self):
        self.assertEqual(subtracao(4, 10), -6)

    def test_multiplicacao(self):
        self.assertEqual(multiplicacao(7, 3), 21)

    def test_multiplicacao_por_zero(self):
        self.assertEqual(multiplicacao(123, 0), 0)

    def test_divisao_exata(self):
        self.assertEqual(divisao(10, 2), 5)

    def test_divisao_nao_exata(self):
        self.assertAlmostEqual(divisao(1, 3), 0.3333333333333333)

    def test_divisao_por_zero_lanca_erro(self):
        with self.assertRaises(ZeroDivisionError):
            divisao(10, 0)


class TesteOperacoesCientificas(unittest.TestCase):
    """Testa potência, raízes, log e trigonometria."""

    def test_potencia_simples(self):
        self.assertEqual(potencia(2, 10), 1024)

    def test_potencia_expoente_zero(self):
        self.assertEqual(potencia(5, 0), 1)

    def test_potencia_expoente_fracionario(self):
        self.assertEqual(potencia(4, 0.5), 2.0)

    def test_raiz_quadrada_perfeita(self):
        self.assertEqual(raiz_quadrada(16), 4.0)

    def test_raiz_quadrada_zero(self):
        self.assertEqual(raiz_quadrada(0), 0.0)

    def test_raiz_quadrada_negativa_lanca_erro(self):
        with self.assertRaises(ValueError):
            raiz_quadrada(-4)

    def test_raiz_cubica(self):
        self.assertEqual(raiz_n_esima(8, 3), 2.0)

    def test_raiz_quarta(self):
        self.assertEqual(raiz_n_esima(81, 4), 3.0)

    def test_raiz_indice_zero_lanca_erro(self):
        with self.assertRaises(ValueError):
            raiz_n_esima(8, 0)

    def test_raiz_indice_nao_inteiro_lanca_erro(self):
        with self.assertRaises(TypeError):
            raiz_n_esima(8, 2.5)

    def test_raiz_par_negativo_lanca_erro(self):
        with self.assertRaises(ValueError):
            raiz_n_esima(-8, 2)

    def test_log_base_10(self):
        self.assertAlmostEqual(logaritmo(1000), 3.0)

    def test_log_base_2(self):
        self.assertEqual(logaritmo(8, 2), 3.0)

    def test_log_de_zero_lanca_erro(self):
        with self.assertRaises(ValueError):
            logaritmo(0)

    def test_log_negativo_lanca_erro(self):
        with self.assertRaises(ValueError):
            logaritmo(-5)

    def test_log_base_1_lanca_erro(self):
        with self.assertRaises(ValueError):
            logaritmo(10, 1)

    def test_seno_zero(self):
        self.assertEqual(seno(0), 0.0)

    def test_seno_90_graus(self):
        self.assertAlmostEqual(seno(math.pi / 2), 1.0)

    def test_cosseno_zero(self):
        self.assertEqual(cosseno(0), 1.0)

    def test_cosseno_180_graus(self):
        self.assertAlmostEqual(cosseno(math.pi), -1.0)

    def test_tangente_zero(self):
        self.assertEqual(tangente(0), 0.0)

    def test_tangente_45_graus(self):
        self.assertAlmostEqual(tangente(math.pi / 4), 1.0)


class TestePrecisao(unittest.TestCase):
    """Verifica alguns resultados conhecidos da matemática."""

    def test_pitagoras_3_4_5(self):
        """hipotenusa de triângulo 3-4-5 usando raiz quadrada."""
        hip = raiz_quadrada(potencia(3, 2) + potencia(4, 2))
        self.assertAlmostEqual(hip, 5.0)

    def test_soma_de_fracoes(self):
        """0.1 + 0.2 deve ser (aproximadamente) 0.3."""
        self.assertTrue(quase_igual(soma(0.1, 0.2), 0.3))


if __name__ == "__main__":
    unittest.main()