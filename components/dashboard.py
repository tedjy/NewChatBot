import streamlit as st
import pandas as pd
import plotly.express as px
import json

def afficher_dashboard():

    st.markdown("""
    <style>
    .sidebar-buttons button {
        background-color: transparent;
        color: white;
        border: 1px solid #555;
        padding: 0.5rem;
        margin-bottom: 5px;
        width: 100%;
        text-align: left;
        border-radius: 0.5rem;
        transition: background-color 0.3s;
    }
    .sidebar-buttons button:hover {
        background-color: #4f8bf9;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Simulations de données - à remplacer par tes vraies données
    formations_demandes = pd.DataFrame({
        'Formation': ['Cybersécurité', 'Réseau', 'Santé', 'Commerce', 'Droit'],
        'Demandes': [120, 95, 60, 30, 15]
    })

    repartition_age = pd.DataFrame({
        'Age': ['<18', '18-21', '22-25', '26-30', '>30'],
        'Utilisateurs': [20, 55, 90, 30, 10]
    })

    repartition_geo = pd.DataFrame({
        'Ville': ['Lille', 'Paris', 'Marseille', 'Lyon', 'Bordeaux'],
        'Utilisateurs': [65, 45, 30, 25, 15]
    })

    performances_chatbot = pd.DataFrame({
        'Jour': pd.date_range(end=pd.Timestamp.today(), periods=7),
        'Requêtes traitées': [54, 63, 59, 72, 88, 95, 100],
        'Temps moyen (s)': [3.2, 2.8, 3.0, 2.7, 2.5, 2.6, 2.4]
    })

    # ✅ Charger les données JSON des formations
    with open("data/export_faiss.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame([item["metadata"] for item in data])

    st.title("📊 Tableau de bord du chatbot")

    st.sidebar.markdown("### Sections")
    sections = [
        "Vue générale", "Formations demandées", "Utilisateurs par âge",
        "Utilisateurs par ville", "Performances chatbot",
        "Domaines par villes"
    ]

    if "selected_section" not in st.session_state:
        st.session_state.selected_section = "Vue générale"

    with st.sidebar.container():
        st.markdown('<div class="sidebar-buttons">', unsafe_allow_html=True)
        for sec in sections:
            if st.button(sec, key=sec):
                st.session_state.selected_section = sec
        st.markdown('</div>', unsafe_allow_html=True)

    section = st.session_state.selected_section

    if section == "Vue générale":
        st.subheader("Tendance globale")
        col1, col2 = st.columns(2)
        col1.metric("Total demandes", formations_demandes['Demandes'].sum())
        col2.metric("Utilisateurs actifs", repartition_age['Utilisateurs'].sum())

        fig = px.pie(formations_demandes, names='Formation', values='Demandes', title="Part des formations demandées")
        st.plotly_chart(fig, use_container_width=True)

        nombre_formations = len(data)
        st.metric("📚 Formations disponibles en France", nombre_formations)

    elif section == "Formations demandées":
        st.subheader("📌 Formations les plus demandées")
        fig = px.bar(formations_demandes, x='Formation', y='Demandes', color='Formation')
        st.plotly_chart(fig, use_container_width=True)

    elif section == "Utilisateurs par âge":
        st.subheader("👥 Répartition par âge")
        fig = px.bar(repartition_age, x='Age', y='Utilisateurs', color='Age')
        st.plotly_chart(fig, use_container_width=True)

    elif section == "Utilisateurs par ville":
        st.subheader("🗽 Répartition géographique")
        fig = px.bar(repartition_geo, x='Ville', y='Utilisateurs', color='Ville')
        st.plotly_chart(fig, use_container_width=True)

    elif section == "Performances chatbot":
        st.subheader("⚙ Performances chatbot")
        st.line_chart(performances_chatbot.set_index('Jour')[['Requêtes traitées']])
        st.line_chart(performances_chatbot.set_index('Jour')[['Temps moyen (s)']])

    elif section == "Domaines par villes":
        if 'Ville' in df.columns and 'Domaine' in df.columns:
            st.subheader("🌍 Domaines les plus présents par ville")
            with st.container():
                domaine_ville = df.groupby(['Ville', 'Domaine']).size().reset_index(name="Nb_Formations")
                top_villes = domaine_ville.groupby("Ville")["Nb_Formations"].sum().nlargest(20).index.tolist()
                domaine_ville_filtre = domaine_ville[domaine_ville["Ville"].isin(top_villes)]
                domaine_ville_filtre = domaine_ville_filtre.groupby(['Ville', 'Domaine']).sum().reset_index()

                top_30_domaines_par_ville = domaine_ville_filtre.groupby('Ville').apply(
                    lambda x: x.nlargest(15, 'Nb_Formations')).reset_index(drop=True)

                fig2 = px.treemap(
                    top_30_domaines_par_ville,
                    path=['Ville', 'Domaine'],
                    values='Nb_Formations',
                    title="Répartition des domaines par ville (Sur 20 villes, Top 15 domaines/villes)",
                    color='Nb_Formations',
                    color_continuous_scale='Viridis'
                )
                fig2.update_layout(margin=dict(t=30, l=10, r=10, b=10), height=500, width=1200)
                fig2.update_traces(texttemplate='%{label}<br>%{value}', textfont_size=16, selector=dict(type='treemap'))
                st.plotly_chart(fig2, use_container_width=False)
        else:
            st.warning("❗ Impossible de générer le graphique : certaines colonnes sont absentes.")

 
