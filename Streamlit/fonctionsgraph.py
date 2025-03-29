import streamlit as st

import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from matplotlib.ticker import FuncFormatter

import statsmodels.api as sm
from statsmodels.formula.api import ols

def graph_countIncident(df, variable):
    """
    Affiche un barplot comptant le nombre d'incidents en fonction d'une variable catégorielle dans un DataFrame.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
    """

    jours_semaine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    mois = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    if variable == 'DayOfWeek':
        df[variable] = pd.Categorical(df[variable], categories=jours_semaine, ordered=True)
    elif variable == 'Month':
        df[variable] = pd.Categorical(df[variable], categories=mois, ordered=True)

    df_count = df[['IncidentNumber', variable]].groupby(variable).agg(['count']).reset_index()
    
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(list(df_count[variable]), list(df_count.IncidentNumber['count']))
    ax.set_ylabel("Nombre d'incidents")
    ax.set_xlabel(variable)
    ax.set_title(f"Nombre d'incidents pour les valeurs de {variable}")

    if variable == 'DayOfWeek' or variable == 'Month':
        # Incline les annotations de l'axe des abscisses
        plt.xticks(rotation=45, ha='right')  # Ajout de cette ligne
        plt.tight_layout() # Ajout de cette ligne
    
        # Affichage du graphique dans Streamlit
    st.pyplot(fig)

def graphQuali_countPlot(df, variable):
    """
    Affiche un histogramme interactif de la distribution d'une variable catégorielle dans un DataFrame.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
    """
    fig = px.histogram(df, x=variable, nbins=30, title=f"Distribution de {variable}")
    
    # Personnaliser le layout
    fig.update_layout(
        height=500,
        width=600,
        barmode='group'  # Pour grouper les barres si nécessaire
    )
    
    # Affichage du graphique dans Streamlit
    st.plotly_chart(fig)

def graphQuali_pointplot(df, variable):
    """
    Affiche un pointplot (indication de la moyenne + IC95%) des temps (transformation Box-Cox) en fonction d'une variable catégorielle.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
    """
    var = 'boxcox_TotalResponseTime'  # Variable à tracer

    jours_semaine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    mois = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    if variable == 'DayOfWeek':
        df[variable] = pd.Categorical(df[variable], categories=jours_semaine, ordered=True)
    elif variable == 'Month':
        df[variable] = pd.Categorical(df[variable], categories=mois, ordered=True)
    
    # Création du graphique
    fig, axes = plt.subplots(1, 1, figsize=(6, 5))
    
    # Tracer le pointplot
    sns.pointplot(x=variable, y=var, data=df, ax=axes)
    
    # Titres et labels
    axes.set_title(f"Pointplot de {var} \nen fonction de {variable}")
    axes.set_xlabel(variable)
    axes.set_ylabel(var)

    if variable == 'ratioSC':
        # Formatter les ticks de l'axe des abscisses en entiers
        axes.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: int(x)))

    if variable == 'DayOfWeek' or variable == 'Month':
        # Incline les annotations de l'axe des abscisses
        plt.xticks(rotation=45, ha='right')  # Ajout de cette ligne
        plt.tight_layout() # Ajout de cette ligne
    
    # Affichage du graphique
    plt.tight_layout()
    st.pyplot(fig)


def graphQuali_pointplot2(df, variable):
    """
    Affiche un pointplot (indication de la moyenne + IC95%) des temps (transformation Box-Cox) en fonction d'une variable catégorielle.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
    """
    var = 'boxcox_TotalResponseTime'  # Variable à tracer

    jours_semaine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    mois = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    if variable == 'DayOfWeek':
        df[variable] = pd.Categorical(df[variable], categories=jours_semaine, ordered=True)
    elif variable == 'Month':
        df[variable] = pd.Categorical(df[variable], categories=mois, ordered=True)
    elif variable == 'ratioSC':
        # Formatter les ticks de l'axe des abscisses en entiers
        axes.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: int(x)))
    
    # Création du graphique
    fig, axes = plt.subplots(1, 1, figsize=(6, 5))
    
    # Tracer le pointplot
    sns.pointplot(x=variable, y=var, data=df, ax=axes)
    
    # Titres et labels
    axes.set_title(f"Pointplot de {var} \nen fonction de {variable}")
    axes.set_xlabel(variable)
    axes.set_ylabel(var)

    if variable == 'DayOfWeek' or variable == 'Month':
        # Incline les annotations de l'axe des abscisses
        plt.xticks(rotation=45, ha='right')  # Ajout de cette ligne
        plt.tight_layout() # Ajout de cette ligne
    
    # Affichage du graphique
    plt.tight_layout()
    st.pyplot(fig)

