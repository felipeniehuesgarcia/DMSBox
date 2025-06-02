from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

from google_sheets import GoogleSheetsReader

app = Flask(__name__)


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
        profissionais_disponiveis = GoogleSheetsReader().profissionais_disponiveis_recorrente(
            datetime.strptime(inicio, "%Y-%m-%d"), int(vigencia)
        )

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
        profissionais_disponiveis = GoogleSheetsReader().profissionais_disponiveis_avulso(inicio, fim)
        total_meses = (fim.year - inicio.year) * 12 + fim.month - inicio.month + 1

        return render_template('alocar_avulso.html',
                               profissionais=profissionais_disponiveis,
                               meses=total_meses,
                               qtd=qtd_profissionais)
    return render_template('dados_avulso.html')


# Rota para processar resultados (ainda precisa ser implementada)
@app.route('/resultado', methods=['POST'])
def resultado():
    # Aqui você processará os dados do formulário e calculará os resultados
    # Por enquanto, vou retornar uma página de resultado básica
    return render_template('resultado.html', dados=request.form)


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