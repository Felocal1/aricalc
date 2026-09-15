"""
Módulo historico — registro de todas as operações da AriCalc.

Toda vez que o usuário faz um cálculo, a calculadora guarda um
"registro" daquela operação (o que foi feito e o resultado).
Isso é chamado de HISTÓRICO.

Por que guardar?
    - O usuário pode consultar o que já fez;
    - O histórico fica salvo em um arquivo (historico.json),
      então sobrevive mesmo depois de fechar o programa;
    - É uma ótima oportunidade de aprender sobre PERSISTÊNCIA
      de dados: transformar objetos em texto (serialização)
      e transformar texto de volta em objetos (desserialização).

FORMATO DOS REGISTROS
---------------------
Cada registro é um dicionário com três campos:
    {
        "expressao": "5 + 3",        # o que foi digitado / descrição
        "resultado": 8,              # o número que saiu do cálculo
        "momento"  : "2026-09-15 10:30:00"   # quando aconteceu
    }

O histórico inteiro é uma lista desses registros, e essa lista é
salva no arquivo usando o formato JSON (JavaScript Object Notation),
que é um padrão simples de texto que qualquer linguagem entende.
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class Historico:
    """
    Classe responsável por guardar, exibir, limpar e persistir
    o histórico de operações.

    Atributos
    ---------
    arquivo : str — caminho do arquivo onde o histórico é salvo.
    registros : list — lista de registros (cada um é um dicionário).

    Métodos principais
    ------------------
    adicionar(expressao, resultado) — guarda uma nova operação.
    listar()                        — devolve os registros em ordem.
    limpar()                        — apaga todos os registros.
    carregar()  / salvar()          — ler e escrever o arquivo JSON.
    """

    def __init__(self, arquivo: str = "historico.json"):
        """
        Cria um objeto Historico já pronto para uso.

        O caminho do arquivo pode ser informado; se não for,
        usa "historico.json" na pasta atual. Como todos os dados
        são salvos logo no início, o histórico anterior (se houver)
        já fica disponível via self.registros.

        Parâmetros
        ----------
        arquivo : str — caminho do arquivo de histórico.
        """
        self.arquivo = arquivo
        self.registros: List[Dict] = []
        self.carregar()  # se já existir um arquivo, lê de lá

    # ------------------------------------------------------------------
    # Operações principais
    # ------------------------------------------------------------------

    def adicionar(self, expressao: str, resultado: float) -> None:
        """
        Adiciona uma nova operação ao histórico e salva no arquivo.

        Parâmetros
        ----------
        expressao : str   — descrição da operação, ex.: "5 + 3".
        resultado : float — o valor numérico obtido.
        """
        registro = {
            "expressao": expressao,
            "resultado": resultado,
            "momento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        self.registros.append(registro)
        self.salvar()

    def listar(self) -> List[Dict]:
        """
        Devolve uma cópia dos registros na ordem em que foram feitos.

        Retorno
        -------
        list — os registros do histórico.
        """
        return self.registros.copy()

    def limpar(self) -> None:
        """
        Apaga todos os registros do histórico e atualiza o arquivo.
        """
        self.registros.clear()
        self.salvar()

    # ------------------------------------------------------------------
    # Persistência (carregar e salvar em disco)
    # ------------------------------------------------------------------

    def carregar(self) -> None:
        """
        Lê o arquivo JSON e carrega os registros para a memória.

        Se o arquivo não existir (primeira execução) ou estiver
        corrompido, simplesmente começa com a lista vazia — nada
        é travado, e o usuário nem percebe.

        DICA DE APRENDIZADO:
        "carregar()" vai do DISCO para a MEMÓRIA.
        "salvar()"   vai da MEMÓRIA para o DISCO.
        """
        if not os.path.exists(self.arquivo):
            self.registros = []
            return

        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo_aberto:
                conteudo = arquivo_aberto.read()
                # Se o arquivo estiver vazio, também começamos do zero.
                self.registros = json.loads(conteudo) if conteudo else []
        except (json.JSONDecodeError, OSError):
            self.registros = []

    def salvar(self) -> None:
        """
        Escreve os registros atuais no arquivo, em formato JSON.

        Por que precisamos da codificação "utf-8" e do parâmetro
        "indent=4"?
            - utf-8 : garante que acentos e símbolos (ã, ç, á...) 
              sejam salvos corretamente em qualquer sistema;
            - indent=4 : escreve o JSON com indentação, para que
              quem abrir o arquivo no editor consiga ler.
        """
        with open(self.arquivo, "w", encoding="utf-8") as arquivo_aberto:
            json.dump(self.registros, arquivo_aberto, ensure_ascii=False, indent=4)

    def tem_registros(self) -> bool:
        """
        Informa se o histórico está vazio ou não.

        Retorno
        -------
        bool — True se houver pelo menos um registro; False caso contrário.
        """
        return len(self.registros) > 0