/* =====================================================================
   script.js — A lógica do frontend da AriCalc web.

   IMPORTANTE: este arquivo NÃO faz nenhuma conta de verdade. Ele apenas:
     1. entende o que o usuário clica (números, operadores, funções);
     2. monta o JSON da operação;
     3. envia para o servidor:  POST /api/calcular
     4. recebe o JSON com o resultado e mostra na tela.

   A matemática vive toda no servidor (calculadora/operacoes.py).

   FUNÇÃO fetch(): é a forma nativa do JavaScript de fazer pedidos
   HTTP. O padrão usado aqui:

       const resposta = await fetch(url, { method, headers, body });
       const dados = await resposta.json();

   - await "espera" o servidor responder;
   - resposta.ok indica se deu certo (200) ou errado (400/500);
   - dados é o JSON devolvido transformado em objeto JS.
   ===================================================================== */

// ---------------------------------------------------------------------
// Estado da calculadora (o que está "acontecendo agora" na tela)
// ---------------------------------------------------------------------
let acumulador = null;      // primeiro número guardado (ex.: 5 em "5 + 3")
let operadorPendente = null; // qual operação escolhemos (ex.: "soma")
let digitoAtual = "0";      // o número que está sendo digitado agora
let iniciarNovoNumero = true; // se o próximo dígito começa número novo

// Referências aos elementos da página (HTML)
const telaExpressao = document.getElementById("tela-expressao");
const telaResultado = document.getElementById("tela-resultado");
const aviso = document.getElementById("aviso");
const valorMemoria = document.getElementById("valor-memoria");
const listaHistorico = document.getElementById("lista-historico");

// ---------------------------------------------------------------------
// Utilitários de exibição
// ---------------------------------------------------------------------

/** Formata um número para mostrar bonito (sem "10.0000000001"). */
function formatar(valor) {
    const numero = Number(valor);
    if (Number.isInteger(numero)) return String(numero);
    // Limite de dígitos significativos para evitar ruído de ponto flutuante.
    return parseFloat(numero.toPrecision(12)).toString();
}

/** Mostra o número digitado na "tela" da calculadora. */
function atualizarTela() {
    telaResultado.textContent = digitoAtual;
}

/** Mostra uma mensagem de erro/aviso na área própria. */
function mostrarAviso(mensagem) {
    aviso.textContent = mensagem;
}

/** Faz o fetch e converte a resposta; lança erro se vier erro do servidor. */
async function pedir(url, metodo, corpo) {
    const opcoes = {
        method: metodo,
        headers: corpo ? { "Content-Type": "application/json" } : {},
    };
    if (corpo !== undefined) {
        opcoes.body = JSON.stringify(corpo);
    }

    const resposta = await fetch(url, opcoes);
    const dados = await resposta.json();

    if (!resposta.ok) {
        // Servidor mandou erro com mensagem clara (ex.: divisão por zero).
        throw new Error(dados.detail || "Erro desconhecido no servidor.");
    }
    return dados;
}

// ---------------------------------------------------------------------
// Operações de memória (MC, MR, M+, M-, MS)
// ---------------------------------------------------------------------

/** Atualiza a faixa "Memória: ..." no topo da calculadora. */
async function atualizarFaixaMemoria() {
    const dados = await pedir("/api/memoria", "GET");
    valorMemoria.textContent = dados.valor === null ? "(vazia)" : formatar(dados.valor);
}

/** Trata um clique em um botão de memória (MC, MR, M+, M-, MS). */
async function acaoMemoria(qual) {
    mostrarAviso("");
    const valor = parseFloat(digitoAtual);

    try {
        if (qual === "MC") {
            await pedir("/api/memoria", "DELETE");
        } else if (qual === "MR") {
            const dados = await pedir("/api/memoria", "GET");
            if (dados.valor === null) {
                mostrarAviso("Memória vazia.");
                return;
            }
            digitoAtual = formatar(dados.valor);
            iniciarNovoNumero = true;
            atualizarTela();
        } else if (qual === "MS") {
            await pedir("/api/memoria/armazenar", "POST", { valor });
        } else if (qual === "M+") {
            await pedir("/api/memoria/somar", "POST", { valor });
        } else if (qual === "M-") {
            await pedir("/api/memoria/subtrair", "POST", { valor });
        }
        await atualizarFaixaMemoria();
    } catch (erro) {
        mostrarAviso(erro.message);
    }
}

