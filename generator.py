from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )
    
    system_message = '''*Instructions:* Given the user query and chunks that are most relevant to the user query, please
    give a response to the user query. Answer using only the rule text chunks `chunks` provided. For each chunk you are provided the game and distance.
    Distance is vector distance - the closer to 0 the more relevance. If the answer is not contained
    in the provided text, do not answer anything or attempt to answer the question using outside knowledge, respond with "I couldn't
    find that in the loaded rule books.".'''

    def convert_chunks(chunks):
        ret = ""
        i = 1
        for c in chunks:
            c_string = f"Chunk {i} (Game: {c["game"]}; Distance: {c["distance"]}) : {c["text"]}\n"
            ret += c_string
            i += 1
        return ret

    def create_user_mssg(chunks, query):
        return f"""

        *chunks:*
        {convert_chunks(chunks)}

        *user_query:* {query}

        """
    
    response = _client.chat.completions.create(
        model = LLM_MODEL,
        messages=[
            {'role' : 'system', 'content' : system_message},
            {'role' : 'user', 'content' : create_user_mssg(retrieved_chunks, query)},
        ]

    )
    # Your implementation here.
    return response.choices[0].message.content
