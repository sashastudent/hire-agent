from app.config import client
from app.modules.embedding.embedding_module import build_vector_db, EMBEDDING_MODEL


# built ONCE per app run (when this module is first imported)
collection = build_vector_db()

# all the positions we have a PDF for, e.g. ["Python Dev", ...]
POSITIONS = sorted({m["position"] for m in collection.get(include=["metadatas"])["metadatas"]})


def find_position(position):
    """Match the position name case-insensitively ('python dev' -> 'Python Dev')"""
    for p in POSITIONS:
        if p.lower() == position.strip().lower():
            return p
    return None


def search_job_info(position, question, n_results=3):
    """Semantic search - only inside the chunks of the requested position's PDF"""
    query_embedding = client.embeddings.create(
        input=[question], model=EMBEDDING_MODEL
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"position": position},       # filter by metadata = search only this PDF
    )
    return results["documents"][0]


def get_info_from_pdf(position, question):
    matched = find_position(position)
    if matched is None:
        return f"No job description found for '{position}'. Available positions: {', '.join(POSITIONS)}."

    context = "\n\n---\n\n".join(search_job_info(matched, question))

    response = client.responses.create(
        model="gpt-4.1",
        instructions=(
            f"You are a recruiting assistant for a {matched} position, chatting by SMS. "
            "Answer the candidate's question based only on the context. "
            "If the answer is not in the context, say you don't have that information "
            "and that the recruiter can cover it in the interview. Keep it short."
        ),
        input=f"Context:\n{context}\n\nQuestion: {question}",
    )
    return response.output_text
