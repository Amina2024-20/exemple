import streamlit as st
st.sidebar.markdown("""
    <div style="text-align:center; padding: 10px;">
        <img src="lafae.jpg.jpg" width="100" style="border-radius:50%;">
        <h3 style="color:#ffffff;">LafargeHolcim Meknès</h3>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Filtres")

mois = st.sidebar.selectbox("📅 Mois", ["Janvier", "Février", "Mars", "Avril"])
createur = st.sidebar.selectbox("👷‍♂️ Créateur", df["Created by"].unique())
status = st.sidebar.selectbox("📌 Statut", df["User Status"].unique())

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Résumé")
st.sidebar.metric("🔔 Total Notifications", )
st.sidebar.metric("👤 Créateurs",)
