import streamlit as st
import pandas as pd
import os
import numpy as np

def load_data():
    base_path = os.path.dirname(__file__)
    clubs_path = os.path.join(base_path, "clubs.csv")
    players_path = os.path.join(base_path, "players.csv")
    clubs = pd.read_csv(clubs_path)
    players = pd.read_csv(players_path)
    return clubs, players

def show_dataframes(clubs, players):
    st.write("Dataframe cluburi:")
    st.dataframe(clubs)

    st.write("Dataframe jucatori:")
    st.dataframe(players)

def filter_by_club_name(clubs):
    st.markdown("### Filtrare dupa nume de echipa")
    nume_club = st.text_input("Introduceti numele echipei:")
    if nume_club:
        result = clubs[clubs["name"].str.contains(nume_club, case=False, na=False)]
        st.write(result)
    st.warning("Daca nu se afiseaza nimic inseamna ca nu exista echipa cu numele respectiv.")

def filter_by_player_name(players):
    st.markdown("### Filtrare dupa numele familiei unui jucator")
    nume_jucator = st.text_input("Introduceti numele jucatorului:")
    if nume_jucator:
        st.write(players[players["name"] == nume_jucator])

def filter_by_position(players):
    st.markdown("### Filtrare pentru o pozitie anume")
    pozitie = st.selectbox("Alegeti o pozitie", players["position"].unique())
    if pozitie:
        st.write(players[["name", "current_club_name", "position"]][players["position"] == pozitie])

def filter_by_age(players):
    st.markdown("### Filtrare dupa varsta")
    varsta = st.slider("Alegeti o varsta", min_value=12, max_value=50)
    if varsta:
        players["age"] = 2025 - pd.to_datetime(players["date_of_birth"]).dt.year
        st.write(players[["name", "current_club_name", "age", "market_value_in_eur"]][players["age"] == varsta])

def show_top_valuable_players(players):
    st.markdown("### Cei mai valorosi jucatori")
    top_players = players[["name", "current_club_name", "highest_market_value_in_eur"]]
    st.write(top_players.sort_values(by="highest_market_value_in_eur", ascending=False).head(10))

def show_players_from_club(players):
    st.markdown("### Afisare jucatorii dintr-o echipa")
    club = st.selectbox("Alegeti o echipa", sorted(players["current_club_name"].unique().tolist()))
    checkbox = st.checkbox("Afiseaza doar cei din ultimul an", value=False)
    if club:
        if checkbox:
            st.write(players.loc[(players["current_club_name"] == club) & (players["last_season"] == 2024),
                                 ["name", "position", "current_club_name", "last_season", "market_value_in_eur"]])
        else:
            st.write(players.loc[players["current_club_name"] == club,
                                 ["name", "position", "current_club_name", "last_season", "market_value_in_eur"]])

def filter_by_country(players):
    st.markdown("### Filtrare jucatori dupa tara de origine")
    tara = st.selectbox("Alegeti o tara", players["country_of_birth"].unique().tolist())
    if tara:
        st.write(players.loc[players["country_of_birth"] == tara,
                             ["name", "position", "current_club_name", "country_of_birth", "last_season", "market_value_in_eur"]])

st.title("Filtrari si Afisare Date")
st.markdown("In aceasta sectiune puteti filtra datele in functie de anumite criterii si afisa datele filtrate.")

clubs, players = load_data()
show_dataframes(clubs, players)
filter_by_club_name(clubs)
filter_by_player_name(players)
filter_by_position(players)
filter_by_age(players)
show_top_valuable_players(players)
show_players_from_club(players)
filter_by_country(players)
