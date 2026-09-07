from app.retriever import retrieve_chunks
from app.llm import generate_response


def generate_rag_response(question, top_k=3):
    # Retrieve relevant course material
    results = retrieve_chunks(question, top_k=top_k)

    # Combine retrieved chunks into context
    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # Give the retrieved material to the LLM
    prompt = f"""
You are Agent Tutor for the course Designing Corporate-Startup Synergies (ENT 3805).

Answer the student's question using the course material provided below.


Rules:
- Use the retrieved course material as the primary source.
- Do not invent facts, examples, companies, or claims.
- If the material directly answers the question, explain it clearly.
- If the material does not give a direct definition but provides examples or related characteristics, synthesize those examples into a cautious explanation and clearly indicate that it is an interpretation based on the material.
- If the retrieved material genuinely does not provide enough information, say so.
- Distinguish between what the source explicitly states and what is inferred from it.
- Give a concise and student-friendly answer.

COURSE MATERIAL:
{context}

STUDENT QUESTION:
{question}
"""

    return generate_response(prompt), results

def generate_reflection(key_points, open_question, top_k=3):
    reflection_query = f"""
Class key points:
{key_points}

Open / unanswered question:
{open_question}
"""

    results = retrieve_chunks(reflection_query, top_k=top_k)

    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are Agent Tutor for the course Designing Corporate-Startup Synergies (ENT 3805).

Create a concise class reflection using the student's notes and the retrieved course material.

Rules:
- Keep the student's key points as the basis of the reflection.
- Use the retrieved course material to connect the reflection to the course.
- Do not invent facts or claims.
- Do not answer the student's open question unless the retrieved material directly supports an answer.
- Clearly distinguish course-supported information from interpretation.
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
