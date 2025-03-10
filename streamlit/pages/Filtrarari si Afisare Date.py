import streamlit as st
import pandas as pd
import os
import numpy as np

st.title("Filtrari si Afisare Date")
st.markdown("In aceasta sectiune puteti filtra datele in functie de anumite criterii si afisa datele filtrate.")
#clubs = pd.read_csv("./data/clubs.csv")
# aparent nu merge daca nu e in 'working directory'

# AFISARI

data_path = os.path.join(os.path.dirname(__file__), "clubs.csv")
clubs = pd.read_csv(data_path)

st.write("Dataframe cluburi: ")
df = pd.DataFrame(clubs)
st.dataframe(df)

data_path2 = os.path.join(os.path.dirname(__file__), "players.csv")
players = pd.read_csv(data_path2)
st.write("Dataframe jucatori: ")
df2 = pd.DataFrame(players)
st.dataframe(df2)

# Filtrari


st.markdown("### Filtrare dupa nume de echipa")
nume_club = st.text_input("Introduceti numele echipei: ")
if nume_club:
    st.write(clubs[clubs["name"].str.contains(nume_club, case=False, na=False)])
st.warning("Daca nu se afiseaza nimic inseamna ca nu exista echipa cu numele respectiv.")

st.markdown("### Filtrare dupa numele familiei unui jucator")
nume_jucator = st.text_input("Introduceti numele jucatorului: ")
if nume_jucator:
    st.write(players[players["name"] == nume_jucator])

st.markdown("### Filtrare pentru o pozitie anume")
pozitie = st.selectbox("Alegeti o pozitie", players["position"].unique())
if pozitie:
    st.write(players[["name", "current_club_name", "position"]][players["position"] == pozitie])

st.markdown("### Filtrare dupa varsta")
varsta = st.slider("Alegeti o varsta", min_value=12, max_value=50)
# varsta trebuie sa o calculam, in tabel avem doar anul nasterii sub forma 1978-06-09
if varsta:
    players["age"] = 2025 - pd.to_datetime(players["date_of_birth"]).dt.year
    st.write(players[["name", "current_club_name", "age","market_value_in_eur"]][players["age"] == varsta])

st.markdown("### Cei mai valorosi jucatori")
st.write(players[["name", "current_club_name", "highest_market_value_in_eur"]].sort_values(by="highest_market_value_in_eur", ascending=False).head(10))


# Afisare jucatori din o echipa
st.markdown("### Afisare jucatorii dintr-o echipa")
club = st.selectbox("Alegeti o echipa", sorted(players["current_club_name"].unique().tolist()))
checkbox = st.checkbox("Afiseaza doar cei din ultimul an", value=False)
if club and checkbox:
    st.write(players.loc[(players["current_club_name"] == club) & (players["last_season"] == 2024), ["name", "position", "current_club_name", "last_season","market_value_in_eur"]])
elif club:
    st.write(players.loc[players["current_club_name"] == club, ["name", "position", "current_club_name", "last_season","market_value_in_eur"]])  

# Filtrare jucatori dupa tara de Origina
st.markdown("### Filtrare jucatori dupa tara de origine")
tara = st.selectbox("Alegeti o tara", players["country_of_birth"].unique().tolist())
if tara:
    st.write(players.loc[players["country_of_birth"] == tara, ["name", "position", "current_club_name", "country_of_birth","last_season","market_value_in_eur"]])



