import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Dashboard Performance", layout="wide")

# Design CSS
st.markdown("""
    <style>
    .kpi {
        font-size: 32px;
        color: #64ffda;
        text-align: center;
    }
    .kpi-title {
        font-size: 16px;
        text-align: center;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Génération des données simulées
np.random.seed(42)
df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=100),
    "Production": np.random.randint(100, 1000, size=100),
    "Créateur": np.random.choice(["Amina", "Sara", "Yassine", "Ali"], size=100),
    "Statut": np.random.choice(["Validé", "En attente", "Rejeté"], size=100)
})

# Sidebar
st.sidebar.header("Filtres")
selected_creator = st.sidebar.multiselect("🎨 Choisir créateur :", df["Créateur"].unique(), default=df["Créateur"].unique())
selected_status = st.sidebar.multiselect("📦 Statut :", df["Statut"].unique(), default=df["Statut"].unique())

df_filtered = df[df["Créateur"].isin(selected_creator) & df["Statut"].isin(selected_status)]

# KPI
col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='kpi'>{df_filtered['Production'].sum()}</div>", unsafe_allow_html=True)
col1.markdown("<div class='kpi-title'>Production totale</div>", unsafe_allow_html=True)

col2.markdown(f"<div class='kpi'>{df_filtered['Créateur'].nunique()}</div>", unsafe_allow_html=True)
col2.markdown("<div class='kpi-title'>Créateurs actifs</div>", unsafe_allow_html=True)

col3.markdown(f"<div class='kpi'>{df_filtered.shape[0]}</div>", unsafe_allow_html=True)
col3.markdown("<div class='kpi-title'>Entrées filtrées</div>", unsafe_allow_html=True)

# Graphique
st.subheader("📈 Production dans le temps")
fig = px.line(df_filtered, x="Date", y="Production", color="Créateur", markers=True)
st.plotly_chart(fig, use_container_width=True)
