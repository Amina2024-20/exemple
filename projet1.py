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
    margin: 5px;
    border-radius: 5%;
    padding: 10px;
}
h1 { color: #64ffda; font-size: 34px; font-weight: bold; }
h3 { font-size: 18px; font-weight: 600; color: #00bcd4; margin-bottom: 10px; }
.card {
    background-color: #112240;
    border-radius: 10px;
    padding: 20px 10px 10px 10px;
    box-shadow: 1px 1px 10px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}
.sidebar-logo img {
    width: 40px;
    border-radius: 5px;
}
.logo-text {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #64ffda;
}

/* 📱📲 RESPONSIVE LAYOUT */
@media screen and (max-width: 768px) {
    .css-1kyxreq, .css-1x8cf1d {
        flex-direction: column !important;
    }
    .card {
        padding: 15px 10px;
    }
    h1 { font-size: 24px !important; }
    h3 { font-size: 16px !important; }
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("""
        <div class="sidebar-logo">
            <img src="data:image/jpeg;base64,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" alt="Logo" class="logo-img ">
            <span class="logo-text" style=" letter-spacing: 3px">Holcim Meknes</span>
        </div>
    """, unsafe_allow_html=True)

# Boutons pour choisir mode (Notifications / Ordres)
if "mode" not in st.session_state:
    st.session_state.mode = None
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📤 Importer un fichier Excel", type=["xlsx"])



if st.sidebar.button("🔔 Notifications"):
    st.session_state.mode = "notifications"
if st.sidebar.button("📦 Ordres"):
    st.session_state.mode = "orders"


# Fonction pour dessiner les graphiques en cards
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

# Chargement fichier

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if st.session_state.mode == "notifications":
        if 'Notification date' in df.columns:
            df['Notification date'] = pd.to_datetime(df['Notification date'], format='%d/%m/%Y', errors='coerce')
            df['Année-Mois'] = df['Notification date'].dt.to_period('M').astype(str)
            mois_list = sorted(df['Année-Mois'].dropna().unique())
            mois_choisi = st.sidebar.selectbox("📅 Mois Notifications", mois_list, key="mois_notifications")
            df_n = df[df['Année-Mois'] == mois_choisi]

            st.markdown("## 🔔 Analyse  des Notifications")
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
                    data = df_n['Main work center'].dropna().value_counts()
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
            st.warning("Le fichier ne contient pas les colonnes 'Basic start date' et/ou 'Order' nécessaires.")
else:
    st.info("📥 Veuillez importer un fichier Excel contenant les colonnes nécessaires.")
st.sidebar.markdown("""
        <hr style="border:0.5px solid #334155;">
        <p style="font-size:12px; color:#94a3b8; text-align:center;">
        © 2025 LafargeHolcim Meknès<br>
        Bureau Méthodes<br><br>
        <span style="font-size:11px;">Développé par: <strong style="color:#facc15;">Amina Benkhay</strong></span>
        </p>
        """, unsafe_allow_html=True)
