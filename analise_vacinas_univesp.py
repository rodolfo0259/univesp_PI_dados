import pandas as pd
import matplotlib.pyplot as plt

class GerarGraficos:
    def __init__(self):
        pass

    def make_graph(df, graph_type, name, xlabel="", ylabel=""):
        plt.figure(figsize=(8, 8))
        if graph_type == 'pie':
            df.plot(kind=graph_type, autopct='%1.1f%%') 
        else:
            df.plot(kind=graph_type) 
            # Add labels and values to the bars
            for i, v in enumerate(df.values.tolist()):
                plt.annotate(str(v), xy=(i, v), ha='center', va='bottom')
            
            plt.xticks(rotation=0)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        

        # Save the image with a custom name
        plt.savefig(f'graph_imgs/{name}_{graph_type}.png')
        # Clear the current figure and axes
        plt.clf()
        plt.cla()

    def tratamento_qtd_vacinas_aplicadas(base_df):
        df = base_df[["DATA_APLICACAO_VACINA", "index"]].copy()
        # Convert date column to datetime format with multiple formats
        df['data_nova'] = pd.to_datetime(df['DATA_APLICACAO_VACINA'], infer_datetime_format=True)

        # Create new column with year-month format
        df['DATA_APLICACAO_VACINA'] = df['data_nova'].dt.strftime('%Y-%m-%d')
        df['year_month'] = df['data_nova'].dt.strftime('%Y-%m')

        grouped = df.groupby('year_month')['index'].count()

        graph_type = 'line'
        make_graph(grouped, graph_type, 'vacinas_por_periodo', xlabel="Periodo", ylabel="Vacinas aplicadas")

    def perc_por_tipo_vacina(base_df):
        df = base_df[["IMUNOBIOLOGICO", "index"]].copy()
        df["IMUNOBIOLOGICO"] = df["IMUNOBIOLOGICO"].str.replace('\s.*', '', regex=True)
        df["IMUNOBIOLOGICO"] = df["IMUNOBIOLOGICO"].str.replace('/.*', '', regex=True)
        grouped = df.groupby("IMUNOBIOLOGICO")["index"].count()
        make_graph(grouped, graph_type="pie", name="vacinas_aplicadas", xlabel="Tipo de vacinas aplicadas")

    def perc_sexo(base_df):
        df = base_df[["SEXO_PACIENTE", "index"]].copy()
        df.loc[df["SEXO_PACIENTE"] == "F", "SEXO_PACIENTE"] = "Feminino"
        df.loc[df["SEXO_PACIENTE"] == "M", "SEXO_PACIENTE"] = "Masculino"
        df.loc[df["SEXO_PACIENTE"] == "I", "SEXO_PACIENTE"] = "Não informado"
        grouped = df.groupby("SEXO_PACIENTE")["index"].count()
        make_graph(grouped, graph_type="pie", name="vacinas_aplicadas_por_sexo", xlabel="Vacinas aplicadas por sexo")

    def idade_vacinados(base_df):
        df = base_df[["IDADE", "index"]].copy()
        linhas = ["1 a 9", "10 a 19", "20 a 29", "30 a 39", "40 a 49", "50 a 59", "60 a 69", "70 a 79"]
        for i in linhas:
            df.loc[(df["IDADE"] >= eval(i.split('a')[0].strip()))  & (df["IDADE"] <= eval(i.split('a')[1].strip())),'faixa_etaria'] = i
        df.loc[df["IDADE"] >= 80,'faixa_etaria'] = "80 ou mais"
        grouped = df.groupby("faixa_etaria")["index"].count()
        make_graph(grouped, graph_type="bar", name="vacinas_aplicadas_por_idade", xlabel="Idade (em anos)", ylabel="Quantida de vacinas aplicadas")

