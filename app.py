from openai import OpenAI
import time
import sqlite3
from flask import Flask, request, render_template, redirect, url_for
from PyPDF2 import PdfReader
from config import API_KEY

#Inicialização do flask
app = Flask(__name__)

# Configuração do cliente OpenAI
client = OpenAI(api_key = API_KEY)


#'0052211-83.2020.8.06.0029 ' 61 páginas
#'0022701-03.2020.8.05.0110' 94 páginas
#'0001242-24.2021.8.05.0137' 120 páginas

def gerar_resposta_consolidada(objetivo_final):
    resposta = ''
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{objetivo_final}, considerando \n\n {resumo_partes} em no máximo {tamanho_resposta}. Imprima o resultado em HTML"}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            resposta += chunk.choices[0].delta.content
    return resposta

def get_name_from_page_count(filename):
    if filename == "94pag.pdf":
        return "0022701-03.2020.8.05.0110"
    elif filename == "61pag.pdf":
        return "0052211-83.2020.8.06.0029 "
    elif filename == "120pag.pdf":
        return "0001242-24.2021.8.05.0137"
    else:
        return "Processo inválido"

num_processo = ""


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global num_processo

    if 'pdf_file' not in request.files:
        return "Nenhum arquivo PDF enviado"

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "Nenhum arquivo selecionado"

    if pdf_file:
        filename = pdf_file.filename
        num_processo = get_name_from_page_count(filename)

        pergunta = "Como as leis aplicáveis influenciam o caso?"
        tamanho_resposta = "300"

        # Conectar ao banco de dados
        conn = sqlite3.connect('C:/Users/raul.oliveira.miran1/Downloads/database/dados_processos2.db')
        cursor = conn.cursor()

        # Definir o número do processo desejado
        numero_processo_desejado = f"{num_processo}"

        # Executar a consulta SQL para selecionar os dados da linha com o número do processo desejado
        cursor.execute('''
            SELECT * FROM Processos WHERE numero_processo = ?
        ''', (numero_processo_desejado,))

        # Recuperar o resultado da consulta
        resultado = cursor.fetchone()

        # Fechar a conexão
        conn.close()

        # Atribuir os valores a outras variáveis
        numero_processo, autor, juiz, reu, advogado_autor, advogado_reu, valor_indenizacao, juizado, comarca, vara, data_abertura, data_atualizacao, status, sintese, acuracia, resumo_partes = resultado
        
        juizQuantidade = "N/A"
        clienteQuantidade = "N/A"
        tribunalQuantidade = "N/A"
        produto = "Empréstimo"
        tipoReclamacao = "Contratação indevida"

        if num_processo == "0052211-83.2020.8.06.0029 ":

            juiz = "Karla Cristina de Oliveira"
            autor = "FRANCISCA ROMANA BEZERRA DA COSTA"
            reu = "BANCO BRADESCO S.A"
            advogado_autor = "Rangel Pereira Ribeiro"
            advogado_reu = "FRANCISCO SAMPAIO DE MENEZES JUNIOR"
            valor_indenizacao = "23.054,24"
            juizado = "TJCE"
            comarca = "TJCE"
            data_abertura = "14/12/2020"
            data_atualizacao = "10/11/2021"
        elif num_processo == "0022701-03.2020.8.05.0110":
            juiz = "Alexandre Lopes"
            autor = "Delci Rodrigues Santana Silva"
            reu = "Banco Bradesco Financiamento S A"
            advogado_autor = "Davi Olinto Soares"
            advogado_reu = "Fernando Augusto de Faria Corbo"
            valor_indenizacao = "15.000,00"
            juizado = "TJBA"
            comarca = "TJBA"
            data_abertura = "03/12/2020"
            data_atualizacao = "28/07/2023"
        else:  
            juiz = "BERNARDO MARIO DANTAS LUBAMBO"
            autor = "JORGE PEREIRA DA SILVA"
            reu = "BANCO BRADESCO S.A"
            advogado_autor = "EMILIO LOPES DA CRUZ"
            advogado_reu = "FERNANDO AUGUSTO DE FARIA CORBO"
            valor_indenizacao = "9.583,04"
            juizado = "TJBA"
            comarca = "TJBA"
            data_abertura = "12/04/2021"
            data_atualizacao = "18/04/2023"

        return render_template('index.html', numero_processo=numero_processo, autor=autor, reu=reu, advogado_autor=advogado_autor, advogado_reu=advogado_reu, data_abertura=data_abertura, data_atualizacao=data_atualizacao, acuracia=acuracia, status=status, valor_indenizacao=valor_indenizacao, vara=vara, comarca=comarca, juizado=juizado, juiz=juiz, juizQuantidade=juizQuantidade, clienteQuantidade=clienteQuantidade, tribunalQuantidade=tribunalQuantidade, resumo_partes=resumo_partes, produto=produto, tipoReclamacao=tipoReclamacao)

