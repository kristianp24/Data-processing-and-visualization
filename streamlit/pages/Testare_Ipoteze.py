import streamlit as st
from scipy import stats
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Testare ipoteze statistice")
st.markdown("In aceasta sectiune o sa testam ipoteze statistice folosind diferite testele statistice T si ANOVA.")

def genereaza_grafic_boxplot(data, x_col, y_col):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=data)
    plt.title(f'Distribuția {y_col} pe baza {x_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    st.pyplot(plt.gcf())


def atacanti_vs_fundasi(players):
    st.markdown("# Jucătorii atacanți au o valoare de piață diferită de fundași?")
    st.markdown("H0 -> Media valorii de piață a atacanților este aproximativ egală cu cea a fundașilor. ")
    st.markdown("H1 -> Media valorii de piață a atacanților este diferită de cea a fundașilor. ")
    st.markdown(" Vom folosi testul T pentru ca avem de a face cu comparatia a numai 2 grupurilor diferite.")

     # Filtrare jucatori atacanti si fundasi
    atacanti = players[players['position'].isin(['Attack'])]['market_value_in_eur']
    fundasi = players[players['position'].isin(['Defender'])]['market_value_in_eur']
    
    # Testare ipoteza
    t_stat, p_value = stats.ttest_ind(atacanti, fundasi, equal_var=False)
    
    # Afisare rezultate
    st.write(f"Statistica T: {t_stat}")
    st.write(f"Valoarea P: {p_value}")
    
    if p_value < 0.05:
        st.success("Respingem H0: Media valorii de piață a atacanților este diferită de cea a fundașilor." \
        "Exista suficiente dovezi pentru a sustine ca media valorii de piata a atacantilor este diferita de cea a fundasilor.")
    else:
        st.error("Nu respingem H0: Media valorii de piață a atacanților este aproximativ egală cu cea a fundașilor."
        "Nu exista suficiente dovezi pentru a sustine ca media valorii de piata a atacantilor este diferita de cea a fundasilor.")
    
    st.markdown("### Distribuția valorii de piață (Boxplot)")

    # Pregătire date pentru grafic
    box_data = players[players['position'].isin(['Attack', 'Defender'])][['position', 'market_value_in_eur']]

    genereaza_grafic_boxplot(box_data, 'position', 'market_value_in_eur')


def valoareaCurenta_vs_ValMax(players):
    st.markdown("# Valoarea actuală a atacantilor este semnificativ mai mică decât valoarea maximă atinsă?")
    st.markdown("H0 -> Media valorii curente este aproximativ egală cu cea a valorii maxime.")
    st.markdown("H1 -> Media valorii curente este diferită de cea a valorii maxime.")
    st.markdown("Vom folosi testul T pentru ca avem de a face cu comparatia a numai 2 grupurilor diferite.")

    # Filtrare jucatori atacanti si fundasi
    atacanti = players[players['position'].isin(['Attack'])]['market_value_in_eur']
    atacanti_highest = players[players['position'].isin(['Attack'])]['highest_market_value_in_eur']
    
    # Testare ipoteza
    t_stat, p_value = stats.ttest_ind(atacanti, atacanti_highest, equal_var=False)
    
    # Afisare rezultate
    st.write(f"Statistica T: {t_stat}")
    st.write(f"Valoarea P: {p_value}")
    
    if p_value < 0.05:
        st.success("Respingem H0: Media valorii de piață curente este diferită de cea maximă." \
        "Exista suficiente dovezi pentru a sustine ca media valorii de piata curente este diferita de cea maxima.")
    else:
        st.error("Nu respingem H0: Media valorii de piață curente este aproximativ egală cu cea maximă."
        "Nu exista suficiente dovezi pentru a sustine ca media valorii de piata curente este diferita de cea maxima.")
    
    st.markdown("### Distribuția valorii (Boxplot)")
    box_data = players[players['position'].isin(['Attack'])][['highest_market_value_in_eur', 'market_value_in_eur']]

    genereaza_grafic_boxplot(box_data, 'highest_market_value_in_eur', 'market_value_in_eur')

def diferente_valori_tari(df):
    st.markdown("# Jucătorii din anumite țări sunt mai valoroși?")
    st.markdown("**H₀** → Media valorii de piață a jucătorilor din țări diferite este aproximativ egală.")
    st.markdown("**H₁** → Media valorii de piață a jucătorilor din țări diferite este diferită.")
    st.markdown("Vom folosi **ANOVA** pentru că avem de a face cu comparația a mai multor grupuri.")

    top_countries = df['country_of_citizenship'].value_counts().head(5).index.tolist()

    df_anova = df[df['country_of_citizenship'].isin(top_countries)]

    grouped_values = [
        df_anova[df_anova['country_of_citizenship'] == country]['market_value_in_eur']
        for country in top_countries
    ]

    anova_stat, p_value_anova = stats.f_oneway(*grouped_values)

    st.write(f"**Statistica ANOVA:** {anova_stat:.4f}")
    st.write(f"**Valoarea P:** {p_value_anova:.8f}")

    if p_value_anova < 0.05:
        st.success("Respingem H₀: p_value < 0.05. Există diferențe semnificative între valorile de piață ale jucătorilor din aceste țări." \
        "Exista suficiente dovezi pentru a sustine ca media valorii de piata a jucatorilor din aceste tari este diferita.")
    else:
        st.error("Nu respingem H₀: Nu există suficiente dovezi că valorile de piață diferă semnificativ între țări."
                 "Nu exista suficiente dovezi pentru a sustine ca media valorii de piata a jucatorilor din aceste tari este diferita.")
    
    st.markdown("### Distribuția valorii de piață pe țări (Boxplot)")
    genereaza_grafic_boxplot(df_anova, 'country_of_citizenship', 'market_value_in_eur')

def picior_stang_vs_picior_drept(players):
    st.markdown("# Jucătorii care folosesc piciorul stâng au o valoare de piață diferită de cei care folosesc piciorul drept?")
    st.markdown("H0 -> Media valorii de piață a jucătorilor care folosesc piciorul stâng este aproximativ egală cu cea a celor care folosesc piciorul drept.")
    st.markdown("H1 -> Media valorii de piață a jucătorilor care folosesc piciorul stâng este diferită de cea a celor care folosesc piciorul drept.")
    st.markdown("Vom folosi testul T pentru ca avem de a face cu comparatia a numai 2 grupurilor diferite.")

    # Filtrare jucatori atacanti si fundasi
    picior_stang = players[players['foot'].isin(['left'])]['market_value_in_eur']
    picior_drept = players[players['foot'].isin(['right'])]['market_value_in_eur']
    
    # Testare ipoteza
    t_stat, p_value = stats.ttest_ind(picior_stang, picior_drept, equal_var=False)
    
    # Afisare rezultate
    st.write(f"Statistica T: {t_stat}")
    st.write(f"Valoarea P: {p_value}")
    
    if p_value < 0.05:
        st.success("Respingem H0: Media valorii de piață a jucătorilor care folosesc piciorul stâng este diferită de cea a celor care folosesc piciorul drept." \
        "Exista suficiente dovezi pentru a sustine ca media valorii de piata a jucatorilor care folosesc piciorul stang este diferita de cea a celor care folosesc piciorul drept.")
    else:
        st.error("Nu respingem H0: Media valorii de piață a jucătorilor care folosesc piciorul stâng este aproximativ egală cu cea a celor care folosesc piciorul drept."
        "Nu exista suficiente dovezi pentru a sustine ca media valorii de piata a jucatorilor care folosesc piciorul stang este diferita de cea a celor care folosesc piciorul drept.") 
    
    box_data = players[players['foot'].isin(['left', 'right'])][['foot', 'market_value_in_eur']]
    genereaza_grafic_boxplot(box_data, 'foot', 'market_value_in_eur')

def diferente_poziti_jucatori(players):
    st.markdown("# Jucătorii din diferite poziții au valori de piață diferite?")
    st.markdown("H0 -> Media valorii de piață a jucătorilor din diferite poziții este aproximativ egală.")
    st.markdown("H1 -> Media valorii de piață a jucătorilor din diferite poziții este diferită.")
    st.markdown("Vom folosi **ANOVA** pentru că avem de a face cu comparația a mai multor grupuri.")

    poziti = players['position'].unique()
    grouped_values = [players[players['position'] == poz]['market_value_in_eur'] for poz in poziti]

    anova_stat, p_value_anova = stats.f_oneway(*grouped_values)

    st.write(f"**Statistica ANOVA:** {anova_stat:.4f}")
    st.write(f"**Valoarea P:** {p_value_anova:.8f}")

    if p_value_anova < 0.05:
        st.success("Respingem H₀: p_value < 0.05. Există diferențe semnificative între valorile de piață ale jucătorilor din aceste poziții." \
        "Exista suficiente dovezi pentru a sustine ca media valorii de piata a jucatorilor din aceste pozitii este diferita.")
    else:
        st.error("Nu respingem H₀: Nu există suficiente dovezi că valorile de piață diferă semnificativ între poziții."
                 "Nu exista suficiente dovezi pentru a sustine ca media valorii de piata a jucatorilor din aceste pozitii este diferita.")
    
    st.markdown("### Distribuția valorii de piață pe poziții (Boxplot)")
    genereaza_grafic_boxplot(players, 'position', 'market_value_in_eur')
        
if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "players_cleaned.csv")
    players = pd.read_csv(data_path)
    atacanti_vs_fundasi(players)
    valoareaCurenta_vs_ValMax(players)
    diferente_valori_tari(players)
    picior_stang_vs_picior_drept(players)
    diferente_poziti_jucatori(players)
    
   