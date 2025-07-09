import streamlit as st

# --- Formulaire de contact dans un popup modal ---
@st.experimental_dialog("Contact Me")
def show_contact_form():
    with st.form("contact_form"):
        name = st.text_input("Votre nom")
        email = st.text_input("Votre email")
        message = st.text_area("Votre message")
        submitted = st.form_submit_button("Envoyer")

        if submitted:
            st.success(f"Merci {name}, votre message a été envoyé !")

# --- Interface principale ---
def main():
    col1, col2 = st.columns([1, 2], gap="small", vertical_alignment="center")

    with col1:
        st.image("https://avatars.githubusercontent.com/u/9919?s=280&v=4", width=150)  # Image exemple

    with col2:
        st.title("Sven Bosau")
        st.write("Senior Data Analyst, assisting enterprises by supporting data-driven decision-making.")

        if st.button("✉️ Contact Me"):
            show_contact_form()

    st.markdown("---")
    st.subheader("Experience & Qualifications")
    st.write("""
    - 7 Years experience extracting actionable insights from data
    - Strong hands-on experience and knowledge in Python and Excel
    - Good understanding of statistical principles and their respective applications
    - Excellent team-player and displaying a strong sense of initiative on tasks
    """)

    st.subheader("Hard Skills")
    st.write("""
    - Programming: Python (Scikit-learn, Pandas), SQL, VBA
    - Data Visualization: PowerBi, MS Excel, Plotly
    - Modeling: Logistic regression, linear regression, decision trees
    - Databases: Postgres, MongoDB, MySQL
    """)

if __name__ == "__main__":
    main()
