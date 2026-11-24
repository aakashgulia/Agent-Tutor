
import json
import re

from app.retriever import retrieve_chunks
from app.llm import generate_response


def generate_rag_response(question, top_k=3):
    """
    Assess course-material support and generate an answer.

    Modes:
    - SUPPORTED: Answer using course material.
    - PARTIAL: Combine course material with general AI knowledge.
    - NOT_SUPPORTED: Answer using general AI knowledge only.

    Returns:
        response (str): Formatted answer with an explicit mode label.
        sources (list): Only sources actually selected as supporting evidence.
    """

    results = retrieve_chunks(question, top_k=top_k)

    context_parts = []

    for result in results:
        context_parts.append(
            f"Chunk ID: {result['id']}\n"
            f"Source: {result['source']}\n"
            f"Content:\n{result['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    if not context:
        context = "No course material was retrieved."

    prompt = f"""
You are Agent Tutor for the course
Designing Corporate-Startup Synergies (ENT 3805).

Your task is to answer the student's question accurately.

You must first assess whether the supplied course material
actually supports an answer. Keyword similarity alone does
not mean that a source supports the answer.

Choose exactly one status:

1. SUPPORTED
Use this when the course material contains enough relevant
information to answer the question.

2. PARTIAL
Use this when the course material supports some parts of
the answer but additional information is needed.

3. NOT_SUPPORTED
Use this when the course material does not meaningfully
support an answer to the question.

IMPORTANT RULES:

- Do not classify material as relevant merely because it
  contains a few matching keywords.
- Check the actual meaning and context of each chunk.
- Do not invent facts or claim that a source says something
  it does not say.
- General AI knowledge is allowed when course material is
  insufficient.
- Clearly distinguish course-supported information from
  general AI knowledge.
- Never use general AI knowledge as a course citation.
- Only include chunk IDs that genuinely support the answer.
- Use simple, student-friendly language.
- If the question is outside the course, still answer it
  using general AI knowledge.
- Acknowledge uncertainty where appropriate.

OUTPUT FORMAT:

Return ONLY valid JSON. Do not use Markdown code fences.

Use exactly this structure:

{{
    "status": "SUPPORTED",
    "answer": "Your complete answer here.",
    "used_chunk_ids": [0, 1]
}}

For PARTIAL:
- Explain the course-supported information first.
- Clearly identify the additional AI-generated information.
- Include only genuinely supporting course chunk IDs.

For NOT_SUPPORTED:
- Answer using general AI knowledge.
- Explicitly state that the answer is not based on the
  provided course material.
- Set used_chunk_ids to an empty list.

COURSE MATERIAL:

{context}

STUDENT QUESTION:

{question}
"""

    raw_response = generate_response(prompt)

    try:
        # Remove Markdown code fences if the model adds them.
        cleaned_response = raw_response.strip()
        cleaned_response = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned_response,
            flags=re.IGNORECASE
        )
        cleaned_response = re.sub(
            r"\s*```$",
            "",
            cleaned_response
        )

        data = json.loads(cleaned_response)

        status = str(data.get("status", "")).upper()
        answer = str(data.get("answer", "")).strip()
        used_ids = data.get("used_chunk_ids", [])

        if status not in {"SUPPORTED", "PARTIAL", "NOT_SUPPORTED"}:
            raise ValueError("Invalid answer status.")

        if not answer:
            raise ValueError("Empty answer returned.")

        if not isinstance(used_ids, list):
            raise ValueError("Invalid source ID list.")

        # Only allow IDs that actually exist in retrieved results.
        valid_results = {
            str(result["id"]): result
            for result in results
        }

        selected_sources = []

        if status != "NOT_SUPPORTED":
            for chunk_id in used_ids:
                source = valid_results.get(str(chunk_id))

                if source and source not in selected_sources:
                    selected_sources.append(source)

        # Do not display course citations if the model
        # did not identify any valid supporting chunks.
        if status == "SUPPORTED" and not selected_sources:
            status = "PARTIAL"

            answer = (
                "The retrieved course material was not sufficiently "
                "validated as supporting this answer.\n\n"
                "Additional AI-generated explanation:\n"
                + answer
                + "\n\nThis explanation should be treated as "
                "general AI knowledge rather than a verified "
                "course-based answer."
            )

        if status == "SUPPORTED":
            response = (
                "**[COURSE-SUPPORTED ANSWER]**\n\n"
                + answer
            )

        elif status == "PARTIAL":
            response = (
                "**[PARTIALLY COURSE-SUPPORTED + "
                "AI-GENERATED ANSWER]**\n\n"
                + answer
                + "\n\n*Some information above uses general AI "
                "knowledge because the course material does not "
                "fully cover the question.*"
            )

        else:
            response = (
                "**[AI-GENERATED ANSWER - OUTSIDE COURSE MATERIAL]**"
                "\n\n"
                + answer
            )

            selected_sources = []

        return response, selected_sources

    except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
        # Safe fallback: never claim course support when the
        # structured support assessment cannot be validated.
        fallback_response = (
            "**[AI-GENERATED ANSWER - SOURCE VALIDATION UNAVAILABLE]**"
            "\n\n"
            + raw_response
            + "\n\n*The answer could not be reliably classified "
            "against the course material. Please treat it as "
            "general AI-generated information.*"
        )

        return fallback_response, []


def generate_reflection(key_points, open_question, top_k=3):
    """
    Generate a class reflection using student notes and
    relevant course material.
    """

    reflection_query = f"""
Class key points:
{key_points}

Open / unanswered question:
{open_question}
"""

    results = retrieve_chunks(
        reflection_query,
        top_k=top_k
    )

    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are Agent Tutor for the course Designing
Corporate-Startup Synergies (ENT 3805).

Create a concise class reflection using the student's notes
and retrieved course material.

RULES:
- Keep the student's key points as the basis.
- Use course material to connect the reflection to the course.
- Do not invent session numbers, facts, examples or claims.
- Do not invent information about classroom discussions.
- Do not answer the open question unless the course material
  directly supports an answer.
- Clearly distinguish course-supported information
  from interpretation.
- Keep the reflection student-friendly.

STUDENT KEY POINTS:
{key_points}

STUDENT OPEN QUESTION:
{open_question}

RETRIEVED COURSE MATERIAL:
{context}
"""

    reflection = generate_response(prompt)

    return reflection, results
