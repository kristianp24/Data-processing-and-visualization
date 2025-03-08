import streamlit as st

st.title('Proiect Pachete Software')
st.header(' O scurta prezentare a datelor')
st.markdown(r"""
    Acest proiect isi propune sa prezinte un set de date referitoare niste date legat de niste echipe de fotbal disponibile 
    la **https://www.kaggle.com/datasets/davidcariboo/player-scores**.
   
    **- Tabele luate in considerare:**
    - players.csv
    - clubs.csv
    
     **-Informatii despre coloanele la fiecare tabel:**
     - players.csv: Contine infromatii legat de jucatorii din diferite echipe de fotbal.
        - player_id: id-ul jucatorului
        - first_name: prenumele jucatorului
        - last_name: numele jucatorului
        - name: numele complet al jucatorului  
        - last_season: sezonul in care a jucat ultima data
        - current_club_id: id-ul echipei la care joaca in prezent          
        - player_code: codul jucatorului
        - country_of_birth: tara de nastere a jucatorului   
        - city_of_birth: orasul de nastere a jucatorului
        - country_of_citizenship: tara de cetatenie a jucatorului 
        
     - clubs.csv: Contine informatii legate de echipele de fotbal.
        - club_id: id-ul echipei
        - club_code: codul echipei
        - club_name: numele echipei
        - domestic_competition: liga in care joaca echipa
        - total_market_value: valoarea totala a echipei (Null, asa ca este scoasa din DataFrame )
        - squad_size: numarul de jucatori din echipa
        - average_age: varsta medie a jucatorilor din echipa
        - foreigners_number: numarul de jucatori straini din echipa   
        - foreigner_percentage: procentajul de jucatori straini din echipa
        - national_team_players: numarul de jucatori care joaca in echipa nationala

     Datele sunt preluate de pe Kaggle si sunt disponibile pentru download la link-ul de mai sus. Sursa de date este **Transfermarkt**.   
            
            """, unsafe_allow_html=True)
