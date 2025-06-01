from datetime import timedelta

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GoogleSheetsReader:
    def __init__(self):
        self.credenciais_path = "ninth-archway-456822-d9-4bc9133f5905.json"
        self.nome_planilha = "Projeto DMSBox"
        self.client = self._autenticar()

    def _autenticar(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credenciais_path, scope)
        client = gspread.authorize(creds)
        return client

    def get_sheet(self, sheet_name):
        return self.client.open(self.nome_planilha).worksheet(sheet_name).get_all_records()

    def get_sheet_df(self, sheet_name):
        return pd.DataFrame(self.get_sheet(sheet_name))

    def buscar_profissionais(self):
        dados = self.get_sheet("Base de Dados Funcionários")

        for linha in dados:
            valor_hora = float(str(linha.get("Valor da Hora")).replace("R$", "").replace(",", "."))

        # valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        dados_df = pd.DataFrame(dados)

        dados_df = dados_df[dados_df["Apelido"] != ""]

        return dados_df

    def buscar_alocacao_horas(self):

        dados = self.get_sheet("Alocação de Horas")
        dados_df = pd.DataFrame(dados)
        alocacao_horas = dados_df.groupby(["Cliente", "Mes", "Funcionario", "Ano"])["Total de Horas"].sum().reset_index()
        alocacao_horas = alocacao_horas[alocacao_horas["Mes"].apply(lambda x: isinstance(x, int))]

        return alocacao_horas

    def pegar_horas_disponiveis_por_mes(self):
        profissionais = self.buscar_profissionais()
        alocacao = self.buscar_alocacao_horas()

        merged = alocacao.merge(profissionais[["Apelido", "HORAS ÚTEIS PONDERADAS"]], how="left", right_on="Apelido", left_on='Funcionario')

        merged["Horas disponiveis"] = merged["HORAS ÚTEIS PONDERADAS"] - merged["Total de Horas"]

        return merged

    def profissionais_disponiveis_avulso(self, data_inicio_projeto, data_fim_projeto):
        mes_inicio = data_inicio_projeto.month
        ano_inicio = data_inicio_projeto.year
        mes_fim = data_fim_projeto.month
        ano_fim = data_fim_projeto.year

        data_atual = data_inicio_projeto
        resultado = []
        while data_atual <= data_fim_projeto:
            resultado.append({"Mes": data_atual.month, "Ano": data_atual.year})
            if data_atual.month == 12:
                data_atual = data_atual.replace(year=data_atual.year+1, month=1)
            else:
                data_atual = data_atual.replace(month=data_atual.month+1)

        modelo = pd.DataFrame(resultado)


        profissionais = self.buscar_profissionais()

        horas_disponiveis_por_mes = self.pegar_horas_disponiveis_por_mes()

        horas_disponiveis_por_mes = horas_disponiveis_por_mes[
            (horas_disponiveis_por_mes["Ano"].astype(int) >= ano_inicio)
            & (horas_disponiveis_por_mes["Ano"].astype(int) <= ano_fim)
            & (horas_disponiveis_por_mes["Mes"].astype(int) >= mes_inicio)
            & (horas_disponiveis_por_mes["Mes"].astype(int) <= mes_fim)
        ]

        profissionais_disponiveis = []
        # profissionais = profissionais[profissionais["Apelido"] == "ANAJU"]
        for index, row in profissionais.iterrows():

            horas_mes = horas_disponiveis_por_mes[horas_disponiveis_por_mes["Apelido"] == row["Apelido"]]

            if "Horas disponiveis" in horas_mes.columns:
                merged = modelo.merge(horas_mes, on=["Mes", "Ano"], how='left')

                merged = merged[["Mes", "Ano", "Horas disponiveis"]]

                horas_sem_alocacao = row["HORAS ÚTEIS PONDERADAS"]
                merged = merged.fillna(horas_sem_alocacao)

                horas = list(merged["Horas disponiveis"])

            else:
                numero_de_meses = (data_fim_projeto.year - data_inicio_projeto.year) * 12 + (data_fim_projeto.month - data_inicio_projeto.month)
                horas = [row["HORAS ÚTEIS PONDERADAS"] for mes in range(0, numero_de_meses)]


            profissionais_disponiveis.append({
                "nome": row["Apelido"],
                "nivel": row["NÍVEL"],
                "valor_hora": float(str(row["Valor da Hora"]).replace("R$", "").replace(",", ".")),
                "horas_mensais": horas
            })

        return profissionais_disponiveis

    def profissionais_disponiveis_recorrente(self, data_inicio_projeto, vigencia):
        data_fim_projeto = data_inicio_projeto + timedelta(days=vigencia*30)
        mes_inicio = data_inicio_projeto.month
        ano_inicio = data_inicio_projeto.year
        mes_fim = data_fim_projeto.month
        ano_fim = data_fim_projeto.year

        data_atual = data_inicio_projeto
        resultado = []
        while data_atual <= data_fim_projeto:
            resultado.append({"Mes": data_atual.month, "Ano": data_atual.year})
            if data_atual.month == 12:
                data_atual = data_atual.replace(year=data_atual.year+1, month=1)
            else:
                data_atual = data_atual.replace(month=data_atual.month+1)

        modelo = pd.DataFrame(resultado)


        profissionais = self.buscar_profissionais()

        horas_disponiveis_por_mes = self.pegar_horas_disponiveis_por_mes()

        horas_disponiveis_por_mes = horas_disponiveis_por_mes[
            (horas_disponiveis_por_mes["Ano"].astype(int) >= ano_inicio)
            & (horas_disponiveis_por_mes["Ano"].astype(int) <= ano_fim)
            & (horas_disponiveis_por_mes["Mes"].astype(int) >= mes_inicio)
            & (horas_disponiveis_por_mes["Mes"].astype(int) <= mes_fim)
        ]

        profissionais_disponiveis = []
        for index, row in profissionais.iterrows():

            horas_mes = horas_disponiveis_por_mes[horas_disponiveis_por_mes["Apelido"] == row["Apelido"]]

            if "Horas disponiveis" in horas_mes.columns:
                merged = modelo.merge(horas_mes, on=["Mes", "Ano"], how='left')

                merged = merged[["Mes", "Ano", "Horas disponiveis"]]

                horas_sem_alocacao = row["HORAS ÚTEIS PONDERADAS"]
                merged = merged.fillna(horas_sem_alocacao)

                horas = list(merged["Horas disponiveis"])

            else:
                numero_de_meses = (data_fim_projeto.year - data_inicio_projeto.year) * 12 + (data_fim_projeto.month - data_inicio_projeto.month)
                horas = [row["HORAS ÚTEIS PONDERADAS"] for mes in range(0, numero_de_meses)]


            profissionais_disponiveis.append({
                "nome": row["Apelido"],
                "nivel": row["NÍVEL"],
                "valor_hora": float(str(row["Valor da Hora"]).replace("R$", "").replace(",", ".")),
                "horas_disponiveis": min(horas) if horas else 0
            })

        return profissionais_disponiveis