import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TasteCompass | Mixology Analytics", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSelectbox label { color: #f0f2f6 !important; font-weight: 600; }
    h1, h2, h3 { color: #ff4b4b; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('kokteyller.csv')

df = load_data()

st.sidebar.title("TasteCompass")
st.sidebar.write("Professional flavor profile analysis for classic cocktails.")
st.sidebar.write("---")

spirit_options = sorted(df['base_spirit'].unique().tolist())
selected_spirit = st.sidebar.selectbox("Choose Base Spirit", spirit_options)

cocktail_options = df[df['base_spirit'] == selected_spirit]['name'].tolist()
selected_name = st.sidebar.selectbox("Choose Cocktail", sorted(cocktail_options))

item = df[df['name'] == selected_name].iloc[0]

st.header(item['name'])
st.write(f"Category: {item['base_spirit']} Based")
st.write("---")

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("Flavor Profile Analysis")
    
    categories = ['Sweet', 'Sour', 'Bitter', 'Boozy', 'Herbal']
    values = [item['sweet'], item['sour'], item['bitter'], item['boozy'], item['herbal']]
    
    fig = px.line_polar(r=values, theta=categories, line_close=True)
    fig.update_traces(fill='toself', line_color='#ff4b4b', marker=dict(size=8))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="#333", tickfont=dict(color="white")),
            angularaxis=dict(gridcolor="#333", tickfont=dict(color="white", size=14))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Recipe Details")
    
    st.write("**Ingredients:**")
    st.info(item['ingredients'])
    
    st.write("**Instructions:**")
    st.write(item['instructions'])
    
    st.write("---")
    
    complexity = sum(values) / 5
    st.metric("Complexity Index", f"{round(complexity, 1)} / 10")

st.sidebar.write("---")
st.sidebar.write("Developed by Utku Sener")
st.sidebar.caption("METU Statistics | Cocktail Taste Chart Dataset")