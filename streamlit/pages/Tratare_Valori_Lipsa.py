import streamlit as st
import os
import io
import pandas as pd

# ------------- Importarea datelor -----------------------------------
# Asiguram ca fisierele clubs.csv si players.csv sunt in acelasi director cu acest script
def read_data():
    data_path = os.path.join(os.path.dirname(__file__), "clubs.csv")
    clubs = pd.read_csv(data_path)
    data_path2 = os.path.join(os.path.dirname(__file__), "players.csv")
    players = pd.read_csv(data_path2)
    return clubs, players

clubs, players = read_data()


st.title('Tratarea valorilor lipsa')
st.markdown('Tratarea valorilor lipsa pentru tabela de jucatori players.csv')
st.markdown('Afisam coloanele si daca au valori lipsa.')

def get_column_name_missing_values(data, column_name):
     return data[column_name].isna().any()

# ------------- Afisarea coloanelor cu valori lipsa -------------------
def get_columns_with_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    dict_missing_columns = {}
    for column in players.columns:
        dict_missing_columns[column] = get_column_name_missing_values(players,column)

    df_missing_columns = pd.DataFrame(list(dict_missing_columns.items()), columns=['Column', 'Has_missing_values'])
    return df_missing_columns

st.write(get_columns_with_missing_values(players))




st.markdown(r"""
   **Coloanele care contin valori lipsa:**
            
    - first_name
    - country_of_birth
    - country_of_citizenship
    - date_of_birth
    - sub_position
    - foot
    - height_in_cm
    - contract_expiration_date
    - agent_name
    - market_value_in_eur
    - highest_market_value_in_eur
    
 **Rezolvarea**
            
    Avand in vedere ca majoritatea coloanelor sunt de tip
    String, am decis sa stergem randurile in care lipseste un element de
    tip String, deoarece nu am avea cu ce sa le inlocuim.
    
    Pentru coloana **height_in_cm** am decis ca valorile lipsa sa le inlocuim cu media coloanei.
            
    Iar coloanele **market_value_in_eur** si **highest_market_value_in_eur** am decis sa inlocuim momentan valorile lipsa cu 0,
    pentru ca am vrea sa pastram randurile care au avut valori lipsa pentru a inlocui valorile lipsa cu o predictie in alte faze ale proiectului.
            

""", unsafe_allow_html=True)

st.markdown(r""" **Coloana heights_in_cm** """)

def clean_missing_values(data: pd.DataFrame, col) -> pd.DataFrame:
     if data[col].isna().any():
            if col == "foreigners_percentage":
                  data[col] = data[col].fillna(0)
            else:    
                  data[col] = data[col].fillna(data[col].mean())
     return data



players_cleaned_height = clean_missing_values(players, 'height_in_cm')
st.write(players_cleaned_height.head())

columns_with_none_values = ['first_name', 'country_of_birth', 'country_of_citizenship', 'date_of_birth', 'sub_position', 'foot', 'contract_expiration_date', 'agent_name']
players_cleaned_height.dropna(subset=columns_with_none_values, inplace=True)

st.markdown(r""" **Datele dupa stergerea randurilor cu valori lipsa mentionate mai sus**""")
st.write(players_cleaned_height)

st.markdown(r""" **Tratarea coloanelor market_value_in_eur si highest_market_value_in_eur.** """)
col1 = "market_value_in_eur"
col2 = "highest_market_value_in_eur"
if players_cleaned_height[col1].isna().any():
      players_cleaned_height[col1] = players_cleaned_height[col1].fillna(0)
if players_cleaned_height[col2].isna().any():
      players_cleaned_height[col2] = players_cleaned_height[col2].fillna(0)

st.write(players_cleaned_height.head())

st.markdown(r""" **Dupa cum vedem acum nu mai avem nicio coloana care contine valori lipsa.** """)
dict_missing_columns2 = {}
for column in players.columns:
    #  print(f'Column {column} : {get_column_name_missing_values(column)}')
    dict_missing_columns2[column] = get_column_name_missing_values(players_cleaned_height, column)

df_missing_columns2 = pd.DataFrame(list(dict_missing_columns2.items()), columns=['Column', 'Has_missing_values'])
st.write(df_missing_columns2)
# players_cleaned_height.to_csv('players_cleaned.csv', index=False)


#  ------------- FISIERUL clubs.csv --------------------------------
st.markdown(r""" **Coloanele cu valori lipsa in fisiserul clubs.csv.** """)
def get_column_name_missing_values(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
      dict_missing_columns_clubs = {}
      for column in clubs.columns:
           dict_missing_columns_clubs[column] = get_column_name_missing_values(clubs, column)
      df_missing_columns_clubs = pd.DataFrame(list(dict_missing_columns_clubs.items()), columns=['Column', 'Has_missing_values'])
      return df_missing_columns_clubs

st.write(get_column_name_missing_values(clubs))

# ----------------- Coloana total_market_value -----------------------
st.markdown(r""" **Dupa cum observam mai jos valoarea maxima a coloanei total_market_value este nan ceea ce
                 indica faptul ca toata coloana este nan, din cauza asta renuntam la acesta coloana**""")
st.write('Maxim:', clubs['total_market_value'].max())
clubs.drop('total_market_value', inplace=True, axis=1)
st.markdown("Setul de date fara coloana total_market_value:")
st.write(clubs.head())

# ------------------ Coloana coach_name -----------------------------
st.markdown(r""" Si pentru coloana coach_name exista aceeasi problema, intreaga coloana este lipsa.""")
st.write('Numarul valorilor non nule: ', clubs.loc[:, 'coach_name'].count())
st.markdown(r""" Asa ca vom proceda la fel ca la pasul cu coloana anterioara. """)
clubs.drop('coach_name', inplace=True, axis=1)
st.write(clubs.head())

# ---------------- Coloana average_age ------------------------------
clubs = clean_missing_values(clubs, 'average_age')
st.markdown(r""" **Am inlocuit valorile lipsa cu valoarea medie al coloanei average_age.** """)
st.write(clubs.head())

# -------------- Coloana foreigners_percentage ------------------------
st.write(f'Iar pentru coloana foreign_percentage avem {clubs.shape[0] - clubs['foreigners_percentage'].count()} valori lipsa.')
st.write(' In cazul asta valorile lipsa o sa fie inlocuite cu 0, fiindca exista cluburi care nu au niciun jucator strain si din cauza asta procentul este egaul cu 0.')
clubs = clean_missing_values(clubs, 'foreigners_percentage')
st.write(clubs.tail())

st.write('Dupa cum vedem mai jos nu a mai ramas nicio valoare lipsa in setul de date clubs.csv')
dict_missing_columns_clubs2 = {}
for column in clubs.columns:
      dict_missing_columns_clubs2[column] = get_column_name_missing_values(clubs, column)
df_missing_columns_clubs2 = pd.DataFrame(list(dict_missing_columns_clubs2.items()), columns=['Column', 'Has_missing_values'])
st.write(df_missing_columns_clubs2)
# clubs.to_csv('clubs_cleaned.csv', index=False)