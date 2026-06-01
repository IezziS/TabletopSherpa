import ollama
from pathlib import Path
from backend.util.chroma_utils import query_router

ROOT = Path(__file__).parent.parent



def ask_rules_lawyer(question):
    if (question.find('Tau') != -1): #probably a stupid check, but most people will write Tau, while offical spelling is T'au
        question = question.replace('Tau', 'T’au')
        
    documents, metadatas = query_router(question, edition = "10th", n_results = 5)

    context = "\n---\n".join(documents)
    
    prompt = f"""You are a Warhammer 40k gameplay assistant and rules teacher. 
    Your job is to:
    - explain rules clearly and accurately
    - summarize rules in your own words
    - help teach gameplay flow and timing
    - stay grounded ONLY in the provided rules context
    State whether each answer is:
    - directly supported by rules context: use language like: 'The rules state that...', 'According to the rules...', 'The text says...'
    - inferred from gameplay procedure 
    - uncertain/ambiguous
    IMPORTANT RULES:
    - Do NOT invent rules not supported by the context
    - If the context is incomplete or ambiguous, say so clearly
    - Prefer cautious wording over overconfident wording
    - Avoid verbatim quoting unless necessary for rule keywords or names
    - Explain WHY a rule works when possible
    - For gameplay procedures, explain the sequence step-by-step
    - If multiple interpretations may exist, acknowledge that
    - If the answer cannot be determined from the context, explicitly say so

    Additional notes:
    - "nan" means no value / universal
    - Detachment/type metadata may not always be relevant
    - Do not mention missing metadata unless important
    
    Rules Text:
    {context}

    Question:

    {question}
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    return response["message"]["content"]



question = "What is the CP cost for a command re-roll? What can i use it on?"
print(question)
print(ask_rules_lawyer(question))
question = "What does oath of moment do?"
print(question)
print(ask_rules_lawyer(question))

question = "When rolling saving throws, on a unit where models have different armor saves , do you roll all the saves at once or one at a time? Is there a fast rolling method for this?"
print(question)
print(ask_rules_lawyer(question))

question = "I'm in the shooting phase, what stratagems can I use of my space marine infantry unit?"
print(question)
print(ask_rules_lawyer(question))
