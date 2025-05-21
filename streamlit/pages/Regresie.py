import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def load_data():
    df = pd.read_csv('pages/players_cleaned.csv', parse_dates=['date_of_birth'], dayfirst=True)
    
    df['age'] = df['last_season'] - df['date_of_birth'].dt.year
    
    df = df.dropna(subset=['height_in_cm', 'market_value_in_eur', 'age'])
    return df


df = load_data()


st.title('Regresie pentru valoare jucatorului')
st.write('Foloseste regresia simpla sau multipla')


st.sidebar.header('Configurarea Modelului')
model_type = st.sidebar.selectbox('Alegeti modelul de regresie', ['Simple Regression', 'Multiple Regression'])


def get_features():
    if model_type == 'Simple Regression':
        return ['height_in_cm']
    else:
        
        return st.sidebar.multiselect('Selectati variabile', ['height_in_cm', 'age'], default=['height_in_cm', 'age'])

features = get_features()
if not features:
    st.sidebar.error('Va rugam sa selectati macar o variabila.')
    st.stop()


y = df['market_value_in_eur']
X = df[features]


if st.sidebar.button('Vizualizeaza Model'):
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    coef = model.coef_
    intercept = model.intercept_
    r2 = r2_score(y, y_pred)

    
    st.subheader(f'{model_type} Results')
    st.write('**Features and Coefficients:**')
    for feat, c in zip(features, coef):
        st.write(f'- {feat}: {c:,.2f}')
    st.write(f'**Intercept:** {intercept:,.2f}')
    st.write(f'**R² Score:** {r2:.4f}')

    
    fig, ax = plt.subplots()
    ax.scatter(y, y_pred, alpha=0.5)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], '--', linewidth=2)
    ax.set_xlabel('Actual Market Value (EUR)')
    ax.set_ylabel('Predicted Market Value (EUR)')
    ax.set_title('Actual vs. Predicted')
    st.pyplot(fig)

else:
    st.write('Configure your model in the sidebar and click **Show Model**.')