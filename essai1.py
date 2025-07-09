import pandas as pd
import streamlit as st

st.set_page_config(page_title="📊 Moyenne Totale des Notifications", layout="wide")
st.title("📈 Moyenne Générale Mensuelle des Notifications (toutes functional locations confondues)")

# 📥 Importation
fichier = st.file_uploader("Importer le fichier Excel", type=["xlsx", "xls"])

if fichier:
    df = pd.read_excel(fichier)

    if 'Notification date' in df.columns:
        df['Notification date'] = pd.to_datetime(df['Notification date'], errors='coerce')
        df.dropna(subset=['Notification date'], inplace=True)

        # 🔄 Extraire le mois et l’année
        df['YearMonth'] = df['Notification date'].dt.to_period('M')

        # 📊 Nombre total de notifications par mois
        notif_par_mois = df.groupby('YearMonth').size().reset_index(name='Total notifications')

        # 🎯 Moyenne globale des notifications par mois
        moyenne_globale = notif_par_mois['Total notifications'].mean()
        variance_globale = notif_par_mois['Total notifications'].var()

        # 🖥️ Affichage
        st.subheader("📊 Nombre total de notifications par mois")
        st.dataframe(notif_par_mois)

        st.subheader("📌 Moyenne Générale")
        st.metric("Moyenne des notifications par mois", f"{moyenne_globale:.2f}")
        st.metric("la variance  des notifications par mois", f"{variance_globale:.2f}")

    else:
        st.error("❌ La colonne 'Notification date' est manquante.")
else:
    st.info("Veuillez importer un fichier Excel contenant la colonne 'Notification date'.")
