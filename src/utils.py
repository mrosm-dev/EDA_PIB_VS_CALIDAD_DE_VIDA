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


def plot_com_variable(df:pd.DataFrame, comunidades:list, variables:list, tipo:str='linea'):
    '''
    Función para graficar la línea temporal de X variables en Y comunidades autónomas.
    '''
    for comunidad in comunidades:
        df_com = df[df["comunidad_autonoma"] == comunidad].sort_values("año")

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

    return fig


def plot_todas_comunidades(df:pd.DataFrame, variable:list, comunidades:list=None):
    """
    Un gráfico para una 'variable'(columna), con una línea por comunidad (com_aut) a lo largo de los años.
    """
    # Si no pasás lista, usa todas las comunidades del df
    if comunidades is None:
        comunidades = sorted(df["comunidad_autonoma"].dropna().unique())

    plt.figure(figsize=(11, 6))

    for com in comunidades:
        df_com = df[df["comunidad_autonoma"] == com].sort_values("año")
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


def plot_dual_axis(df:pd.DataFrame, comunidades:list, var1:str, var2:str, x:str="año"):

    for comunidad in comunidades:
    
        df_com = df[df["comunidad_autonoma"] == comunidad].sort_values(x).copy()
    
        fig, ax1 = plt.subplots(figsize=(10, 5))
        ax2 = ax1.twinx()
    
        # líneas
        l1 = ax1.plot(df_com[x], df_com[var1], marker="o", linewidth=1.5, label=var1)
        l2 = ax2.plot(df_com[x], df_com[var2], marker="s", linewidth=1.5, label=var2)
    
        # labels
        ax1.set_xlabel(x)
        ax1.set_ylabel(var1)
        ax2.set_ylabel(var2)
    
        # título
        ax1.set_title(f"{comunidad}: {var1} vs {var2} (a lo largo del tiempo)")
    
        # eje X prolijo
        ax1.set_xticks(sorted(df_com[x].unique()))
        ax1.tick_params(axis="x", rotation=45)
    
        # grilla
        ax1.grid(True, alpha=0.3)
    
        # leyenda combinada
        lines = l1 + l2
        labels = [line.get_label() for line in lines]
        ax1.legend(lines, labels, loc="upper center")
    
        plt.tight_layout()
        plt.show()


def correlacion_com_bivariante(df, comunidades, variable1, variable2,alpha = 0.05):
    
    for comunidad in comunidades:
        df_com = df[df["comunidad_autonoma"] == comunidad].sort_values("año")
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
            
        print(f'En {comunidad}, para las variables {variable1} y {variable2} interpretamos:\n {interpretacion}')