class TratamentoExcel:
    def __init__(self):
        pass

    def tratar_data_hora(base_df):
        colunas_sem_horas = [
            "DATA_APLICACAO_VACINA",
            "DATA_APRAZAMENTO",
            "DATA_NASCIMENTO_PACIENTE",
            "DATA_VALIDADE_LOTE"
        ]

        for index, colum in enumerate(colunas_sem_horas):
            base_df[colum] = pd.to_datetime(
                base_df[colum],
                dayfirst=True
                ).dt.strftime('%Y-%m-%d')

        ## colunas com horas
        df = base_df["DATA_REGISTRO_VACINA"].str.split(' ', expand=True).add_prefix('A_horas_')

        df['A_horas_0'] = pd.to_datetime(
            df['A_horas_0'], 
            infer_datetime_format=True,
            dayfirst=True
            ).dt.strftime('%Y-%m-%d')

        base_df["DATA_REGISTRO_VACINA"] = df['A_horas_0'] + ' ' + df['A_horas_1']

        return base_df

    def padronizar_sexo(base_df):
        base_df['SEXO_PACIENTE'] = base_df['SEXO_PACIENTE'].str.strip()
        base_df.loc[base_df['SEXO_PACIENTE'] == 'M', 'SEXO_PACIENTE'] = "Homem"
        base_df.loc[base_df['SEXO_PACIENTE'] == 'F', 'SEXO_PACIENTE'] = "Mulher"
        base_df.loc[base_df['SEXO_PACIENTE'] == 'I', 'SEXO_PACIENTE'] = "Indefinido"
        base_df['SEXO_PACIENTE'].fillna('Indefinido', inplace=True)

        return base_df

    def tratar_nulls_e_nome_dose(base_df):
        ## nulls
        base_df['MUNICIPIO_RESIDENCIA_PACIENTE'].fillna('NAO INFORMADA', inplace=True)
        
        base_df.loc[base_df['MUNICIPIO_RESIDENCIA_PACIENTE'] == 'NAO INFORMADA', 'SIGLA_UF_RESIDENCIA_PACIENTE'] == "NAO INFORMADA"
        base_df['SIGLA_UF_RESIDENCIA_PACIENTE'].fillna('SP', inplace=True)

        ## Nome errado
        base_df.loc[base_df['DOSE'] >= "REFORCO", 'DOSE'] =  "1° REFORCO"

        ## quando sexo indefinido, PACIENTE_GESTANTE e PACIENTE_PUERPERE vem null
        for x in ["PACIENTE_GESTANTE", "PACIENTE_PUERPERE"]:
            base_df[x].fillna(0, inplace=True)
            base_df[x] = base_df[x].astype(int)
            base_df[x] = base_df[x].astype(str)
            base_df.loc[base_df[x] == "1", x] = "SIM"
            base_df.loc[base_df[x] == "0", x] = "NÃO"

        return base_df

    def criar_faixa_etarias(base_df):
        base_df.loc[(base_df['IDADE'] >= 0) & (base_df['IDADE']  < 10), 'FAIXA ETÁRIA'] = '0 a 10 anos'
        base_df.loc[(base_df['IDADE'] >= 10) & (base_df['IDADE'] < 20), 'FAIXA ETÁRIA'] = '10 a 20 anos'
        base_df.loc[(base_df['IDADE'] >= 20) & (base_df['IDADE'] < 30), 'FAIXA ETÁRIA'] = '20 a 30 anos'
        base_df.loc[(base_df['IDADE'] >= 30) & (base_df['IDADE'] < 40), 'FAIXA ETÁRIA'] = '30 a 40 anos'
        base_df.loc[(base_df['IDADE'] >= 40) & (base_df['IDADE'] < 50), 'FAIXA ETÁRIA'] = '40 a 50 anos'
        base_df.loc[(base_df['IDADE'] >= 50) & (base_df['IDADE'] < 60), 'FAIXA ETÁRIA'] = '50 a 60 anos'
        base_df.loc[(base_df['IDADE'] >= 60) & (base_df['IDADE'] < 70), 'FAIXA ETÁRIA'] = '60 a 70 anos'
        base_df.loc[(base_df['IDADE'] >= 70) & (base_df['IDADE'] < 80), 'FAIXA ETÁRIA'] = '70 a 80 anos'
        base_df.loc[(base_df['IDADE'] >= 80) & (base_df['IDADE'] < 90), 'FAIXA ETÁRIA'] = '80 a 90 anos'
        base_df.loc[base_df['IDADE'] >= 90, 'FAIXA ETÁRIA']                             = 'Acima de 90 anos'
        return base_df

if __name__ == "__main__":
    filename = ""
    sheetname = ""
    base_df = pd.read_excel(filename, sheetname)

    base_df = TratamentoExcel.tratar_data_hora(base_df)
    base_df = TratamentoExcel.padronizar_sexo(base_df)
    base_df = TratamentoExcel.tratar_nulls_e_nome_dose(base_df)
    base_df = TratamentoExcel.criar_faixa_etarias(base_df)

    base_df.to_csv("", sep=',', index=True, index_label="INDEX")