// ---------------------------------------------------------------------
// Ações que não são números nem operadores (C, ⌫, =)
// ---------------------------------------------------------------------

/** Apaga tudo e recomeça (botão C). */
function limparTudo() {
    acumulador = null;
    operadorPendente = null;
    digitoAtual = "0";
    iniciarNovoNumero = true;
    telaExpressao.textContent = "\u00A0";
    mostrarAviso("");
    atualizarTela();
}

/** Apaga o último dígito digitado (botão ⌫). */
function apagarDigito() {
    if (iniciarNovoNumero) return; // nada a apagar
    digitoAtual = digitoAtual.length > 1 ? digitoAtual.slice(0, -1) : "0";
    if (digitoAtual === "-") digitoAtual = "0";
    atualizarTela();
}

// ---------------------------------------------------------------------
// Personagem — reação do robô contador
// ---------------------------------------------------------------------

/** Faz o robô dar um pulinho de comemoração quando um cálculo termina. */
function comemorar() {
    const personagem = document.getElementById("personagem");
    // Remove a classe para poder reiniciar a animação do zero.
    personagem.classList.remove("comemora");
    void personagem.offsetWidth;      // "força" o navegador a reaplicar
    personagem.classList.add("comemora");
}

/** Envia o cálculo para o servidor e mostra o resultado. */
async function calcular(a, b, operacao) {
    mostrarAviso("");

    // O corpo da requisição:
    const corpo = { operacao, a, b };

    try {
        const dados = await pedir("/api/calcular", "POST", corpo);

        // Sucesso → mostra o resultado e a expressão correspondente.
        digitoAtual = formatar(dados.resultado);
        telaExpressao.textContent = dados.expressao + " =";
        iniciarNovoNumero = true;
        atualizarTela();
        comemorar();                    // robô comemora!
        await carregarHistorico();      // o servidor registrou a operação
        await atualizarFaixaMemoria();  // nada muda aqui, mas é gratuito
    } catch (erro) {
        mostrarAviso(erro.message);
    }
}

/** Botão "=" — executa a operação pendente (se houver). */
async function apertarIgual() {
    if (operadorPendente === null) {
        // Não há operação esperando; não faz nada (ou histórico).
        return;
    }

    const a = acumulador;
    const b = parseFloat(digitoAtual);
    const operacao = operadorPendente;

    acumulador = null;
    operadorPendente = null;

    await calcular(a, b, operacao);
}

// ---------------------------------------------------------------------
// Dígitos, operadores e funções científicas
// ---------------------------------------------------------------------

/** Clique em um dígito (0-9) ou na vírgula/ponto decimal. */
function apertarNumero(numero) {
    mostrarAviso("");

    if (iniciarNovoNumero) {
        digitoAtual = numero === "." ? "0." : numero;
        iniciarNovoNumero = false;
    } else {
        // Evita dois pontos decimais no mesmo número.
        if (numero === "." && digitoAtual.includes(".")) return;
        if (digitoAtual === "0" && numero !== ".") {
            digitoAtual = numero; // "0" + "7" vira "7", não "07"
        } else {
            digitoAtual += numero;
        }
    }
    atualizarTela();
}

/** Clique em um operador (+, −, ×, ÷, xʸ). */
async function apertarOperador(operacao) {
    mostrarAviso("");

    if (operadorPendente !== null) {
        // Já havia um operador esperando. Para permitir encadeamento
        // (2 + 3 + 4 = ...), primeiro terminamos a conta pendente.
        await apertarIgual();
    }

    acumulador = parseFloat(digitoAtual);
    operadorPendente = operacao;

    // Mostra na expressão: "5 +" (o que já está guardado)
    const simbolos = {
        soma: "+", subtracao: "-", multiplicacao: "×",
        divisao: "÷", potencia: "ʸ",
    };
    telaExpressao.textContent = formatar(acumulador) + " " + (simbolos[operacao] || operacao) + " ";
    iniciarNovoNumero = true;
    atualizarTela();
}

