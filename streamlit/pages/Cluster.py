import streamlit as st
from scipy import stats
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


st.title("Clusterizare")
st.markdown("În această secțiune vom clusteriza jucătorii și cluburile folosind KMeans.")

# KMeans
def kmeans(players):
    st.markdown("# KMeans --> Clusterizare jucătorilor")
    st.markdown("Clusterizăm jucătorii în funcție de vârstă și valoarea de piață.")


    players['age'] = 2025 - pd.to_datetime(players['date_of_birth'], errors='coerce').dt.year # nu avem age, dar calculam dupa data nastere
    players = players[['name', 'market_value_in_eur', 'age']].dropna()

    # alegem nr de clustere dorit
    n_clusters = st.slider("Selectează numărul de clustere:", min_value=2, max_value=8, value=3)

    # KMeans
    X = players[['market_value_in_eur', 'age']]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    players['cluster'] = kmeans.fit_predict(X)

    # grafic de tip scatter
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=players, x='market_value_in_eur', y='age', hue='cluster', palette='tab10', s=100)
    plt.title("Clusterizare jucători în funcție de vârstă și valoare de piață")
    plt.xlabel("Valoare de piață (€)")
    plt.ylabel("Vârstă")
    plt.grid(True)
    st.pyplot(plt.gcf())

    # boxplot-uri
    st.markdown("### Distribuții per cluster")
    genereaza_grafic_boxplot(players, 'cluster', 'market_value_in_eur')
    genereaza_grafic_boxplot(players, 'cluster', 'age')

    # ANOVA pentru fiecare variabilă
    st.markdown("### Testare diferențe semnificative (ANOVA)")

    for feature in ['market_value_in_eur', 'age']:
        st.write(f"**Variabilă analizată:** `{feature}`")
        group_data = [players[players['cluster'] == i][feature] for i in range(n_clusters)]
        f_stat, p_value = stats.f_oneway(*group_data)

        st.write(f"Statistica F: {f_stat:.4f} | p-valoare: {p_value:.4f}")
        if p_value < 0.05:
            st.success("Respingem H0: Există diferențe semnificative între grupuri.")
        else:
            st.warning("Nu respingem H0: Nu există diferențe semnificative între grupuri.")



def genereaza_grafic_boxplot(data, x_col, y_col):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=data)
    plt.title(f'Distribuția {y_col} pe baza {x_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    st.pyplot(plt.gcf())



# cluburi
# conversie valoare transfer
def parse_transfer_value(value):
    try:
        value = value.replace('€', '').replace('+', '').replace('m', 'e6').replace('k', 'e3')
        return float(eval(value))
    except:
        return np.nan

# KMEANS Cluburi
def kmeans_clubs(df_clubs):
    st.write("Dataframe cluburi:")
    st.dataframe(df_clubs)

    df_clubs['net_transfer_record_num'] = df_clubs['net_transfer_record'].apply(parse_transfer_value)

    features = [
        'squad_size', 'average_age', 'foreigners_number',
        'foreigners_percentage', 'national_team_players',
        'stadium_seats', 'net_transfer_record_num'
    ]

    df_clean = df_clubs[features + ['name']].dropna()


    n_clusters = st.slider("Alege numărul de clustere", min_value=2, max_value=10, value=4, step=1)


    max_cluburi = st.slider("Afișează maxim câte cluburi?", 10, len(df_clean), 20, step=1)
    df_subset = df_clean.head(max_cluburi)


    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_subset[features])

    # KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df_subset['cluster'] = clusters

    st.write("Rezultate clusterizare cluburi:")
    st.dataframe(df_subset[['name', 'cluster'] + features])

    # PCA pentru vizualizare
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Scatter cu etichete
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    scatter = ax1.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='Set1', s=100)

    for i, txt in enumerate(df_subset['name']):
        ax1.annotate(f"{txt} (C{clusters[i]})", (X_pca[i, 0], X_pca[i, 1]), fontsize=8)

    ax1.set_title(f"KMeans cu {n_clusters} clustere")
    ax1.set_xlabel("PCA 1")
    ax1.set_ylabel("PCA 2")
    st.pyplot(fig1)

    # bar chart
    cluster_counts = df_subset['cluster'].value_counts().sort_index()

    fig2, ax2 = plt.subplots()
    cluster_counts.plot(kind='bar', color='skyblue', ax=ax2)
    ax2.set_title("Număr de cluburi per cluster")
    ax2.set_xlabel("Cluster")
    ax2.set_ylabel("Număr cluburi")
    ax2.grid(axis='y')
    st.pyplot(fig2)

    st.markdown("### Test ANOVA pentru varsta medie (average_age)")
    st.markdown("**Ipoteze:**")
    st.markdown("- H0: Nu există diferențe semnificative între mediile grupurilor.")
    st.markdown("- H1: Există cel puțin un grup care diferă semnificativ.")

    group_data = [group['average_age'].values for name, group in df_subset.groupby('cluster')]

    f_stat, p_value = stats.f_oneway(*group_data)

    st.write(f"Statistica F: {f_stat:.4f}")
    st.write(f"P-value: {p_value:.4g}")

    if p_value < 0.05:
        st.success("Respingem H0: Există diferențe semnificative între clustere.")
    else:
        st.error("Nu putem respinge H0: Nu există diferențe semnificative între clustere.")




if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "players_cleaned.csv")
    players = pd.read_csv(data_path)

    data_path2 = os.path.join(os.path.dirname(__file__), "clubs_cleaned.csv")
    clubs = pd.read_csv(data_path2)

    st.title("Analiză jucători și cluburi")

    st.header("Jucători")
    st.write("Dataframe jucători:")
    st.dataframe(players)
    kmeans(players)


    st.header("Cluburi")
    kmeans_clubs(clubs)


