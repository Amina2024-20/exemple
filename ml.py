import pandas as pd
import streamlit as st

st.set_page_config(page_title="📊 Analyse Notifications par Mois et Axe", layout="wide")
st.title("Analyse notifications avec seuils min et max par mois et axe")

uploaded_file = st.file_uploader("Importer fichier Excel (.xlsx, .xls)", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    needed_cols = ['Notification date', 'Functional location', 'Created by', 'Main work center', 'User Status', 'Notification']
    if not all(col in df.columns for col in needed_cols):
        st.error(f"Le fichier doit contenir ces colonnes : {needed_cols}")
    else:
        df['Notification date'] = pd.to_datetime(df['Notification date'], errors='coerce')
        df = df.dropna(subset=['Notification date'])
        df['Month'] = df['Notification date'].dt.to_period('M').astype(str)

        mois_choisi = st.selectbox("Choisir un mois", sorted(df['Month'].unique()))

        axe_options = {
            'Functional location (6ème caractère)': 'Functional location',
            'Créateur': 'Created by',
            'Work Center': 'Main work center',
            'User Status': 'User Status'
        }
        axe_label = st.selectbox("Choisir l'axe d'analyse", list(axe_options.keys()))
        axe_col = axe_options[axe_label]

        df_mois = df[df['Month'] == mois_choisi].copy()

        if axe_col == 'Functional location':
            df_mois['FL_char6'] = df_mois['Functional location'].str[5]
            group_col = 'FL_char6'
        elif axe_col == 'User Status':
            df_mois[axe_col] = df_mois[axe_col].fillna('Inconnu')
            df_mois.loc[df_mois[axe_col].str.strip() == '', axe_col] = 'Inconnu'
            group_col = axe_col
        else:
            group_col = axe_col

        df_group = df_mois.groupby(group_col).size().reset_index(name='Nb_Notifications')

        moy = df_group['Nb_Notifications'].mean()
        std = df_group['Nb_Notifications'].std()

        seuil_min = moy - 1.5 * std if not pd.isna(std) else moy
        seuil_max = moy + 1.5 * std if not pd.isna(std) else moy

        def classify(x):
            if x < seuil_min:
                return 'Anormal (trop bas)'
            elif x > seuil_max:
                return 'Anormal (trop haut)'
            else:
                return 'Normal'

        df_group['Anomalie'] = df_group['Nb_Notifications'].apply(classify)

        st.markdown(f"**Seuil minimum = {seuil_min:.2f} | Seuil maximum = {seuil_max:.2f} pour {axe_label} en {mois_choisi}**")

        st.dataframe(df_group.sort_values(by='Nb_Notifications', ascending=False))

        if st.checkbox("Afficher uniquement les anomalies"):
            st.dataframe(df_group[df_group['Anomalie'] != 'Normal'])
