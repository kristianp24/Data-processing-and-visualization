from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
import streamlit as st

data_path2 = os.path.join(os.path.dirname(__file__), "players_cleaned.csv")
players = pd.read_csv(data_path2)

st.markdown(r""" **Codificarea a datelor** """)
st.write(' Ca inceput am ales sa codificam coloanele: position si foot din setul de date pentru jucatori. ')
st.write(f' Valorile unice din coloana position: {set(players['position'].values)}')
st.write(f' Valorile unice din coloana foot: {set(players['foot'].values)}')

encoder = LabelEncoder()

st.write(' Codificarea coloanei position: ')
players['position_encoded'] = encoder.fit_transform(players['position'])
st.write(players[['position', 'position_encoded']].head())

st.write(' Codificarea coloanei foot: ')
players['foot_encoded'] = encoder.fit_transform(players['foot'])
st.write(players[['foot', 'foot_encoded']].head(10))


