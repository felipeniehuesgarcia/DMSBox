from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

# Comentado temporariamente para evitar erro de Google Sheets
# from google_sheets import GoogleSheetsReader

app = Flask(__name__)


# Dados simulados para teste (substitua pela integração real quando resolver o Google Sheets)
def get_mock_profissionais():
    return [
        {
            "nome": "Ana Silva",
            "nivel": "Senior",
            "valor_hora": 85.0,
            "horas_disponiveis": 160,
            "horas_mensais": [160, 140, 180, 160, 150, 170]
        },
        {
            "nome": "João Santos",
            "nivel": "Pleno",
            "valor_hora": 65.0,
            "horas_disponiveis": 180,
            "horas_mensais": [180, 160, 190, 180, 170, 180]
        },
        {
            "nome": "Maria Costa",
            "nivel": "Junior",
            "valor_hora": 45.0,
            "horas_disponiveis": 160,
            "horas_mensais": [160, 150, 170, 160, 160, 160]
        },
        {
            "nome": "Carlos Oliveira",
            "nivel": "Senior",
            "valor_hora": 90.0,
            "horas_disponiveis": 140,
            "horas_mensais": [140, 120, 150, 140, 130, 140]
        },
        {
            "nome": "Fernanda Lima",
            "nivel": "Pleno",
            "valor_hora": 70.0,
            "horas_disponiveis": 170,
            "horas_mensais": [170, 160, 180, 170, 160, 170]
        }
    ]


# Rota principal - página inicial modernizada
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dados_recorrente', methods=['GET', 'POST'])
def dados_recorrente():
    if request.method == 'POST':
        quantidade = int(request.form['quantidade'])
        inicio = request.form['inicio']
        vigencia = request.form['vigencia']

        # Usando dados simulados temporariamente
        profissionais_disponiveis = get_mock_profissionais()

        # Quando resolver o Google Sheets, descomente a linha abaixo:
        # profissionais_disponiveis = GoogleSheetsReader().profissionais_disponiveis_recorrente(
        #     datetime.strptime(inicio, "%Y-%m-%d"), int(vigencia)
        # )

        return render_template('selecionar.html',
                               quantidade=quantidade,
                               profissionais=profissionais_disponiveis,
                               inicio=inicio,
                               vigencia=vigencia)
    return render_template('dados_recorrente.html')


@app.route('/dados_avulso', methods=['GET', 'POST'])
def dados_avulso():
    if request.method == 'POST':
        data_contrato = request.form['data_contrato']
        prazo = request.form['prazo']
        qtd_profissionais = int(request.form['qtd_profissionais'])

        # Calcula meses entre contrato e prazo
        inicio = datetime.strptime(data_contrato, "%Y-%m-%d")
        fim = datetime.strptime(prazo, "%Y-%m-%d")
        total_meses = (fim.year - inicio.year) * 12 + fim.month - inicio.month + 1

        # Usando dados simulados temporariamente
        profissionais_disponiveis = get_mock_profissionais()

        # Quando resolver o Google Sheets, descomente as linhas abaixo:
        # profissionais_disponiveis = GoogleSheetsReader().profissionais_disponiveis_avulso(inicio, fim)

        return render_template('alocar_avulso.html',
                               profissionais=profissionais_disponiveis,
                               meses=total_meses,
                               qtd=qtd_profissionais)
    return render_template('dados_avulso.html')


# Rota para processar resultados
@app.route('/resultado', methods=['POST'])
def resultado():
    # Processar os dados do formulário e calcular os resultados
    form_data = dict(request.form)

    # Aqui você pode implementar a lógica de cálculo
    # Por enquanto, retorna uma página de resultado com os dados do formulário
    return render_template('resultado.html', dados=form_data)