def test_anova(df, variable):
    """
    Réalise un test d'ANOVA sur les 3 temps pour étudier l'influence d'une variable catégorielle sur ceux-ci.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à tester.
    """
    # Liste des variables sur lesquelles réaliser l'ANOVA
    var = 'boxcox_TotalResponseTime'
    
    # Pour chaque variable, on réalise un test ANOVA
    modele = var + ' ~ ' + variable
    result = ols(modele, data=df).fit()
        
    # Affichage des résultats du test ANOVA
    st.write(f"###### Test ANOVA pour étudier l'effet de {variable} sur {var}")
    anova_result = sm.stats.anova_lm(result)
        
    # Affichage du résultat dans Streamlit
    st.table(anova_result)
    st.write("\n")

def graphQuali_meanPlot(df, variable, rest):
    """
    Crée un pointplot (avec uniquement la moyenne) du temps total (transformation Box-Cox) en fonction d'une variable catégorielle,
    et l'affiche dans Streamlit. Affiche un graphique combiné si le nombre de modalités est trop grand.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
        rest (int): Nombre de valeurs à afficher (rest/2 premières et rest/2 dernières si nécessaire).
    """

    # Calculer les moyennes du temps total par valeur de variable
    mean = df.groupby(variable).agg({'boxcox_TotalResponseTime': 'mean'}).reset_index()

    # Trier par temps total moyen par ordre décroissant
    mean_times_by_borough = mean.sort_values(by='boxcox_TotalResponseTime', ascending=False)

    def create_combined_plot(data, title, var_name):
        half_rest = rest // 2
        top_half = data.head(half_rest)
        bottom_half = data.tail(half_rest)

        combined_x = list(top_half[var_name]) + ['...', '...', '...'] + list(bottom_half[var_name])
        combined_y = list(top_half['boxcox_TotalResponseTime']) + [None, None, None] + list(bottom_half['boxcox_TotalResponseTime'])

        fig = go.Figure(data=go.Line(x=combined_x, y=combined_y, name='Temps total', marker_color='green'))

        # Ajuster la taille pour correspondre à figsize=(6, 5)
        fig.update_layout(title_text=title, yaxis_title="Temps moyen", height=500, width=600)
        fig.update_xaxes(tickangle=45)

        return fig

    if rest >= len(df[variable].unique()):
        title = f"Temps total moyen (transformation Box-Cox) par {variable}"
        fig = create_combined_plot(mean_times_by_borough, title, variable)
        st.plotly_chart(fig)
    else:
        title = f"Temps total moyen (transformation Box-Cox) par {variable} \n(Combiné)"
        fig = create_combined_plot(mean_times_by_borough, title, variable)
        st.plotly_chart(fig)



def graphQuali_boxplot(df, variable):
    """
    Crée un boxplot de la distribution du temps total (transformation Box-Cox) en fonction d'une variable catégorielle,
    et l'affiche dans Streamlit.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
        variable (str): Le nom de la colonne à représenter.
    """
    var = 'boxcox_TotalResponseTime'  # Variable à tracer

    # Créer la figure
    fig, ax = plt.subplots(figsize=(6, 5))

    # Créer le boxplot
    sns.boxplot(x=variable, y=var, data=df, ax=ax)
    ax.set_title(f"Boxplot de {var} \nen fonction de {variable}")
    ax.set_xlabel(variable)
    ax.set_ylabel(var)

    plt.tight_layout()
    st.pyplot(fig)  # Afficher le graphique dans Streamlit

def afficher_correlations(df,variable):
    """
    Calcule et affiche les corrélations (Pearson, Spearman, Kendall) entre
    'boxcox_TotalResponseTime' et 'distance'.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données.
    """

    cor_pearson = df[['boxcox_TotalResponseTime', variable]].corr(method='pearson').iloc[0, 1]
    cor_spearman = df[['boxcox_TotalResponseTime', variable]].corr(method='spearman').iloc[0, 1]
    cor_kendall = df[['boxcox_TotalResponseTime', variable]].corr(method='kendall').iloc[0, 1]

    correlation = pd.DataFrame({
        'type': ['pearson', 'spearman', 'kendall'],
        'correlation': [cor_pearson, cor_spearman, cor_kendall]
    })

    st.write(correlation)