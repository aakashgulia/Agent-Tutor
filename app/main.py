import sys
from pathlib import Path
import json
from datetime import datetime

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

        prompt_log_file.parent.mkdir(
            parents=True,
            exist_ok=True
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

    reflection_file = Path("data/reflections.json")

    # Load previously saved reflections
    try:

        reflections = json.loads(
            reflection_file.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(reflections, list):
            reflections = []

    except (FileNotFoundError, json.JSONDecodeError):

        reflections = []

    # --------------------------------------------------
    # CREATE NEW REFLECTION
    # --------------------------------------------------

    st.subheader("Create a New Reflection")

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

            try:

                from rag import generate_reflection

                with st.spinner("Generating your class reflection..."):

                    reflection, sources = generate_reflection(
                        key_points,
                        open_question
                    )

                # Prepare the saved reflection
                saved_record = {
                    "key_points": key_points,
                    "open_question": open_question,
                    "reflection": reflection,
                    "saved_at": datetime.now().strftime(
                        "%d %b %Y, %I:%M %p"
                    ),
                    "sources": [
                        {
                            "source": source.get(
                                "source",
                                "Unknown"
                            ),
                            "score": source.get("score")
                        }
                        for source in sources
                    ]
                }

                # Add new reflection to existing records
                reflections.append(saved_record)

                # Ensure data directory exists
                reflection_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                # Save reflections
                reflection_file.write_text(
                    json.dumps(
                        reflections,
                        indent=2,
                        ensure_ascii=False
                    ),
                    encoding="utf-8"
                )

                st.success(
                    "Reflection generated and saved successfully!"
                )

                st.subheader("Generated Reflection")

                st.write(reflection)

                st.markdown("### Sources")

                for source in sources:

                    st.write(
                        f"📄 {source['source']} "
                        f"(similarity: {source['score']:.3f})"
                    )

            except Exception as e:

                st.error(
                    f"Unable to generate reflection: {e}"
                )

    # --------------------------------------------------
    # SAVED REFLECTIONS
    # --------------------------------------------------

    st.divider()

    st.subheader("Saved Class Reflections")

    # Summary metrics
    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Saved Reflections",
            len(reflections)
        )

    with col2:

        latest_session = (
            reflections[-1].get(
                "saved_at",
                "Previously saved"
            )
            if reflections
            else "No sessions yet"
        )

        st.metric(
            "Latest Session",
            latest_session
        )

    # Display saved reflections
    if not reflections:

        st.info(
            "No saved reflections yet. "
            "Generate your first reflection above."
        )

    else:

        search_query = st.text_input(
            "Search your reflections",
            placeholder="Search by topic, question or class notes..."
        )

        matching_reflections = []

        # Newest reflections appear first
        for index, item in reversed(
            list(enumerate(reflections, start=1))
        ):

            searchable_text = (
                str(item.get("key_points", "")) + " " +
                str(item.get("open_question", "")) + " " +
                str(item.get("reflection", ""))
            ).lower()

            if search_query.lower() in searchable_text:

                matching_reflections.append(
                    (index, item)
                )

        st.caption(
            f"Showing {len(matching_reflections)} "
            f"of {len(reflections)} saved reflections"
        )

        if not matching_reflections:

            st.info(
                "No reflections match your search."
            )

        for index, item in matching_reflections:

            saved_date = item.get(
                "saved_at",
                "Previously saved"
            )

            with st.expander(
                f"Reflection #{index} | {saved_date}"
            ):

                st.markdown("**Key Points from Class**")

                st.write(
                    item.get(
                        "key_points",
                        "Not available"
                    )
                )

                st.markdown(
                    "**Open / Unanswered Question**"
                )

                st.write(
                    item.get(
                        "open_question",
                        "Not available"
                    )
                )

                st.divider()

                st.markdown("**Generated Reflection**")

                st.markdown(
                    item.get(
                        "reflection",
                        "Not available"
                    )
                )

                saved_sources = item.get(
                    "sources",
                    []
                )

                if saved_sources:

                    st.markdown("**Course Sources**")

                    for source in saved_sources:

                        source_name = source.get(
                            "source",
                            "Unknown"
                        )

                        score = source.get("score")

                        if score is not None:

                            st.write(
                                f"📄 {source_name} "
                                f"(similarity: {score:.3f})"
                            )

                        else:

                            st.write(
                                f"📄 {source_name}"
                            )


# --------------------------------------------------
# FORTNIGHTLY NEWS
# --------------------------------------------------

elif section == "Fortnightly News":

    st.header("Fortnightly Startup & Corporate News")

    st.write(
        "Explore recent Indian startup and corporate developments, "
        "including funding, acquisitions, collaborations, technology, "
        "business expansion, IPOs, policy updates, and Panasonic-related news."
    )

    st.caption(
        "News is collected from the previous 14 days."
    )

    if st.button("Find Latest News"):

        from news import fetch_news
        from llm import generate_response

        try:

            articles = fetch_news()

            if not articles:

                st.warning(
                    "No relevant news articles found in the last 14 days. "
                    "Please try again later."
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

Category:
{article.get("category", "General Business News")}

Explain the relevance of this headline to the course.

STRICT GROUNDING RULES:

- Start with exactly: "AI Interpretation:"
- Use ONLY information explicitly stated in the headline.
- Do not explain a company's motivation or purpose unless
  the headline states it.
- Do not predict or suggest outcomes, benefits, results,
  growth, innovation impact, or future opportunities.
- Do not identify a company, startup, programme, technology,
  investment, partnership, or relationship beyond what the
  headline explicitly states.
- Do not add facts from your general knowledge.
- Do not pretend to have read the full article.
- You may connect explicitly stated terms to general course
  concepts such as corporate-startup collaboration,
  entrepreneurship, innovation, and business strategy.
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
                new_links = {
                    article["link"]
                    for article in updated_news
                }

                for old_article in saved_news:

                    if old_article.get("link") not in new_links:
                        updated_news.append(old_article)

                news_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                news_file.write_text(
                    json.dumps(
                        updated_news,
                        indent=2,
                        ensure_ascii=False
                    ),
                    encoding="utf-8"
                )

                st.success(
                    f"Found {len(articles)} recent news articles."
                )

                for article in updated_news[:len(articles)]:

                    st.markdown(
                        f"### {article['title']}"
                    )

                    st.markdown(
                        f"**Category:** {article.get('category', 'General Business News')}"
                    )

                    st.write(
                        f"**Source:** {article.get('source', 'Not available')}"
                    )

                    st.write(
                        f"**Published:** {article.get('published', 'Not available')}"
                    )

                    st.markdown(
                        f"[Open original article]({article['link']})"
                    )

                    st.markdown(
                        "#### Course Relevance (AI Interpretation)"
                    )

                    st.write(
                        article.get(
                            "ai_interpretation",
                            "AI interpretation is not available."
                        )
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