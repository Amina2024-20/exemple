import pandas as pd
import streamlit as st

st.set_page_config(page_title="📊 Analyse Notifications par Functional Location", layout="wide")
st.title("📈 Analyse Mensuelle des Notifications par Functional Location (6 premiers caractères)")

# 📥 Importation
fichier = st.file_uploader("Importer le fichier Excel", type=["xlsx", "xls"])

if fichier:
    df = pd.read_excel(fichier)

    if 'Notification date' in df.columns and 'Functional location' in df.columns:
        # 🧹 Nettoyage des dates
        df['Notification date'] = pd.to_datetime(df['Notification date'], errors='coerce')
        df.dropna(subset=['Notification date'], inplace=True)

        # 🧱 Prendre seulement les 6 premiers caractères de la Functional location
        df['Functional location'] = df['Functional location'].astype(str).str[:6]

        # 🔄 Extraire le mois et l’année
        df['YearMonth'] = df['Notification date'].dt.to_period('M').astype(str)

        # 📊 Nombre de notifications par Functional Location et par mois
        grouped = df.groupby(['YearMonth', 'Functional location']).size().reset_index(name='Nombre de notifications')

        # 🎯 Moyenne globale des notifications
        moyenne_globale = grouped['Nombre de notifications'].mean()
        variance_globale = grouped['Nombre de notifications'].var()

        # 🖥️ Affichage
        st.subheader("📊 Nombre de notifications par mois et par Functional Location (6 caractères)")
        st.dataframe(grouped)

        st.subheader("📌 Moyenne Générale")
        st.metric("Moyenne des notifications", f"{moyenne_globale:.2f}")
        st.metric("Variance", f"{variance_globale:.2f}")

        # 📈 Graphique dynamique
        st.subheader("📉 Graphique des notifications")
        selected_location = st.selectbox("Choisir une Functional Location", grouped['Functional location'].unique())
        chart_data = grouped[grouped['Functional location'] == selected_location]

        st.line_chart(chart_data.set_index('YearMonth')['Nombre de notifications'])

    else:
        st.error("❌ Le fichier doit contenir les colonnes 'Notification date' et 'Functional location'.")
else:
    st.info("Veuillez importer un fichier Excel contenant les colonnes nécessaires.")