@app.route('/resumo', methods=['GET', 'POST'])
def resumo():

    global num_processo

    pergunta = "Faça um resumo"
    tamanho_resposta = "300"

    # Conectar ao banco de dados
    conn = sqlite3.connect('C:/Users/raul.oliveira.miran1/Downloads/database/dados_processos.db')
    cursor = conn.cursor()

    # Definir o número do processo desejado
    numero_processo_desejado = f"{num_processo}"

    # Executar a consulta SQL para selecionar os dados da linha com o número do processo desejado
    cursor.execute('''
        SELECT * FROM Processos WHERE numero_processo = ?
    ''', (numero_processo_desejado,))

    # Recuperar o resultado da consulta
    resultado = cursor.fetchone()

    # Fechar a conexão
    conn.close()

    def gerar_resposta_consolidada(objetivo_final):
        resposta = ''
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"{objetivo_final}, considerando \n\n {resumo_partes} em no máximo {tamanho_resposta}. Imprima o resultado em HTML"}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                resposta += chunk.choices[0].delta.content
        return resposta

    # Atribuir os valores a outras variáveis
    numero_processo, autor, juiz, reu, advogado_autor, advogado_reu, valor_indenizacao, juizado, comarca, vara, data_abertura, data_atualizacao, status, sintese, acuracia, resumo_partes = resultado
    
    resumo= gerar_resposta_consolidada(pergunta)

    juizQuantidade = "N/A"
    clienteQuantidade = "N/A"
    tribunalQuantidade = "N/A"
    produto = "Empréstimo"
    tipoReclamacao = "Contratação indevida"

    if num_processo == "0052211-83.2020.8.06.0029 ":

        juiz = "Karla Cristina de Oliveira"
        autor = "FRANCISCA ROMANA BEZERRA DA COSTA"
        reu = "BANCO BRADESCO S.A"
        advogado_autor = "Rangel Pereira Ribeiro"
        advogado_reu = "FRANCISCO SAMPAIO DE MENEZES JUNIOR"
        valor_indenizacao = "23.054,24"
        juizado = "TJCE"
        comarca = "TJCE"
        data_abertura = "14/12/2020"
        data_atualizacao = "10/11/2021"
    elif num_processo == "0022701-03.2020.8.05.0110":
        juiz = "Alexandre Lopes"
        autor = "Delci Rodrigues Santana Silva"
        reu = "Banco Bradesco Financiamento S A"
        advogado_autor = "Davi Olinto Soares"
        advogado_reu = "Fernando Augusto de Faria Corbo"
        valor_indenizacao = "15.000,00"
        juizado = "TJBA"
        comarca = "TJBA"
        data_abertura = "03/12/2020"
        data_atualizacao = "28/07/2023"
    else:  
        juiz = "BERNARDO MARIO DANTAS LUBAMBO"
        autor = "JORGE PEREIRA DA SILVA"
        reu = "BANCO BRADESCO S.A"
        advogado_autor = "EMILIO LOPES DA CRUZ"
        advogado_reu = "FERNANDO AUGUSTO DE FARIA CORBO"
        valor_indenizacao = "9.583,04"
        juizado = "TJBA"
        comarca = "TJBA"
        data_abertura = "12/04/2021"
        data_atualizacao = "18/04/2023"

    return render_template('index.html', numero_processo=numero_processo, autor=autor, reu=reu, advogado_autor=advogado_autor, advogado_reu=advogado_reu, data_abertura=data_abertura, data_atualizacao=data_atualizacao, acuracia=acuracia, status=status, valor_indenizacao=valor_indenizacao, vara=vara, comarca=comarca, juizado=juizado, juiz=juiz, juizQuantidade=juizQuantidade, clienteQuantidade=clienteQuantidade, tribunalQuantidade=tribunalQuantidade, resumo_partes=resumo_partes, produto=produto, tipoReclamacao=tipoReclamacao, resumo=resumo)

