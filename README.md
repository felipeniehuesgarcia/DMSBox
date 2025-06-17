# Sistema de Rentabilidade

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Características Principais](#características-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Funcionalidades](#funcionalidades)
- [API Endpoints](#api-endpoints)
- [Dashboard](#dashboard)
- [Integração com Google Sheets](#integração-com-google-sheets)
- [Deployment](#deployment)
- [Manutenção](#manutenção)

## 🎯 Visão Geral

O Sistema de Rentabilidade é uma aplicação web desenvolvida em Flask para calcular e analisar a rentabilidade de projetos. O sistema oferece duas modalidades de cálculo:

- **Projetos Recorrentes**: Contratos mensais com equipes dedicadas
- **Projetos Avulsos**: Projetos pontuais com prazo determinado

A aplicação inclui dashboards interativos para visualização de dados operacionais, financeiros e comerciais.

## ✨ Características Principais

### 🔄 Projetos Recorrentes
- Configuração de equipe dedicada
- Vigência contratual em meses
- Cálculo de custo mensal e anual
- Validação de disponibilidade de profissionais

### ⚡ Projetos Avulsos
- Alocação flexível de horas
- Distribuição entre profissionais e meses
- Controle de prazo de entrega
- Validação de limites mensais

### 📊 Dashboard Inteligente
- **Operacional**: Distribuição de tarefas, carga de trabalho, horas por projeto
- **Financeiro**: Faturamento, lucro, custos operacionais, ticket médio
- **Comercial**: Novos clientes, retenção, distribuição geográfica

### 🎨 Interface Moderna
- Design responsivo com gradientes e animações
- Tema escuro/claro automático
- Componentes interativos
- Validação em tempo real

## 🛠 Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **Jinja2** - Template engine
- **Pandas** - Manipulação de dados
- **Google Sheets API** - Integração com planilhas

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript ES6+** - Interatividade
- **Plotly.js** - Gráficos interativos
- **CSS Grid/Flexbox** - Layout responsivo

### Estilização
- **CSS Custom Properties** - Variáveis CSS
- **Gradient Backgrounds** - Fundos modernos
- **Box Shadow** - Profundidade visual
- **Smooth Animations** - Transições suaves

## 📁 Estrutura do Projeto

```
sistema-rentabilidade/
├── app.py                          # Aplicação principal Flask
├── google_sheets.py                # Integração Google Sheets
├── requirements.txt                # Dependências Python
├── ninth-archway-456822-d9-4bc9133f5905.json  # Credenciais Google
├── templates/
│   ├── index.html                  # Página inicial
│   ├── dados_recorrente.html       # Formulário projeto recorrente
│   ├── dados_avulso.html          # Formulário projeto avulso
│   ├── selecionar.html            # Seleção de profissionais
│   ├── alocar_avulso.html         # Alocação de horas avulso
│   ├── resultado.html             # Resultado dos cálculos
│   ├── dashboard.html             # Dashboard principal
│   └── tipo_projeto.html          # Seleção tipo de projeto
└── static/                        # (futuro) Arquivos estáticos
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Conta Google Cloud com Sheets API habilitada
- Credenciais de service account

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd sistema-rentabilidade
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure credenciais Google**
- Baixe o arquivo JSON das credenciais do Google Cloud
- Renomeie para `ninth-archway-456822-d9-4bc9133f5905.json`
- Coloque na raiz do projeto

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse no navegador**
```
http://localhost:5000
```

## 🎯 Funcionalidades

### Página Inicial (`/`)
- Interface com tabs para Calculadora e Dashboard
- Seleção entre projeto recorrente e avulso
- Dashboard integrado com visualizações

### Projetos Recorrentes (`/dados_recorrente`)
**Entrada:**
- Quantidade de profissionais (1-20)
- Data de início do contrato
- Vigência em meses (1-60)

**Processamento:**
- Validação de disponibilidade na planilha
- Cálculo de custos mensais
- Aplicação de markup

### Projetos Avulsos (`/dados_avulso`)
**Entrada:**
- Data do contrato e prazo de entrega
- Total de horas contratadas
- Número de profissionais

**Processamento:**
- Cálculo automático de meses
- Alocação flexível de horas
- Validação de limites por profissional

### Seleção de Profissionais (`/selecionar`)
- Lista dinâmica de profissionais disponíveis
- Exibição de nível e valor/hora
- Validação de horas disponíveis
- Cálculo em tempo real

### Alocação de Horas (`/alocar_avulso`)
- Grid de profissionais vs meses
- Validação de limites mensais
- Progress indicator visual
- Cálculo progressivo de totais

## 🔌 API Endpoints

### GET `/`
**Descrição**: Página inicial do sistema
**Retorno**: Template `index.html`

### GET/POST `/dados_recorrente`
**GET**: Formulário de dados do projeto recorrente
**POST**: Processa dados e redireciona para seleção

**Parâmetros POST:**
```json
{
  "quantidade": "integer",
  "inicio": "date (YYYY-MM-DD)",
  "vigencia": "integer"
}
```

### GET/POST `/dados_avulso`
**GET**: Formulário de dados do projeto avulso
**POST**: Processa dados e redireciona para alocação

**Parâmetros POST:**
```json
{
  "data_contrato": "date",
  "prazo": "date",
  "qtd_profissionais": "integer"
}
```

### POST `/resultado`
**Descrição**: Processa formulários finais e exibe resultado
**Parâmetros**: Dados do formulário de alocação
**Retorno**: Template `resultado.html`

### GET `/api/dashboard-data`
**Descrição**: Dados JSON para os gráficos do dashboard
**Retorno**: Estrutura com dados dos gráficos

```json
{
  "operacional": {
    "Horas Alocadas por Projeto": [plotly_data],
    "Funcionários com Maior Carga": [plotly_data],
    "Distribuição de Tipos de Tarefa": [plotly_data]
  },
  "financeiro": {
    "Faturamento Mensal": [plotly_data],
    "Lucro por Projeto": [plotly_data],
    "Custos Operacionais": [plotly_data],
    "Ticket Médio": [plotly_data]
  },
  "comercial": {
    "Novos Clientes": [plotly_data],
    "Retenção de Clientes": [plotly_data],
    "Distribuição Geográfica": [plotly_data]
  }
}
```

## 📊 Dashboard

### Categorias Disponíveis

#### 🧑‍💻 Operacional
- **Distribuição de Tipos de Tarefa**: Gráfico de barras mostrando horas por tipo
- **Funcionários com Maior Carga**: Ranking de carga horária
- **Horas Alocadas por Projeto**: Distribuição de horas por projeto

#### 💰 Financeiro
- **Faturamento Mensal**: Evolução temporal da receita
- **Lucro por Projeto**: Scatter plot da margem por projeto
- **Custos Operacionais**: Pizza com breakdown de custos
- **Ticket Médio**: Evolução do valor médio por cliente

#### 📈 Comercial
- **Novos Clientes**: Aquisição mensal de clientes
- **Retenção de Clientes**: Tempo médio de permanência
- **Distribuição Geográfica**: Clientes por estado

### Tecnologia dos Gráficos
- **Plotly.js** para renderização
- Layout responsivo
- Configuração de cores personalizadas
- Interatividade completa (zoom, hover, seleção)

## 🔗 Integração com Google Sheets

### Configuração da Planilha

A planilha "Projeto DMSBox" deve conter as seguintes abas:

#### "Base de Dados Funcionários"
```
Colunas obrigatórias:
- Apelido: Nome do profissional
- NÍVEL: Junior/Pleno/Senior
- Valor da Hora: Valor em R$
- HORAS ÚTEIS PONDERADAS: Horas disponíveis padrão
```

#### "Alocação de Horas"
```
Colunas obrigatórias:
- Cliente: Nome do cliente
- Mes: Número do mês (1-12)
- Ano: Ano da alocação
- Funcionario: Nome do funcionário
- Total de Horas: Horas alocadas
```

### Classe GoogleSheetsReader

#### Métodos Principais

**`buscar_profissionais()`**
- Retorna DataFrame com todos os profissionais
- Filtra por apelido não vazio
- Converte valor da hora para float

**`buscar_alocacao_horas()`**
- Retorna alocação agrupada por cliente/mês/funcionário
- Valida se mês é inteiro

**`pegar_horas_disponiveis_por_mes()`**
- Calcula disponibilidade por mês
- Subtrai horas alocadas das horas úteis

**`profissionais_disponiveis_avulso(data_inicio, data_fim)`**
- Retorna profissionais disponíveis para período específico
- Inclui array de horas disponíveis por mês

**`profissionais_disponiveis_recorrente(data_inicio, vigencia)`**
- Retorna profissionais para projeto recorrente
- Inclui mínimo de horas disponíveis no período

### Dados Simulados

Enquanto a integração Google Sheets não estiver funcionando, a função `get_mock_profissionais()` retorna dados simulados:

```python
[
    {
        "nome": "Ana Silva",
        "nivel": "Senior",
        "valor_hora": 85.0,
        "horas_disponiveis": 160,
        "horas_mensais": [160, 140, 180, 160, 150, 170]
    },
    # ... outros profissionais
]
```

## 🚀 Deployment

### Desenvolvimento Local
```bash
python app.py
# Servidor em http://localhost:5000
```

### Produção com Gunicorn
```bash
gunicorn app:app -w 4 -b 0.0.0.0:8000
```

### Docker (Opcional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Variáveis de Ambiente
```bash
FLASK_ENV=production
GOOGLE_SHEETS_CREDENTIALS=ninth-archway-456822-d9-4bc9133f5905.json
PLANILHA_NOME="Projeto DMSBox"
```

## 🔧 Manutenção

### Logs e Monitoramento
- Flask possui logging básico habilitado
- Para produção, configure logging externo
- Monitore endpoints com maior uso

### Backup dos Dados
- Dados principais estão no Google Sheets
- Fazer backup regular das credenciais
- Documentar estrutura da planilha

### Atualizações
1. **Backend**: Atualizar dependências no `requirements.txt`
2. **Frontend**: Atualizar bibliotecas CDN nos templates
3. **Google API**: Verificar mudanças na API periodicamente

### Debugging
```python
# Habilitar debug no desenvolvimento
app.run(debug=True)

# Verificar logs
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance
- Cache de dados do Google Sheets
- Compressão de respostas
- Minificação de CSS/JS para produção
- CDN para assets estáticos

## 📝 Notas Importantes

1. **Segurança**: As credenciais Google estão commitadas no repositório. Em produção, usar variáveis de ambiente.

2. **Rate Limits**: Google Sheets API tem limites de requisições. Implementar cache se necessário.

3. **Validação**: Todas as entradas são validadas no frontend e backend.

4. **Responsividade**: Interface adaptada para mobile e desktop.

5. **Acessibilidade**: Considerar implementar ARIA labels para melhor acessibilidade.

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste localmente
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.
