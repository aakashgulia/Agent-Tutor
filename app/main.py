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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input(
        "Ask a question about the course..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        response, sources = generate_rag_response(question)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
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
        "Latest corporate-startup collaboration news "
        "relevant to Panasonic India."
    )

    if st.button("Find Latest News"):

        from news import fetch_news
        from llm import generate_response

        try:

            articles = fetch_news()

            if not articles:

                st.warning(
                    "No relevant news articles found."
                )

            else:

                news_file = Path("data/news.json")

                try:
                    saved_news = json.loads(
                        news_file.read_text(
                            encoding="utf-8"
                        )
                    )

                except (FileNotFoundError, json.JSONDecodeError):

                    saved_news = []

                updated_news = []

                for article in articles:

                    interpretation_prompt = f"""
You are Agent Tutor for the course
Designing Corporate-Startup Synergies (ENT 3805).

News headline:

{article["title"]}

Source:

{article["source"]}

Explain the relevance of this headline to the course.

STRICT GROUNDING RULES:

- Start with exactly: "AI Interpretation:"
- Use ONLY information explicitly stated in the headline.
- Do not explain the company's motivation or purpose unless
  the headline states it.
- Do not predict or suggest outcomes, benefits, results,
  growth, innovation impact, or future opportunities.
- Do not identify a company, startup, programme, technology,
  investment, partnership, or relationship beyond what the
  headline explicitly states.
- Do not add facts from your general knowledge.
- Do not pretend to have read the full article.
- You may connect explicitly stated terms such as "startup",
  "co-creation", "collaboration", or "programme" to general
  course concepts such as corporate-startup collaboration
  and co-creation.
- If an important detail is not available from the headline,
  say:
  "The headline does not provide enough information to determine this."
- Keep the answer to exactly 2-3 sentences.
- Keep it student-friendly.

Focus on WHAT THE HEADLINE SAYS, not WHY IT MAY BE HAPPENING.
"""

                    interpretation = generate_response(
                        interpretation_prompt
                    )

                    saved_article = article.copy()
                    saved_article["ai_interpretation"] = interpretation

                    updated_news.append(saved_article)

                # Preserve older saved articles
                for old_article in saved_news:

                    if old_article["link"] not in [
                        article["link"]
                        for article in updated_news
                    ]:

                        updated_news.append(old_article)

                news_file.write_text(
                    json.dumps(
                        updated_news,
                        indent=2,
                        ensure_ascii=False
                    ),
                    encoding="utf-8"
                )

                st.success(
                    f"Found {len(articles)} relevant recent articles."
                )

                for article in updated_news[:len(articles)]:

                    st.subheader(article["title"])

                    st.write(
                        f"**Source:** {article['source']}"
                    )

                    st.write(
                        f"**Published:** {article['published']}"
                    )

                    st.markdown(
                        f"[Open original article]({article['link']})"
                    )

                    st.markdown(
                        "### Course Relevance (AI Interpretation)"
                    )

                    st.write(
                        article["ai_interpretation"]
                    )

                    st.caption(
                        "This is an AI interpretation based on the "
                        "headline only. Open the original article for "
                        "verified article details."
                    )

                    st.divider()

        except Exception as e:

            st.error(
                f"Unable to fetch news: {e}"
            )


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

        st.info(
            "No prompt history has been recorded yet."
        )

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

            student_note = st.text_area(
                "Student-added note",
                value=log.get("student_note", ""),
                key=f"student_note_{index}",
                height=100
            )

            if st.button(
                "Save Note",
                key=f"save_note_{index}"
            ):

                prompt_logs[index - 1]["student_note"] = student_note

                prompt_log_file.write_text(
                    json.dumps(
                        prompt_logs,
                        indent=2,
                        ensure_ascii=False
                    ),
                    encoding="utf-8"
                )

                st.success(
                    "Student note saved."
                )

            st.divider()