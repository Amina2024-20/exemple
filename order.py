import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="📊 Dashboard LafargeHolcim", layout="wide")

# CSS...
st.markdown("""
<style>
/* (ton CSS ici, idem ce que tu avais) */
</style>
""", unsafe_allow_html=True)

# Initialisation du mode
if "mode" not in st.session_state:
    st.session_state.mode = None

# Sidebar
st.sidebar.title("📂 Fichier Excel")
uploaded_file = st.sidebar.file_uploader("Importer un fichier Excel", type=["xlsx"])

# Boutons mode
if st.sidebar.button("📌 Notifications"):
    st.session_state.mode = "notifications"
if st.sidebar.button("📦 Ordres"):
    st.session_state.mode = "orders"

st.sidebar.markdown("---")
st.sidebar.markdown("Développé par : **Amina Benkhay**", unsafe_allow_html=True)

def draw_card(title, data, xlabel, ylabel, colors):
    with st.container():
        st.markdown(f'<div class="card"><h3 style="font-size:12px;text-align:center">{title}</h3>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 3))
        bars = ax.barh(data.index, data.values, color=colors, edgecolor='white', height=0.5)
        ax.set_facecolor('#0a192f')
        fig.patch.set_facecolor('#0a192f')
        ax.set_xlabel(xlabel, fontsize=9, color="#18d2a6")
        ax.set_ylabel(ylabel, fontsize=9, color='#64ffda')
        ax.tick_params(colors='#c3d1f5')
        ax.bar_label(bars, fontsize=8, color='white', fmt='%d')
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        ax.grid(axis='x', linestyle='--', alpha=0.3, color='#64ffda')
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if st.session_state.mode == "notifications":
        if 'Notification date' in df.columns:
            df['Notification date'] = pd.to_datetime(df['Notification date'], format='%d/%m/%Y', errors='coerce')
            df['Année-Mois'] = df['Notification date'].dt.to_period('M').astype(str)
            mois_list = df['Année-Mois'].dropna().unique()
            mois_choisi = st.sidebar.selectbox("📅 Mois Notifications", sorted(mois_list))
            df_n = df[df['Année-Mois'] == mois_choisi]

            st.markdown("## 🔔 Statistiques des Notifications")
            st.markdown(f"#### Mois sélectionné : {mois_choisi}")
            st.markdown(f"- Total global : **{len(df)}** notifications")
            st.markdown(f"- Pour ce mois : **{len(df_n)}** notifications")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if 'Created by' in df_n.columns:
                    data = df_n['Created by'].dropna().value_counts()
                    draw_card("Par Créateur", data, "Nombre", "Créateur", ["#26c6da"] * len(data))
            with col2:
                if 'Functional location' in df_n.columns:
                    data = df_n['Functional location'].astype(str).str[:6].value_counts()
                    draw_card("Par Emplacement", data, "Nombre", "Location", ["#ab47bc"] * len(data))
            with col3:
                if 'User Status' in df_n.columns:
                    status = df_n['User Status'].fillna("Vide").astype(str)
                    data = status.value_counts()
                    draw_card("Par Statut", data, "Nombre", "Statut", ["#ff7043" if s == 'Vide' else "#66bb6a" for s in data.index])
            with col4:
                if 'Main work center' in df_n.columns:
                    data = df_n['Main work center'].dropna().value_counts()
                    draw_card("Par Work Center", data, "Nombre", "Centre", ["#29b6f6"] * len(data))
        else:
            st.warning("Le fichier ne contient pas la colonne 'Notification date' nécessaire.")

    elif st.session_state.mode == "orders":
        if 'Basic start date' in df.columns and 'Order' in df.columns:
            df['Basic start date'] = pd.to_datetime(df['Basic start date'], errors='coerce')
            df.dropna(subset=['Basic start date'], inplace=True)
            df['Année-Mois'] = df['Basic start date'].dt.to_period('M').astype(str)
            df['LocShort'] = df['Functional location'].astype(str).str[:6]
            mois_list_order = df['Année-Mois'].unique()
            mois_choisi_o = st.sidebar.selectbox("📅 Mois Ordres", sorted(mois_list_order), key="mois_order")
            df_o = df[df['Année-Mois'] == mois_choisi_o]

            st.markdown("## 📦 Statistiques des Ordres")
            st.markdown(f"#### Mois sélectionné : {mois_choisi_o}")
            st.markdown(f"- Total global : **{df['Order'].nunique()}** ordres")
            st.markdown(f"- Pour ce mois : **{df_o['Order'].nunique()}** ordres")

            data = df_o.groupby("LocShort")["Order"].nunique().sort_values(ascending=True)
            draw_card("Ordres par Emplacement", data, "Nombre", "Location", ["#4dd0e1"] * len(data))
        else:
            st.warning("Le fichier ne contient pas les colonnes 'Basic start date' et/ou 'Order' nécessaires.")

else:
    st.info("📥 Veuillez importer un fichier Excel contenant les colonnes nécessaires.")
