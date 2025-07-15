import pandas as pd
import streamlit as st

st.set_page_config(page_title="📊 Seuils par mois et location", layout="wide")

st.title("📈 Analyse des Seuils par Mois et Functional Location")

# 📥 Uploader fichier Excel
uploaded_file = st.file_uploader("📤 Importer un fichier Excel contenant les notifications", type=["xlsx"])

if uploaded_file:
    # Charger les données
    df = pd.read_excel(uploaded_file)

    # Vérifier colonnes nécessaires
    if 'Notification date' in df.columns and 'Functional location' in df.columns:
        # Nettoyage et préparation
        df['Notification date'] = pd.to_datetime(df['Notification date'], errors='coerce')
        df['Année-Mois'] = df['Notification date'].dt.to_period('M').astype(str)
        df['LocShort'] = df['Functional location'].astype(str).str[:6]  # premiers 6 caractères

        # Notifications par mois et FL
        notif_par_mois_fl = df.groupby(['Année-Mois', 'LocShort']).size().reset_index(name='Nb_notifications')

        # Calcul du seuil = moyenne des notifications par FL et mois
        seuils = notif_par_mois_fl.groupby(['LocShort', 'Année-Mois'])['Nb_notifications'].mean().reset_index()
        seuils.rename(columns={'Nb_notifications': 'Seuil'}, inplace=True)

        # Fusion des données
        df_final = notif_par_mois_fl.merge(seuils, on=['LocShort', 'Année-Mois'])

        # Marquer anomalie si dépassement du seuil
        df_final['Anomalie'] = df_final['Nb_notifications'] > df_final['Seuil']

        # Calcul moyenne totale (globale) par FL sur toute la période
        nb_mois = df['Année-Mois'].nunique()
        total_notifications_par_fl = df.groupby('LocShort').size().reset_index(name='Total_notifications')
        total_notifications_par_fl['Moyenne_totale'] = total_notifications_par_fl['Total_notifications'] / nb_mois

        # Affichage des résultats
        st.success("✅ Analyse terminée avec succès !")
        st.markdown("### Tableau des notifications mensuelles avec seuils et anomalies")
        st.dataframe(df_final)

        st.markdown("### Moyenne totale (globale) des notifications par Functional Location")
        st.dataframe(total_notifications_par_fl)

        # Choix Functional Location
        st.markdown("### Visualisation des seuils par mois pour chaque Functional Location")
        fl_list = df_final['LocShort'].unique()
        fl_selected = st.selectbox("Choisir une Functional Location", fl_list)

        df_fl = df_final[df_final['LocShort'] == fl_selected].set_index('Année-Mois')
        st.line_chart(df_fl[['Nb_notifications', 'Seuil']])

        # Nouvelle partie : afficher moyenne totale pour la FL sélectionnée
        moyenne_fl = total_notifications_par_fl.loc[total_notifications_par_fl['LocShort'] == fl_selected, 'Moyenne_totale'].values
        if len(moyenne_fl) > 0:
            st.markdown(f"#### Moyenne totale pour la Functional Location **{fl_selected}** sur toute la période : **{moyenne_fl[0]:.2f}**")
        else:
            st.markdown("Aucune donnée pour cette Functional Location.")

    else:
        st.error("❌ Le fichier doit contenir les colonnes 'Notification date' et 'Functional location'")
else:
    st.info("📁 Veuillez importer un fichier Excel contenant les notifications.")
