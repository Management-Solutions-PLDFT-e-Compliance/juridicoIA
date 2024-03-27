from openai import OpenAI
import time
import sqlite3
import PyPDF2
from flask import Flask, request, render_template, redirect, url_for
from PyPDF2 import PdfReader
from config import API_KEY
import spacy

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
    resumo = ""
    perguntaUser =""

    perguntaUser = request.form['texto']
    tamanho = request.form['valor']
    
    pergunta = perguntaUser
    tamanho_resposta = tamanho
    #tamanho_resposta = int(request.form['tamanho_resposta'])
    bases = 'C:/Users/raul.oliveira.miran1/Downloads/database/'
    arquivo = '61pag.pdf'
    caminho_pdf = bases + arquivo
    num_processo = "0022701-03.2020.8.05.0110"
    #tamanho_resposta_final = 100
    tamanho_resposta_final = tamanho_resposta
    #tamanho_resposta_final = request.form['tamanho_resposta']
    print(tamanho_resposta_final)
    tamanho_respostas_int = tamanho_resposta_final*2

    # Carregar o modelo de língua portuguesa do spaCy hhh
    nlp = spacy.load("pt_core_news_sm")

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

    # Funções
    def ler_pdf_e_dividir(caminho_arquivo, max_tokens=3000):
        leitor_pdf = PyPDF2.PdfReader(caminho_arquivo)
        partes = []
        texto_atual = ''
        tokens_atual = 0
        for pagina in leitor_pdf.pages:
            texto_pagina = pagina.extract_text() + "\n"
            tokens_pagina = len(texto_pagina.split())
            if tokens_atual + tokens_pagina > max_tokens:
                partes.append(texto_atual)
                texto_atual = texto_pagina
                tokens_atual = tokens_pagina
            else:
                texto_atual += texto_pagina
                tokens_atual += tokens_pagina
        if texto_atual:
            partes.append(texto_atual)
        return partes

    def analise_textos(objetive, partes):
        max_tokens_input = 3000
        max_tokens_output = 900
        resposta_final = ''
        for i, parte in enumerate(partes):  # Adiciona um loop para iterar sobre as partes e um contador (i) para acompanhar o número da parte
            print(f"Analisando parte {i+1} de {len(partes)}")  # Imprime o número da parte atual
            # Divide o texto em partes menores de max_tokens_input caracteres (para deixar uma margem de segurança)
            partes_texto = [parte[i:i+max_tokens_input] for i in range(0, len(parte), max_tokens_input)]
            for parte_texto in partes_texto:
                stream = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": f"{objetive} \n\n{parte_texto}"}],
                    stream=True,
                    max_tokens=max_tokens_output  # Define o max_tokens_output para a chamada da API
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        resposta_final += chunk.choices[0].delta.content
        return resposta_final


    def tokenizar_respostas_com_spacy(respostas):
        doc = nlp(respostas)  # Aqui, 'respostas' deve ser uma string única contendo todo o texto.
        todas_sentencas = [sent.text.strip() for sent in doc.sents]
        return todas_sentencas

    def gerar_resposta_consolidada_processamento(objetivo_final):
        resposta = ''
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"{objetivo_final}"}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                resposta += chunk.choices[0].delta.content
        return resposta



    def gerar_resposta_consolidada(objetivo_final):
        resposta = ''
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content":f"{objetivo_final}, considerando \n\n {resumo_partes} em no máximo {tamanho_resposta} caracteres. Se não for possível encontrar a resposta, retorne a palavra 'Vazio'"}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                resposta += chunk.choices[0].delta.content
        return resposta

    # Atribuir os valores a outras variáveis
    numero_processo, autor, juiz, reu, advogado_autor, advogado_reu, valor_indenizacao, juizado, comarca, vara, data_abertura, data_atualizacao, status, sintese, acuracia, resumo_partes = resultado

    if gerar_resposta_consolidada(pergunta) != "Vazio":
        print("Resultado na base de dados:\n")
        resumo = gerar_resposta_consolidada(pergunta)
        print(resumo)
    else:
        print("Resposta vazia, refazendo processamento...")
        ######## INICIO

        # Leitura e divisão do PDF em partes
        partes_pdf = ler_pdf_e_dividir(caminho_pdf)

        #########################DEFINIR A PERGUNTA 1#########################
        pergunta_int = f"{pergunta}, responda em no máximo{tamanho_respostas_int} palavras. Responda de forma curta e direta'"

        # Extração da resposta combinada do modelo generativo
        respostas_partes = analise_textos(pergunta_int, partes_pdf)

        # Tokenização do resultado
        respostas_concatenadas_1 = ''.join(respostas_partes)
        respostas_tokenizadas_1 = tokenizar_respostas_com_spacy(respostas_concatenadas_1)
        print(respostas_tokenizadas_1)
        print("\n\n\n\n\n\n")

        #DEFINIR A PERGUNTA CONSOLIDADA
        pergunta_sintese = f"{pergunta}: procurar resposta em: {', '.join(respostas_tokenizadas_1)} em no máximo {tamanho_resposta_final} palavras."

        #GERAR RESUMO

        resumo= gerar_resposta_consolidada_processamento(pergunta_sintese)
        print(resumo)
    
        print("\n\nResumo:"+resumo)

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
            juizQuantidade = "N/A"
            clienteQuantidade = "N/A"
            tribunalQuantidade = "N/A"
            produto = "Empréstimo"
            tipoReclamacao = "Contratação indevida"
                
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
            juizQuantidade = "N/A"
            clienteQuantidade = "N/A"
            tribunalQuantidade = "N/A"
            produto = "Empréstimo"
            tipoReclamacao = "Contratação indevida"

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
            juizQuantidade = "N/A"
            clienteQuantidade = "N/A"
            tribunalQuantidade = "N/A"
            produto = "Empréstimo"
            tipoReclamacao = "Contratação indevida"
    
    juizQuantidade = "N/A"
    clienteQuantidade = "N/A"
    tribunalQuantidade = "N/A"
    produto = "Empréstimo"
    tipoReclamacao = "Contratação indevida"

    return render_template('index.html', numero_processo=numero_processo, autor=autor, reu=reu, advogado_autor=advogado_autor, advogado_reu=advogado_reu, data_abertura=data_abertura, data_atualizacao=data_atualizacao, acuracia=acuracia, status=status, valor_indenizacao=valor_indenizacao, vara=vara, comarca=comarca, juizado=juizado, juiz=juiz, juizQuantidade=juizQuantidade, clienteQuantidade=clienteQuantidade, tribunalQuantidade=tribunalQuantidade, resumo_partes=resumo_partes, produto=produto, tipoReclamacao=tipoReclamacao, resumo=resumo, pergunta=pergunta)

if __name__ == '__main__':
    app.run(debug=True)

inicio_resumo = time.time()

#resumo= gerar_resposta_consolidada(pergunta)
#print(resumo)