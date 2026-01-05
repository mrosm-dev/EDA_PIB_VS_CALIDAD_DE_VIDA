import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr

def filtrar_columna(df:pd.DataFrame, columna:str):
    '''
    Función para dividir un Dataset, en una lista de Dataset según los valores de una columna.
    '''
    lista_df = []
    lista_valores = df[columna].unique().tolist()
    for valor in lista_valores:
        lista_df.append(df[df[columna] == valor].set_index(columna))
    return lista_df


def plot_com_variable(df, comunidades, variables, tipo = 'linea'):
    for comunidad in comunidades:
        df_com = df[df["com_aut"] == comunidad].sort_values("año")

        if tipo == 'linea':
            for columna in variables:
                plt.figure(figsize=(8,4))
                plt.plot(df_com["año"], df_com[columna], marker="o")
                plt.xticks(df_com["año"], rotation=45)
                plt.xlabel("Año")
                plt.ylabel(columna)
                plt.title(f"{columna} - {comunidad}")
                plt.grid(True)
                plt.tight_layout()
                fig = plt.gcf()
                plt.show()

        if tipo == 'barra':
            for columna in variables:
                plt.figure(figsize=(8,4))
                plt.bar(df_com["año"], df_com[columna])
                plt.xticks(df_com["año"], rotation=45)
                plt.xlabel("Año")
                plt.ylabel(columna)
                plt.title(f"{columna} - {comunidad}")
                plt.grid(True)
                plt.tight_layout()
                fig = plt.gcf()
                plt.show()

    return fig


def plot_todas_comunidades(df, variable, comunidades=None):
    """
    Un gráfico para una 'variable'(columna), con una línea por comunidad (com_aut) a lo largo de los años.
    """
    # Si no pasás lista, usa todas las comunidades del df
    if comunidades is None:
        comunidades = sorted(df["com_aut"].dropna().unique())

    plt.figure(figsize=(11, 6))

    for com in comunidades:
        df_com = df[df["com_aut"] == com].sort_values("año")
        plt.plot(df_com["año"], df_com[variable], marker="o", linewidth=1)

    plt.xlabel("Año")
    plt.ylabel(variable)
    plt.title(f"Evolución de {variable} por Comunidad Autónoma")
    plt.grid(True)
    
    plt.legend(comunidades, bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    fig = plt.gcf()
    plt.show()
    
    return fig


def correlacion_com_bivariante(df, comunidades, variable1, variable2,alpha = 0.05):
    
    for comunidad in comunidades:
        df_com = df[df["com_aut"] == comunidad].sort_values("año")
        coef, pval = spearmanr(df_com[variable1], df_com[variable2])

        if pval < alpha:
            if coef > 0:
                interpretacion = "correlacion positiva significativa"
            elif coef < 0:
                interpretacion = "correlacion negativa significativa"
            else:
                interpretacion = "correlacion no significativa"
        else:
            interpretacion = "No se encontró evidencia estadísticamente significativa de correlación (p ≥ 0.05)"
            
        print(f'En {comunidad}, para las variables {variable1} y {variable2} interpretamos: {interpretacion}')