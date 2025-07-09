import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(page_title="📊 Dashboard LafargeHolcim", layout="wide")

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
        margin:5px;
        border-radius: 5%;
        padding:0px;

    }

    [data-testid="stSidebar"] > div{
        margin-top: 0 !important;
        padding-top: 0 !important;
            
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #64ffda;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #e0f7fa;
        font-size: 14px;
    }
    h1 {
        color: #64ffda;
        font-size: 34px;
        font-weight: bold;
    }
    h3 {
        font-size: 18px;
        font-weight: 600;
        color: #00bcd4;
        margin-bottom: 10px;
    }
    .card {
        background-color: #112240;
        border-radius: 10px;
        padding: 20px;
        padding-top: 0px;
        box-shadow: 1px 1px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    
    .logo-img {
        width: 60px;
        height: 60px;
        padding-top:0px;
        border-radius: 50%;
        object-fit: cover;
    }
    .logo-text {
        font-size: 18px;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
        <div class="sidebar-logo">
            <img src="data:image/jpeg;base64,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" alt="Logo" class="logo-img ">
            <span class="logo-text" style=" letter-spacing: 3px">Holcim Meknes</span>
        </div>
    """, unsafe_allow_html=True)
st.sidebar.markdown("---")

username = st.sidebar.text_input("👤 Nom", "younesse fatimi")
st.sidebar.success(f" Bienvenue {username}")
uploaded_file = st.sidebar.file_uploader("📤 Importer un fichier Excel", type=["xlsx"])
with st.sidebar.expander("🔔 Notifications", expanded=False):
    show_createurs = st.checkbox("📌 Créateurs", value=True)
    show_functional = st.checkbox("🏭 Functional Location", value=True)
    show_status = st.checkbox("⚙️ Statut Utilisateur", value=True)
    show_workcenter = st.checkbox("🔧 Work Center", value=True)
    show_addit = st.checkbox("", value=True)

st.sidebar.markdown("---")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if 'Notification date' in df.columns:
        df['Notification date'] = pd.to_datetime(df['Notification date'], format='%d/%m/%Y', errors='coerce')
        df['Année-Mois'] = df['Notification date'].dt.to_period('M').astype(str)
        mois_disponibles = df['Année-Mois'].sort_values().unique().tolist()

        mois_choisi = st.sidebar.selectbox("📅 Sélectionner un mois", mois_disponibles)
        df_filtered = df[df['Année-Mois'] == mois_choisi]
        total_notifications = len(df)
        total_notifications_mois = len(df_filtered)
        st.markdown("## 📈 Statistiques mensuelles")
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; background-color: #112240; padding: 15px 25px; border-radius: 12px; margin-bottom: 20px;">
            <div style="text-align: center;">
                <h4 style="color: #64ffda;">📊 Total notifications</h4>
                <p style="font-size: 26px; color: white; margin-top: -10px;">{total_notifications}</p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #64ffda;">📅 Total ({mois_choisi})</h4>
                <p style="font-size: 26px; color: white; margin-top: -10px;">{total_notifications_mois}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 🔍 Résultats pour le mois : {mois_choisi}")
        st.sidebar.markdown("""
        <hr style="border:0.5px solid #334155;">
        <p style="font-size:12px; color:#94a3b8; text-align:center;">
        © 2025 LafargeHolcim Meknès<br>
        Bureau Méthodes<br><br>
        <span style="font-size:11px;">Développé par: <strong style="color:#facc15;">Amina Benkhay</strong></span>
        </p>
        """, unsafe_allow_html=True)
        def draw_card(title, data, xlabel, ylabel, colors):
            with st.container():
                st.markdown(f'<div class="card"><h3 style="font-size:10px;text-align:center">{title}</h3>', unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(4, 3))
                bars = ax.barh(data.index, data.values, color=colors, edgecolor='white', height=0.5)
                ax.set_facecolor('#0a192f')
                fig.patch.set_facecolor('#0a192f')
                ax.set_xlabel(xlabel, fontsize=9, color="#18d2a6")
                ax.set_ylabel(ylabel, fontsize=9, color='#64ffda')
                ax.tick_params(colors='#c3d1f5')
                ax.bar_label(bars, fontsize=8, color='white')
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
                ax.grid(axis='x', linestyle='--', alpha=0.3, color='#64ffda')
                plt.tight_layout()
                st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        if show_createurs and 'Created by' in df_filtered.columns:
            with col1:
                data = df_filtered['Created by'].dropna().value_counts()
                couleur = ["#1e961c" if 25 < val < 75 else "#f32125" for val in data.values]
                draw_card("Notifications par Créateurs", data, "Nombre", "Créateur", couleur)

        if show_functional and 'Functional location' in df_filtered.columns:
            with col2:
                df_subset = df_filtered[['Notification', 'Functional location']].dropna()
                df_subset['Functional location'] = df_subset['Functional location'].astype(str).str[:6]
                data = df_subset['Functional location'].value_counts()
                couleur = ['#1e88e5'] * len(data)
                draw_card("Functional Location", data, "Nombre", "Emplacement", couleur)

        if show_status and 'User Status' in df_filtered.columns:
            with col3:
                status_series = df_filtered['User Status'].fillna('Vide')
                data = status_series.value_counts()
                couleur = ["#88ff64" if val == 'CPM' else "#f34f21" if val == 'Vide' else '#546e7a' for val in data.index]
                draw_card("Statut Utilisateur", data, "Nombre", "Statut", couleur)

        if show_workcenter and 'Main work center' in df_filtered.columns:
            with col4:
                data = df_filtered['Main work center'].dropna().value_counts()
                couleur = ['#00bcd4'] * len(data)
                draw_card("Work Center", data, "Nombre", "Centre", couleur)