/** Clique em uma função científica que aplica ao número da tela. */
async function apertarCientifica(funcao) {
    mostrarAviso("");
    const x = parseFloat(digitoAtual);
    const corpo = { operacao: funcao, x };

    if (funcao === "raiz_n_esima") {
        // "ⁿ√x" precisa do índice n. Pedimos ao usuário (simples e funcional).
        const n = prompt("Qual o índice da raiz? (ex.: 2 = quadrada, 3 = cúbica)");
        if (n === null) return; // cancelou
        corpo.n = parseInt(n, 10);
        if (isNaN(corpo.n)) {
            mostrarAviso("Índice inválido.");
            return;
        }
    }

    try {
        const dados = await pedir("/api/calcular", "POST", corpo);
        digitoAtual = formatar(dados.resultado);
        telaExpressao.textContent = dados.expressao + " =";
        iniciarNovoNumero = true;
        atualizarTela();
        comemorar();                    // robô comemora!
        await carregarHistorico();
    } catch (erro) {
        mostrarAviso(erro.message);
    }
}

// ---------------------------------------------------------------------
// Histórico
// ---------------------------------------------------------------------

/** Busca e desenha o histórico vindo do servidor. */
async function carregarHistorico() {
    const dados = await pedir("/api/historico", "GET");
    const registros = dados.registros;

    listaHistorico.innerHTML = ""; // limpa a lista atual

    if (registros.length === 0) {
        const item = document.createElement("li");
        item.className = "vazio";
        item.textContent = "Nenhuma operação ainda.";
        listaHistorico.appendChild(item);
        return;
    }

    // Mais recente primeiro (invertido) para leitura rápida.
    for (const registro of registros.slice().reverse()) {
        const item = document.createElement("li");

        const expressao = document.createElement("span");
        expressao.className = "expressao";
        expressao.textContent = registro.expressao;

        const resultado = document.createElement("span");
        resultado.className = "resultado";
        resultado.textContent = "= " + formatar(registro.resultado);

        item.appendChild(expressao);
        item.appendChild(resultado);
        listaHistorico.appendChild(item);
    }
}

// ---------------------------------------------------------------------
// Ligando todos os eventos (o "maestro" da página)
// ---------------------------------------------------------------------
document.addEventListener("click", (evento) => {
    const botao = evento.target.closest("button");
    if (!botao) return;

    // Cada botão tem um data-* que diz o que ele faz.
    if (botao.dataset.numero !== undefined) apertarNumero(botao.dataset.numero);
    else if (botao.dataset.operador) apertarOperador(botao.dataset.operador);
    else if (botao.dataset.funcao) apertarCientifica(botao.dataset.funcao);
    else if (botao.dataset.memoria) acaoMemoria(botao.dataset.memoria);
    else if (botao.dataset.acao === "C") limparTudo();
    else if (botao.dataset.acao === "backspace") apagarDigito();
    else if (botao.dataset.acao === "igual") apertarIgual();
});

document.getElementById("limpar-historico").addEventListener("click", async () => {
    await pedir("/api/historico", "DELETE");
    await carregarHistorico();
});

// ---------------------------------------------------------------------
// Suporte ao teclado (didático e útil!)
// ---------------------------------------------------------------------
document.addEventListener("keydown", (evento) => {
    const tecla = evento.key;
    const mapa = { "+": "soma", "-": "subtracao", "*": "multiplicacao", "/": "divisao" };

    if (/^[0-9]$/.test(tecla) || tecla === ".") apertarNumero(tecla);
    else if (mapa[tecla]) apertarOperador(mapa[tecla]);
    else if (tecla === "Enter" || tecla === "=") apertarIgual();
    else if (tecla === "Backspace") apagarDigito();
    else if (tecla === "Escape") limparTudo();
});

// ---------------------------------------------------------------------
// Inicialização: estado inicial da tela + busca do histórico/memória
// ---------------------------------------------------------------------
atualizarTela();
carregarHistorico();
atualizarFaixaMemoria();