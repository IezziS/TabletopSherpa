import ollama
from pathlib import Path
from backend.util.chroma_utils import query_router

ROOT = Path(__file__).parent.parent



def ask_rules_lawyer(question, edition):
    if (question.find('Tau') != -1): #probably a stupid check, but most people will write Tau, while offical spelling is T'au
        question = question.replace('Tau', 'T’au')
        
    documents, metadatas = query_router(question, edition, n_results = 5)

    context = "\n---\n".join(documents)
    
    prompt = f"""You are a Warhammer 40k gameplay assistant and rules teacher. 
    Your job is to:
    - explain rules clearly and accurately
    - Be concise and direct.
    - help teach gameplay flow and timing
    - stay grounded ONLY in the provided rules context
    - Examples can only be used if they are directly supported by the rules context, do not extrapolate.
    State whether each answer is:
    - directly supported by rules context: use language like: 'The rules state that...', 'According to the rules...', 'The text says...'
    - inferred from gameplay procedure 
    - uncertain/ambiguous
    IMPORTANT RULES:
    - Do NOT invent rules not supported by the context
    - When analyzing unit interactions, use the stats listed in their datasheets
    - If the context is incomplete or ambiguous, say so clearly
    - Prefer cautious wording over overconfident wording
    - Avoid verbatim quoting unless necessary for rule keywords or names
    - For gameplay procedures, explain the sequence step-by-step
    - If multiple interpretations may exist, acknowledge that
    - If the answer cannot be determined from the context, explicitly say so

    Additional notes:
    - "nan" means no value / universal
    - Detachment/type metadata may not always be relevant, example, many pieces of data say "Boarding Action" in them, this is a different game format, not always necessary to aknowledge it.
    - Do not mention missing metadata unless important
    
    Rules Text:
    {context}

    Question:

    {question}
    """

    response = ollama.chat(model='qwen2.5:7b', messages=[{"role": "user", "content": prompt}])
    
    return response["message"]["content"]


if __name__ == '__main__':
    question = "What does oath of moment do?"
    print(question)
    print(ask_rules_lawyer(question , "10th"))

    question = "When rolling saving throws, on a unit where models have different armor saves , do you roll all the saves at once or one at a time? Is there a fast rolling method for this?"
    print(question)
    print(ask_rules_lawyer(question , "10th"))

    question = "My 5-man intercessor squad is going to shoot at a unit of ork boyz with their bolt rifle, how many wounds should I expect to deal?"
    print(question)
    print(ask_rules_lawyer(question, "10th"))
