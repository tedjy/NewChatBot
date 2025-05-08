from components.dashboard import afficher_dashboard
import streamlit as st
import time 
from components.gen_llm_response import generate_llm_response


def interface(model_fn):
 # Ajout du fond d'écran doux gris clair
     # Ajout du fond d'écran doux gris clair
    st.markdown("""
    <style>
    body, .stApp {
        background-color: #343232;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .chat-message {
        position: relative;
        padding: 0.8rem 1.2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        max-width: 70%;
        word-wrap: break-word;
        animation: pop 0.3s ease;
        box-shadow: 25px 20px 20px rgba(0,0,0,0.2);
    }
    @keyframes pop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .user-message {
        background-color: #4f8bf9;
        color: white;
        margin-right: auto;
        margin-left: 10px;
        text-align: left;
    }
    .user-message::after {
        content: "";
        position: absolute;
        bottom: 12px;
        right: -8px;
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
        border-left: 10px solid #4f8bf9;
    }
    .bot-message {
        background-color: #555b6e;
        color: white;
        margin-left: auto;
        margin-right: 10px;
        text-align: left;
    }
    .bot-message::after {
        content: "";
        position: absolute;
        bottom: 12px;
        left: -8px;
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
        border-right: 10px solid #555b6e;
    }
    </style>
    """, unsafe_allow_html=True)

    page = st.sidebar.selectbox("📂 Tableau de bord : ", ["Chatbot", "Tableau de bord"])

    if page == "Tableau de bord":
        afficher_dashboard()
        return

    elif page == "Chatbot":
        st.title("🤖 Chatbot IAvenir")
        st.write("Posez une question ou lancez un quizz d’orientation.")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "show_quizz" not in st.session_state:
            st.session_state.show_quizz = False

        if "quizz_step" not in st.session_state:
            st.session_state.quizz_step = 0

        if "quizz_answers" not in st.session_state:
            st.session_state.quizz_answers = {}

        if "welcome_shown" not in st.session_state:
            st.session_state.welcome_shown = True
            st.session_state.chat_history.append(("Chatbot", "Bonjour 👋 ! Je suis ton assistant d’orientation."))

        if st.button("🎓 Faire le quizz d'orientation"):
            st.session_state.show_quizz = True
            st.session_state.quizz_step = 0
            st.session_state.quizz_answers = {}

        questions = [
            ("interet", "Qu’est-ce qui t’intéresse le plus ?", ["Sciences", "Art", "Informatique", "Commerce", "Nature"]),
            ("competence", "Dans quoi es-tu le plus à l’aise ?", ["Communiquer", "Résoudre des problèmes", "Créer", "Organiser"]),
            ("travail", "Tu préfères travailler...", ["En équipe", "Seul", "En extérieur", "Avec les mains"]),
            ("etudes", "Jusqu’où veux-tu poursuivre tes études ?", ["Bac", "Bac+2", "Bac+5", "Doctorat"]),
            ("objectif", "Ton objectif principal ?", ["Gagner de l’argent", "Aider les autres", "Innover", "Être indépendant"])
        ]

        if st.session_state.show_quizz and st.session_state.quizz_step < len(questions):
            key, q_text, options = questions[st.session_state.quizz_step]
            st.subheader(f"🧠 Question {st.session_state.quizz_step + 1} sur {len(questions)}")
            choice = st.radio(q_text, options, key=key)
            if st.button("Suivant"):
                st.session_state.quizz_answers[key] = choice
                st.session_state.quizz_step += 1
                st.rerun()

        elif st.session_state.show_quizz and st.session_state.quizz_step >= len(questions):
            st.success("✅ Quizz terminé ! Voici tes réponses :")
            st.json(st.session_state.quizz_answers)

        if not st.session_state.show_quizz:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for sender, message in st.session_state.chat_history:
                message_class = "user-message" if sender == "Vous" else "bot-message"
                st.markdown(f'<div class="chat-message {message_class}"><b>{sender} :</b><br>{message}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        bot_thinking_placeholder = st.empty()
        bot_response_placeholder = st.empty()

        with st.form(key="chat_form"):
            user_input = st.text_input("Posez votre question :", "")
            submitted = st.form_submit_button("Envoyer")

        if submitted and user_input:
            st.session_state.chat_history.append(("Vous", user_input))
            st.session_state.pending_response = True
            st.session_state.pending_user_input = user_input

        if st.session_state.get("pending_response", False):
            bot_thinking_placeholder.markdown(
                "<div style='text-align: right;'>Le bot réfléchit... 🤔</div>",
                unsafe_allow_html=True
            )
            time.sleep(1.2)

            response = generate_llm_response(st.session_state.pending_user_input, model_fn)
            st.session_state.pending_bot_response = response
            st.session_state.pending_response = False
            bot_thinking_placeholder.empty()
            st.rerun()

        if "pending_bot_response" in st.session_state:
            displayed_response = ""
            for word in st.session_state.pending_bot_response.split():
                displayed_response += word + " "
                bot_response_placeholder.markdown(
                    f"<div style='background-color:#555b6e; color:white; padding:10px; border-radius:10px; text-align:left; max-width:70%; margin-left:auto; margin-right:10px;'><b>Chatbot :</b><br>{displayed_response}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.05)

            st.session_state.chat_history.append(("Chatbot", st.session_state.pending_bot_response))
            del st.session_state.pending_bot_response
            st.rerun()