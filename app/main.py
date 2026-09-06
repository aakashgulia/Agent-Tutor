import streamlit as st

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

# Navigation
section = st.sidebar.radio(
    "Navigate",
    [
        "💬 Chat",
        "📝 Class Reflection",
        "📰 Fortnightly News",
        "📋 Prompt Log"
    ]
)

# Chat section
if section == "💬 Chat":
    st.header("Course Chat")
    st.write(
        "Ask questions about corporate-startup collaboration, "
        "course concepts, readings, and our group knowledge."
    )

    question = st.text_input("Ask a question")

    if question:
        st.info(
            "AI answering will be connected in a later step."
        )

# Reflection section
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

# News section
elif section == "📰 Fortnightly News":
    st.header("Fortnightly Corporate-Startup News")

    st.write(
        "This section will collect and summarize relevant "
        "corporate-startup collaboration news."
    )

    st.button("Find Latest News")

# Prompt Log section
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