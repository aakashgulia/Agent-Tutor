from retriever import retrieve_chunks
from llm import generate_response


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
- Prefer the provided course material over general knowledge.
- Do not invent facts.
- If the course material does not contain enough information to answer, clearly say so.
- Give a concise and student-friendly answer.

COURSE MATERIAL:
{context}

STUDENT QUESTION:
{question}
"""

    return generate_response(prompt), results