@app.route('/pergunta', methods=['GET', 'POST'])
def pergunta():

    global num_processo

    perguntaUser =""

    perguntaUser = request.form['texto']
    
    pergunta = perguntaUser
    tamanho_resposta = "300"

    # Conectar ao banco de dados
    conn = sqlite3.connect('C:/Users/raul.oliveira.miran1/Downloads/database/dados_processos.db')
    cursor = conn.cursor()

    # Definir o número do processo desejado
    numero_processo_desejado = f"{num_processo}"

    # Executar a consulta SQL para selecionar os dados da linha com o número do processo desejado
    cursor.execute('''
        SELECT * FROM Processos WHERE numero_processo = ?
    ''', (numero_processo_desejado,))

    # Recuperar o resultado da consulta
    resultado = cursor.fetchone()

    # Fechar a conexão
    conn.close()

    def gerar_resposta_consolidada(objetivo_final):
        resposta = ''
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f" Imprima o resultado em HTML, {objetivo_final}, considerando \n\n {resumo_partes} em no máximo {tamanho_resposta}."}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                resposta += chunk.choices[0].delta.content
        return resposta

    # Atribuir os valores a outras variáveis
    numero_processo, autor, juiz, reu, advogado_autor, advogado_reu, valor_indenizacao, juizado, comarca, vara, data_abertura, data_atualizacao, status, sintese, acuracia, resumo_partes = resultado
    
    resumo= gerar_resposta_consolidada(pergunta)

    print(pergunta)
    print(resumo)

    juizQuantidade = "N/A"
    clienteQuantidade = "N/A"
    tribunalQuantidade = "N/A"
    produto = "Empréstimo"
    tipoReclamacao = "Contratação indevida"

    if num_processo == "0052211-83.2020.8.06.0029 ":

        juiz = "Karla Cristina de Oliveira"
        autor = "FRANCISCA ROMANA BEZERRA DA COSTA"
        reu = "BANCO BRADESCO S.A"
        advogado_autor = "Rangel Pereira Ribeiro"
        advogado_reu = "FRANCISCO SAMPAIO DE MENEZES JUNIOR"
        valor_indenizacao = "23.054,24"
        juizado = "TJCE"
        comarca = "TJCE"
        data_abertura = "14/12/2020"
        data_atualizacao = "10/11/2021"
    elif num_processo == "0022701-03.2020.8.05.0110":
        juiz = "Alexandre Lopes"
        autor = "Delci Rodrigues Santana Silva"
        reu = "Banco Bradesco Financiamento S A"
        advogado_autor = "Davi Olinto Soares"
        advogado_reu = "Fernando Augusto de Faria Corbo"
        valor_indenizacao = "15.000,00"
        juizado = "TJBA"
        comarca = "TJBA"
        data_abertura = "03/12/2020"
        data_atualizacao = "28/07/2023"
    else:  
        juiz = "BERNARDO MARIO DANTAS LUBAMBO"
        autor = "JORGE PEREIRA DA SILVA"
        reu = "BANCO BRADESCO S.A"
        advogado_autor = "EMILIO LOPES DA CRUZ"
        advogado_reu = "FERNANDO AUGUSTO DE FARIA CORBO"
        valor_indenizacao = "9.583,04"
        juizado = "TJBA"
        comarca = "TJBA"
        data_abertura = "12/04/2021"
        data_atualizacao = "18/04/2023"

    return render_template('index.html', numero_processo=numero_processo, autor=autor, reu=reu, advogado_autor=advogado_autor, advogado_reu=advogado_reu, data_abertura=data_abertura, data_atualizacao=data_atualizacao, acuracia=acuracia, status=status, valor_indenizacao=valor_indenizacao, vara=vara, comarca=comarca, juizado=juizado, juiz=juiz, juizQuantidade=juizQuantidade, clienteQuantidade=clienteQuantidade, tribunalQuantidade=tribunalQuantidade, resumo_partes=resumo_partes, produto=produto, tipoReclamacao=tipoReclamacao, resumo=resumo, pergunta=pergunta)
if __name__ == '__main__':
    app.run(debug=True)

inicio_resumo = time.time()

resumo= gerar_resposta_consolidada(pergunta)
print(resumo)