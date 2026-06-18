import ollama

def query(prompt):
    response = ollama.chat(model='qwen2.5:7b', messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def should_retrieve(question, history):
    prompt= f"""Given this conversation so far and the new question, 
    do you need to look up additional rules information to answer accurately?
    Answer only YES or NO. 
    
    Context: {history}
    
    THE QUESTION BEING ASKED:
    {question}
    Reminder, Do you have enough information? answer YES or NO"""
    response = ollama.chat(model='qwen2.5:7b', messages=[{"role": "user", "content": prompt}])
    print(response["message"]["content"])
    return "YES" in response.upper()

    