from flask import Flask, render_template, request
from PyPDF2 import PdfReader

app = Flask(__name__)

#var_1
refProcesso = "1106-85.2016.8.10.0097"


#var_2 
juiz = "Des.Fed. Cecilia Mello" 
#var_3
autor = "Carlos Daniel Barcelos Ferreira"
#var_4
reu = "Banco Bradesco S/A"
#var_5 
advogadosAutor = "Roberto Borralho Junior"
#var_6
advogadosReu = "Wilson Sales Belchior"
#var_7 
indenizacao = "R$ 1.000.000,00"
#var_8
instancia = "TJMA"
#var_9
comarca = "MA"
#var_10
vara = "Matinha"
#var_11
dataAbertura = "31/10/2016"
#var_12
ultimaAtualizacao = "12/03/2024"
#var_13
situacaoFinal = "Suspenso"
#var_14
produto = "Serviços"
#var_15
juizQuantidade = "31"
#var_16
clienteQuantidade = "2"
#var_17
tribunalQuantidade = "234"
#var_18
tipoReclamacao = "DIREITO CIVIL (899) - Obrigações (7681) - Espécies de Contratos (9580) - Sistema Financeiro da Habitação (4839) - Reajuste de Prestações (4842)"



@app.route('/',  methods=['GET', 'POST'])
def index():
    numeroPaginas = 0

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file:
            pdf_reader = PdfReader(file)
            numeroPaginas = len(pdf_reader.pages)
    
    resumoProcesso = "Após uma investigação minuciosa do processo em questão, ficou evidente que o Banco Bradesco foi acionado devido a discrepâncias relacionadas às taxas de juros aplicadas no produto de financiamento de número 109292163523. Os requerentes alegam que as taxas estabelecidas foram inconsistentes com as condições originalmente acordadas, resultando em encargos financeiros excessivos e desproporcionais. A controvérsia em torno dessas taxas gerou um impasse significativo entre as partes envolvidas, levando à necessidade de uma análise mais aprofundada e, possivelmente, à resolução por meio de medidas legais ou de arbitragem. A complexidade e a sensibilidade deste assunto requerem uma abordagem cuidadosa para garantir uma resolução justa e equitativa para todas as partes afetadas."
    
    return render_template('index.html', refProcesso=refProcesso, juiz=juiz, autor=autor, reu=reu, advogadosAutor=advogadosAutor, advogadosReu=advogadosReu, indenizacao=indenizacao, instancia=instancia, comarca=comarca, vara=vara, dataAbertura=dataAbertura, ultimaAtualizacao=ultimaAtualizacao, situacaoFinal=situacaoFinal, produto=produto, juizQuantidade=juizQuantidade, clienteQuantidade=clienteQuantidade, tribunalQuantidade=tribunalQuantidade, tipoReclamacao=tipoReclamacao, resumoProcesso=resumoProcesso, numeroPaginas=numeroPaginas)

if __name__ == '__main__':
    app.run(debug=True)
