import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
                fig.set_facecolor('#00517c')
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
                fig.set_facecolor('#00517c')
                plt.show()

    return fig


def plot_todas_comunidades(df:pd.DataFrame, variable:list, comunidades:list=None):
    """
    Un gráfico para una 'variable'(columna), con una línea por comunidad (com_aut) a lo largo de los años.
    """
    if comunidades is None:
        comunidades = sorted(df["comunidad_autonoma"].dropna().unique())

    plt.figure(figsize=(13, 7))
    ax = plt.gca()

    for com in comunidades:
        df_com = df[df["comunidad_autonoma"] == com].sort_values("año")
        plt.plot(df_com["año"], df_com[variable], linewidth=3.5, marker="o", markersize=7 )

    ax.set_xlabel("Año", color="white", fontsize=16, fontweight="bold")
    ax.set_ylabel(variable, color="white", fontsize=16, fontweight="bold")
    ax.set_title(f"Evolución de {variable}", color="white", fontsize=20, fontweight="bold", pad=15)

    ax.tick_params(axis="both", colors="white", labelsize=14, width=2)
    ax.grid(True, alpha=0.25, color="white", linewidth=1.2)

    leg = ax.legend(comunidades, bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=12, frameon=False)
    for text in leg.get_texts():
        text.set_color("white")
        text.set_fontweight("bold")

    fig = plt.gcf()
    fig.set_facecolor("#00517c")
    ax.set_facecolor("#00517c")

    for spine in ax.spines.values():
        spine.set_color("white")
        spine.set_linewidth(2)

    plt.tight_layout()
    plt.show()

    return fig




def plot_dual_axis(df: pd.DataFrame, comunidades: list, var1: str, var2: str, x: str = "año"):

    fig, ax1 = plt.subplots(figsize=(13, 7))
    fig.set_facecolor("#00517c")
    ax1.set_facecolor("#00517c")
    ax2 = ax1.twinx()

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    for i, comunidad in enumerate(comunidades):
        color = colors[i % len(colors)]
        df_com = df[df["comunidad_autonoma"] == comunidad].sort_values(x).copy()
        ax1.plot(df_com[x], df_com[var1], marker="o", linestyle="-", linewidth=3.5, markersize=7, color=color, label=f"{comunidad} – {var1}")
        ax2.plot(df_com[x], df_com[var2], marker="s", linestyle="--", linewidth=3.5, markersize=7, color=color, label=f"{comunidad} – {var2}")

    ax1.set_xlabel(x, color="white", fontsize=16, fontweight="bold")
    ax1.set_ylabel(var1, color="white", fontsize=16, fontweight="bold")
    ax2.set_ylabel(var2, color="white", fontsize=16, fontweight="bold")

    ax1.set_xticks(sorted(df[x].unique()))
    ax1.tick_params(axis="x", rotation=45, colors="white", labelsize=14, width=2)
    ax1.tick_params(axis="y", colors="white", labelsize=14, width=2)
    ax2.tick_params(axis="y", colors="white", labelsize=14, width=2)

    ax1.set_title(f"{var1} (continua) vs {var2} (discontinua)", color="white", fontsize=20, fontweight="bold", pad=15)
    ax1.grid(True, alpha=0.25, color="white", linewidth=1.2)

    for spine in ax1.spines.values():
        spine.set_color("white")
        spine.set_linewidth(2)
    for spine in ax2.spines.values():
        spine.set_color("white")
        spine.set_linewidth(2)

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    leg = ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper center", ncol=2, fontsize=12, frameon=False)
    for text in leg.get_texts():
        text.set_color("white")
        text.set_fontweight("bold")

    plt.tight_layout()
    plt.show()



def correlacion_com_bivariante(df, comunidades, variable1, variable2,alpha = 0.05):
    print(f'Coeficiente de correlación de Spearman entre {variable1} y {variable2}\n')
    Correlacion_positiva = []
    Correlacion_positiva_coeficiente = []
    Correlacion_negativa = []
    Correlacion_negativa_coeficiente = []
    Sin_correlacion = []
    Sin_correlacion_coeficiente = []
    Sin_evidencia_significativa = []
    Sin_evidencia_pval = []
    
    for comunidad in comunidades:
        df_com = df[df["comunidad_autonoma"] == comunidad].sort_values("año")
        coef, pval = spearmanr(df_com[variable1], df_com[variable2])
        coef = float(coef)
        pval = float(pval)
        umbral_coef = 0.1 

        if pval < alpha:
            if abs(coef) < umbral_coef:
                Sin_correlacion.append(comunidad)
                Sin_correlacion_coeficiente.append(round(coef,3))
            
            elif coef > 0:
                Correlacion_positiva.append(comunidad)
                Correlacion_positiva_coeficiente.append(round(coef,3))
            else:
                Correlacion_negativa.append(comunidad)
                Correlacion_negativa_coeficiente.append(round(coef,3))
        else:
            Sin_evidencia_significativa.append(comunidad)
            Sin_evidencia_pval.append(round(pval,3))
            
    print(f'Comunidades con correlacion positiva y sus coeficientes (pval < {alpha} y coef > 0):\n {Correlacion_positiva}\n { Correlacion_positiva_coeficiente}')
    print('\n')
    print(f'Comunidades con correlacion negativa y sus coeficientes (pval < {alpha} y coef < 0):\n {Correlacion_negativa}\n {Correlacion_negativa_coeficiente}')   
    print('\n')
    print(f'Comunidades sin correlacion y sus coeficientes (pval < {alpha} y coef ≈ 0):\n {Sin_correlacion}\n {Sin_correlacion_coeficiente}')
    print('\n')
    print(f'Comunidades que no se encontró evidencia estadísticamente significativa y su pval (pval > {alpha}):\n {Sin_evidencia_significativa}\n {Sin_evidencia_pval}')


def pearson_p_matrix(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Devuelve una matriz de p-values de Pearson con la misma estructura que df.corr()
    '''

    cols = df.columns
    p_matrix = pd.DataFrame(np.ones((len(cols), len(cols))), index=cols, columns=cols)

    for i, col_i in enumerate(cols):
        for j, col_j in enumerate(cols):
            if i >= j:
                x = df[col_i]
                y = df[col_j]
                valid = x.notna() & y.notna()
                if valid.sum() > 2:
                    _, p = pearsonr(x[valid], y[valid])

                else:
                    p = np.nan

                p_matrix.loc[col_i, col_j] = p
                p_matrix.loc[col_j, col_i] = p

    return p_matrix