# Rota para servir os dados dos gráficos
@app.route('/api/dashboard-data')
def dashboard_data():
    # Dados dos gráficos integrados do segundo projeto
    dashboard_data = {
        "operacional": {
            "Horas Alocadas por Projeto": [{
                "type": "bar",
                "x": ["Projeto 1", "Projeto 2", "Projeto 3", "Projeto 4", "Projeto 5", "Projeto 6", "Projeto 7",
                      "Projeto 8", "Projeto 9", "Projeto 10", "Projeto 11", "Projeto 12", "Projeto 13", "Projeto 14",
                      "Projeto 15"],
                "y": [186, 282, 106, 214, 258, 177, 104, 247, 182, 126, 235, 178, 172, 239, 203],
                "name": "Horas Alocadas",
                "marker": {"color": "#667eea"}
            }],
            "Funcionários com Maior Carga de Trabalho": [{
                "type": "bar",
                "x": ["Ana", "João", "Marcos", "Luiza", "Carlos", "Bruna", "Sofia", "Pedro", "Fernanda", "Tiago"],
                "y": [388, 248, 201, 120, 102, 168, 153, 128, 346, 318],
                "name": "Carga Horária",
                "marker": {"color": "#764ba2"}
            }],
            "Distribuição de Tipos de Tarefa": [{
                "type": "bar",
                "x": ["Design", "Dev", "Redação", "SEO", "Planejamento"],
                "y": [139, 241, 258, 124, 262],
                "name": "Horas por Tipo",
                "marker": {"color": "#f093fb"}
            }]
        },
        "financeiro": {
            "Faturamento Mensal por Cliente": [{
                "type": "line",
                "x": ["01/2025", "02/2025", "03/2025", "04/2025", "05/2025", "06/2025"],
                "y": [282963, 193060, 240119, 152037, 156091, 254315],
                "name": "Faturamento Total",
                "line": {"color": "#667eea", "width": 3}
            }],
            "Lucro por Projeto": [{
                "type": "scatter",
                "x": ["Projeto 1", "Projeto 2", "Projeto 3", "Projeto 4", "Projeto 5", "Projeto 6", "Projeto 7",
                      "Projeto 8", "Projeto 9", "Projeto 10", "Projeto 11", "Projeto 12", "Projeto 13", "Projeto 14",
                      "Projeto 15"],
                "y": [40609, 55360, 58733, 71143, 90696, 87893, 78885, 96913, 101915, 111702, 68414, 67011, 33068,
                      70229, 88085],
                "mode": "markers",
                "name": "Lucro",
                "marker": {"color": "#10b981", "size": 8}
            }],
            "Proporção de Custos Operacionais": [{
                "type": "pie",
                "labels": ["Salários", "Impostos", "Ferramentas", "Infraestrutura"],
                "values": [230278, 258791, 185673, 258434],
                "name": "Custos",
                "marker": {"colors": ["#667eea", "#764ba2", "#f093fb", "#10b981"]}
            }],
            "Evolução do Ticket Médio": [{
                "type": "line",
                "x": ["01/2025", "02/2025", "03/2025", "04/2025", "05/2025", "06/2025"],
                "y": [13425, 9180, 16897, 9173, 11366, 10740],
                "name": "Ticket Médio",
                "line": {"color": "#764ba2", "width": 3}
            }]
        },
        "comercial": {
            "Número de Novos Clientes por Mês": [{
                "type": "bar",
                "x": ["01/2025", "02/2025", "03/2025", "04/2025", "05/2025", "06/2025"],
                "y": [3, 6, 10, 9, 8, 4],
                "name": "Novos Clientes",
                "marker": {"color": "#f093fb"}
            }],
            "Tempo Médio de Retenção de Clientes": [{
                "type": "bar",
                "x": ["Cliente A", "Cliente B", "Cliente C", "Cliente D", "Cliente E", "Cliente F", "Cliente G",
                      "Cliente H", "Cliente I", "Cliente J"],
                "y": [13, 18, 24, 21, 22, 9, 7, 24, 15, 18],
                "name": "Meses de Retenção",
                "marker": {"color": "#667eea"}
            }],
            "Distribuição Geográfica de Clientes": [{
                "type": "bar",
                "x": ["SP", "RJ", "MG", "BA", "RS", "PR", "SC", "DF", "PE", "CE"],
                "y": [6, 1, 6, 3, 2, 6, 8, 6, 7, 4],
                "name": "Clientes por Estado",
                "marker": {"color": "#764ba2"}
            }]
        }
    }

    return jsonify(dashboard_data)


if __name__ == '__main__':
    app.run(debug=True)