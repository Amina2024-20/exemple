import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="📊 Dashboard LafargeHolcim", layout="wide")

# --- CSS ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0a192f;
    color: #ccd6f6;
    padding: 20px 35px;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #112240;
    color: white;
    margin-left: 0px;
    border-radius: 5%;
    padding: 10px;
}
h1 { color: #64ffda; font-size: 34px; font-weight: bold; }
h3 { font-size: 18px; font-weight: 600; color: #00bcd4; margin-bottom: 10px; }
.card {
    background-color: #112240;
    border-radius: 10px;
    color:#E8c39E;
    padding: 20px 10px 10px 10px;
    box-shadow: 1px 1px 10px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0px;
}
.sidebar-logo img {
    width: 30px;
    height:30px;
    border-radius: 50%;
}
.logo-text {
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #c8ad7f;
}

/* 📱 RESPONSIVE */
@media screen and (max-width: 768px) {
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .mobile-bar {
        display: flex !important;
        flex-direction: column;
        gap: 10px;
        background-color: #112240;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
}
@media screen and (min-width: 769px) {
    .mobile-bar {
        display: none !important;
    }
}

div.stButton > button {
    width: 100%;
    height: 50px;
    background-color:#c8ad7f ;
    color: #ffffff;
    font-weight: bold;
    font-size: 16px;
    border-radius: 10px;
    border: none;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color:  #fdecda;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# --- Barre mobile horizontale
with st.container():
    st.markdown('<div class="mobile-bar">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📤 Importer un fichier Excel", type=["xlsx"], key="upload_mobile")
    colm1, colm2 = st.columns(2)
    with colm1:
        if st.button("🔔 Notifications"):
            st.session_state.mode = "notifications"
    with colm2:
        if st.button("📦 Ordres"):
            st.session_state.mode = "orders"
    st.markdown('</div>', unsafe_allow_html=True)

# --- Sidebar (PC uniquement)
st.sidebar.markdown("""
        <div class="sidebar-logo">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/LafargeHolcim_logo.svg/1280px-LafargeHolcim_logo.svg.png" alt="Logo" class="logo-img ">
            <span class="logo-text">Holcim Meknes</span>
        </div>
    """, unsafe_allow_html=True)

if "mode" not in st.session_state:
    st.session_state.mode = None

st.sidebar.markdown("---")
uploaded_file_sidebar = st.sidebar.file_uploader("📤 Importer un fichier Excel", type=["xlsx"], key="upload_sidebar")

if st.sidebar.button("🔔 Notifications", key="notif_sidebar"):
    st.session_state.mode = "notifications"
if st.sidebar.button("📦 Ordres", key="order_sidebar"):
    st.session_state.mode = "orders"

# Gestion fichier (sidebar ou mobile)
uploaded_file = uploaded_file or uploaded_file_sidebar

# --- Fonction d'affichage carte graphique
def draw_card(title, data, xlabel, ylabel, colors):
    with st.container():
        st.markdown(f'<div class="card"><h3 style="font-size:14px;text-align:center">{title}</h3>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 3))
        bars = ax.barh(data.index, data.values, color=colors, edgecolor='white', height=0.5)
        ax.set_facecolor('#0a192f')
        fig.patch.set_facecolor('#0a192f')
        ax.set_xlabel(xlabel, fontsize=10, color="#18d2a6")
        ax.set_ylabel(ylabel, fontsize=10, color='#64ffda')
        ax.tick_params(colors='#c3d1f5')
        ax.bar_label(bars, fontsize=9, color='white', fmt='%d')
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        ax.grid(axis='x', linestyle='--', alpha=0.3, color='#64ffda')
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Analyse fichier
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if st.session_state.mode == "notifications":
        if 'Notification date' in df.columns:
            df['Notification date'] = pd.to_datetime(df['Notification date'], format='%d/%m/%Y', errors='coerce')
            df['Année-Mois'] = df['Notification date'].dt.to_period('M').astype(str)
            mois_list = sorted(df['Année-Mois'].dropna().unique())
            mois_choisi = st.sidebar.selectbox("📅 Mois Notifications", mois_list, key="mois_notifications")
            df_n = df[df['Année-Mois'] == mois_choisi]

            st.markdown("## 🔔 Analyse des Notifications")
            st.markdown(f"#### Mois sélectionné : {mois_choisi}")
            st.markdown(f"- Total global : **{len(df)}** notifications")
            st.markdown(f"- Pour ce mois : **{len(df_n)}** notifications")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if 'Created by' in df_n.columns:
                    data = df_n['Created by'].dropna().value_counts()
                    colors = ["#26c6da"] * len(data)
                    draw_card("Par Créateur", data, "Nombre", "Créateur", colors)
            with col2:
                if 'Functional location' in df_n.columns:
                    data = df_n['Functional location'].astype(str).str[:6].value_counts()
                    colors = ["#ab47bc"] * len(data)
                    draw_card("Par Emplacement", data, "Nombre", "Location", colors)
            with col3:
                if 'User Status' in df_n.columns:
                    status = df_n['User Status'].fillna("Vide").astype(str)
                    data = status.value_counts()
                    colors = ["#ff7043" if s == 'Vide' else "#66bb6a" for s in data.index]
                    draw_card("Par Statut", data, "Nombre", "Statut", colors)
            with col4:
                if 'Main work center' in df_n.columns:
                    data = df_n['Main work center'].value_counts()
                    colors = ["#29b6f6"] * len(data)
                    draw_card("Par Work Center", data, "Nombre", "Centre", colors)
        else:
            st.warning("Le fichier ne contient pas la colonne 'Notification date' nécessaire.")

    elif st.session_state.mode == "orders":
        if 'Basic start date' in df.columns and 'Order' in df.columns:
            df['Basic start date'] = pd.to_datetime(df['Basic start date'], errors='coerce')
            df.dropna(subset=['Basic start date'], inplace=True)
            df['Année-Mois'] = df['Basic start date'].dt.to_period('M').astype(str)
            df['LocShort'] = df['Functional location'].astype(str).str[:6]
            mois_list_order = sorted(df['Année-Mois'].unique())
            mois_choisi_o = st.sidebar.selectbox("📅 Mois Ordres", mois_list_order, key="mois_orders")
            df_o = df[df['Année-Mois'] == mois_choisi_o]

            st.markdown("## 📦 Statistiques des Ordres")
            st.markdown(f"#### Mois sélectionné : {mois_choisi_o}")
            st.markdown(f"- Total global : **{df['Order'].nunique()}** ordres")
            st.markdown(f"- Pour ce mois : **{df_o['Order'].nunique()}** ordres")

            data = df_o.groupby("LocShort")["Order"].nunique().sort_values(ascending=True)
            colors = ["#4dd0e1"] * len(data)
            draw_card("Ordres par Emplacement", data, "Nombre", "Location", colors)
        else:
            st.warning("Le fichier ne contient pas les colonnes 'Basic start date' et/ou 'Order'.")
else:
    st.markdown("""<h4 style="margin-top:0px;padding-top:0px;color:#E8c39E; text-align:center;"> 💼 Bienvenue dans votre espace </h4>""", unsafe_allow_html=True)

# Footer
st.sidebar.markdown("""
        <hr style="border:0.5px solid #334155;">
        <p style="font-size:12px; color:#fff6ed; text-align:center;">
        © 2025 LafargeHolcim Meknès<br>
        Bureau De Méthodes<br><br>
        <span style="font-size:11px;">Développé par: <strong style="color:#E8c39E;">Amina Benkhay</strong></span>
        </p>
        """, unsafe_allow_html=True)
