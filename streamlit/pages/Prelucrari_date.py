import streamlit as st
import os
import pandas as pd

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "clubs.csv")
    clubs = pd.read_csv(data_path)
    data_path2 = os.path.join(os.path.dirname(__file__), "players_cleaned.csv")
    players = pd.read_csv(data_path2)
    return clubs, players

def show_height_distribution(players):
    st.markdown('### Distributia inaltimilor jucatorilor')
    st.markdown(':blue-background[Media, mediana si deviatia standard] a inaltimii in functie de pozitia jucatorilor.')
    st.markdown('Compararea distributiei inaltimilor pentru diferite ligi.')

    st.markdown('**Media inaltimii in functie de pozitia jucatorilor**')
    st.write(players.groupby('position')['height_in_cm'].mean())

    st.markdown('**Mediana inaltimii in functie de pozitia jucatorilor**')
    st.write(players.groupby('position')['height_in_cm'].median())

    st.markdown('**Deviatia standard a inaltimii in functie de pozitia jucatorilor**')
    st.write(players.groupby('position')['height_in_cm'].std())

    st.line_chart(players.groupby('position')['height_in_cm'].mean())
    st.info('Observam ca portarii sunt cei mai inalti jucatori.')
    st.divider()

def show_market_value_by_league(players):
    st.markdown('### Valoarea de piata a jucatorilor per liga')
    st.markdown(':blue-background[Valoarea medie] a jucatorilor pe fiecare competitie interna (current_club_domestic_competition_id).')
    st.markdown('Top 5 ligi cu cea mai mare valoare medie a jucatorilor.')

    st.markdown('**Valoarea medie a jucatorilor pe fiecare competitie interna**')
    st.write(players.groupby('current_club_domestic_competition_id')['market_value_in_eur'].mean())

    st.markdown('**Top 5 ligi cu cea mai mare valoare medie a jucatorilor**')
    st.write(players.groupby('current_club_domestic_competition_id')['market_value_in_eur'].mean().nlargest(5))
    st.info('Observam ca valoarea medie a jucatorilor este cea mai mare in Premier League (Great Britain 1).')
    st.divider()

def show_market_value_by_country(players):
    st.markdown('### Tarile cu cei mai valorosi jucatori')
    st.markdown(':blue-background[Media valorii] de piata pe tara de cetatenie (country_of_citizenship).')
    st.markdown('Top 10 tari cu cei mai valorosi jucatori.')

    st.markdown('**Media valorii de piata pe tara de cetatenie**')
    st.write(players.groupby('country_of_citizenship')['market_value_in_eur'].mean())

    st.markdown('**Top 10 tari cu cei mai valorosi jucatori**')
    st.write(players.groupby('country_of_citizenship')['market_value_in_eur'].mean().nlargest(10))

    st.area_chart(players.groupby('country_of_citizenship')['market_value_in_eur'].mean())
    st.divider()

def show_other_statistics(players):
    st.markdown('### Alte grupari sau prelucrari statistice')
    st.markdown('Aici puteti vizualiza alte grupari sau prelucrari statistice.')

    st.markdown('**Media valorii de piata pe pozitie**')
    st.write(players.groupby('position')['market_value_in_eur'].mean())

    st.markdown('**Mediana valorii de piata pe pozitie**')
    st.write(players.groupby('position')['market_value_in_eur'].median())

    st.markdown('**Deviatia standard a valorii de piata pe pozitie**')
    st.write(players.groupby('position')['market_value_in_eur'].std())

    st.markdown('**Top 10 echipe cu cei mai valorosi jucatori**')
    st.write(players.groupby('current_club_name')['market_value_in_eur'].mean().nlargest(10))

    st.markdown('### Grafic bar chart si line chart pentru valoarea medie a jucatorilor pe pozitie')
    st.bar_chart(players.groupby('position')['market_value_in_eur'].mean())
    st.line_chart(players.groupby('position')['market_value_in_eur'].mean())
    st.divider()

def show_foot_analysis(players):
    st.markdown('### Distribuția jucătorilor pe piciorul de bază')
    st.markdown('Câți sunt dreptaci, stângaci și câți folosesc ambele picioare.')
    foot_counts = players['foot'].value_counts()
    st.bar_chart(foot_counts)

    st.markdown('### Compararea valorii de piață între jucătorii dreptaci și stângaci')
    market_value_comparison = players[players['foot'].isin(['right', 'left'])]
    st.bar_chart(market_value_comparison.groupby('foot')['market_value_in_eur'].mean())
    st.divider()

def show_active_vs_retired(players):
    st.markdown('### Jucători activi vs retrași')
    st.markdown('Distribuția jucătorilor în funcție de last_season.')
    last_season_counts = players['last_season'].value_counts()
    st.bar_chart(last_season_counts)

    st.markdown('### Diferența de valoare de piață între jucătorii retrași și cei activi')
    active_vs_retired = players.copy()
    active_vs_retired['status'] = active_vs_retired['last_season'].apply(lambda x: 'Active' if pd.isna(x) or x >= 2024 else 'Retired')
    st.bar_chart(active_vs_retired.groupby('status')['market_value_in_eur'].mean())
    st.divider()

def show_age_market_analysis(players):
    st.markdown('### Vârsta și valoarea de piață')
    players['age'] = 2024 - pd.to_datetime(players['date_of_birth']).dt.year
    players['age_category'] = pd.cut(players['age'], bins=[15, 20, 25, 30, 35, 40, 50], labels=['15-20', '21-25', '26-30', '31-35', '36-40', '40+'])
    st.bar_chart(players.groupby('age_category')['market_value_in_eur'].mean())

    st.markdown('### Vârsta cu cea mai mare valoare de piață medie')
    peak_age = players.groupby('age')['market_value_in_eur'].mean().idxmax()
    st.success(f'Vârsta cu cea mai mare valoare de piață medie este: {peak_age} ani')


clubs, players = load_data()
st.header('Prelucrari :green[date]', divider="green")
st.markdown('Aici puteti vizualiza diferite prelucrari de :green[date].')

show_height_distribution(players)
show_market_value_by_league(players)
show_market_value_by_country(players)
show_other_statistics(players)
show_foot_analysis(players)
show_active_vs_retired(players)
show_age_market_analysis(players)
