import streamlit as st
from rag import generate_rag_response


# Page configuration
st.set_page_config(
    page_title="Agent Tutor",
    page_icon="🎓",
    layout="wide"
)

# Application title
st.title("🎓 Agent Tutor")
st.caption("Designing Corporate-Startup Synergies — ENT 3805")

st.divider()

# Sidebar navigation
section = st.sidebar.radio(
    "Navigate",
    [
        "💬 Chat",
        "📝 Class Reflection",
        "📰 Fortnightly News",
        "📋 Prompt Log"
    ]
)

# --------------------------------------------------
# CHAT
# --------------------------------------------------

if section == "💬 Chat":

    st.header("Course Chat")

    st.write(
        "Ask questions about corporate-startup collaboration, "
        "course concepts, readings, and our group knowledge."
    )

    # Create chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    question = st.chat_input(
        "Ask a question about the course..."
    )

    if question:

        # Add student question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        # Temporary response
        response, sources = generate_rag_response(question) 

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message("assistant"):
            st.write(response)


# --------------------------------------------------
# CLASS REFLECTION
# --------------------------------------------------

elif section == "📝 Class Reflection":

    st.header("Class Reflection")

    st.write(
        "Use this section after each class session."
    )

    st.text_area(
        "Key points from today's class",
        height=150
    )

    st.text_area(
        "One open / unanswered question",
        height=100
    )

    st.button("Generate Reflection")


# --------------------------------------------------
# FORTNIGHTLY NEWS
# --------------------------------------------------

elif section == "📰 Fortnightly News":

    st.header("Fortnightly Corporate-Startup News")

    st.write(
        "This section will collect and summarize relevant "
        "corporate-startup collaboration news."
    )

    st.button("Find Latest News")


# --------------------------------------------------
# PROMPT LOG
# --------------------------------------------------

elif section == "📋 Prompt Log":

    st.header("Prompt & Activity Log")

    st.write(
        "The final system will maintain a visible record of:"
    )

    st.markdown("""
    - Student prompts
    - AI responses
    - Student-added notes
    """)
