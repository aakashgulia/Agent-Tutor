import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from rag import generate_rag_response


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Agent Tutor",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# Application title
# --------------------------------------------------

st.title("🎓 Agent Tutor")
st.caption("Designing Corporate-Startup Synergies — ENT 3805")

st.divider()


# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------

section = st.sidebar.radio(
    "Navigate",
    [
        "Chat",
        "Class Reflection",
        "Fortnightly News",
        "Prompt Log"
    ]
)


# --------------------------------------------------
# CHAT
# --------------------------------------------------

if section == "Chat":

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

        # Generate RAG response
        response, sources = generate_rag_response(question)

        # Save assistant response to chat history
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # Save prompt and response to prompt log
        prompt_log_file = Path("data/prompt_log.json")

        try:
            prompt_logs = json.loads(
                prompt_log_file.read_text(
                    encoding="utf-8"
                )
            )

        except (FileNotFoundError, json.JSONDecodeError):

            prompt_logs = []

        prompt_logs.append(
            {
                "prompt": question,
                "response": response,
                "student_note": ""
            }
        )

        prompt_log_file.write_text(
            json.dumps(
                prompt_logs,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        with st.chat_message("assistant"):

            st.write(response)

            st.markdown("### Sources")

            for source in sources:

                st.write(
                    f"📄 {source['source']} "
                    f"(similarity: {source['score']:.3f})"
                )


# --------------------------------------------------
# CLASS REFLECTION
# --------------------------------------------------

elif section == "Class Reflection":

    st.header("Class Reflection")

    st.write(
        "Use this section after each class session."
    )

    key_points = st.text_area(
        "Key points from today's class",
        height=150
    )

    open_question = st.text_area(
        "One open / unanswered question",
        height=100
    )

    if st.button("Generate Reflection"):

        if not key_points.strip() or not open_question.strip():

            st.warning(
                "Please enter both the key points and the open question."
            )

        else:

            from rag import generate_reflection

            reflection, sources = generate_reflection(
                key_points,
                open_question
            )

            st.subheader("Generated Reflection")

            st.write(reflection)

            # Save reflection
            reflection_file = Path("data/reflections.json")

            try:
                reflections = json.loads(
                    reflection_file.read_text(
                        encoding="utf-8"
                    )
                )

            except (FileNotFoundError, json.JSONDecodeError):

                reflections = []

            reflections.append(
                {
                    "key_points": key_points,
                    "open_question": open_question,
                    "reflection": reflection
                }
            )

            reflection_file.write_text(
                json.dumps(
                    reflections,
                    indent=2,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

            st.success(
                "Reflection saved successfully."
            )

            st.subheader("Sources")

            for source in sources:

                st.write(
                    f"📄 {source['source']} "
                    f"(similarity: {source['score']:.3f})"
                )


# --------------------------------------------------
# FORTNIGHTLY NEWS
# --------------------------------------------------

elif section == "Fortnightly News":

    st.header("Fortnightly Corporate-Startup News")

    st.write(
        "This section will collect and summarize relevant "
        "corporate-startup collaboration news."
    )

    st.button("Find Latest News")


# --------------------------------------------------
# PROMPT LOG
# --------------------------------------------------

elif section == "Prompt Log":

    st.header("Prompt & Activity Log")

    st.write(
        "The system maintains a visible record of:"
    )

    st.markdown(
        """
        - Student prompts
        - AI responses
        - Student-added notes
        """
    )

    prompt_log_file = Path("data/prompt_log.json")

    try:
        prompt_logs = json.loads(
            prompt_log_file.read_text(
                encoding="utf-8"
            )
        )

    except (FileNotFoundError, json.JSONDecodeError):

        prompt_logs = []

    if not prompt_logs:

        st.info("No prompt history has been recorded yet.")

    else:

        for index, log in enumerate(
            prompt_logs,
            start=1
        ):

            st.markdown(
                f"### Interaction {index}"
            )

            st.write(
                f"**Student Prompt:** {log['prompt']}"
            )

            st.write(
                f"**AI Response:** {log['response']}"
            )

            st.write(
                f"**Student Note:** "
                f"{log.get('student_note', '') or 'No note added yet.'}"
            )

            st.divider()