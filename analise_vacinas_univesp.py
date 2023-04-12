import pandas as pd
import matplotlib.pyplot as plt

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


def save_to_sqlite():
    import sqlite3

    df = pd.read_csv("normalizada_lista_de_vacinados_araras.csv", sep=';')

    # Create a connection to a SQLite database
    conn = sqlite3.connect('univesp_PI.db')

    # Write the dataframe to a table in the database
    df.to_sql('vacinas_araras', conn, if_exists='replace', index=False)

    # Close the connection to the database
    conn.close()


if __name__ == "__main__":
    base_df = pd.read_csv("lista_de_vacinados_araras.csv", sep=';')

    # tratamento_qtd_vacinas_aplicadas(base_df)
    # perc_por_tipo_vacina(base_df)
    # perc_sexo(base_df)
    idade_vacinados(base_df)

