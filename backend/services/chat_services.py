from backend.services.llm_services import query, should_retrieve
from backend.services.chroma_services import query_router
from backend.services.prompt_services import form_new_prompt , form_prompt

def get_answer(question, game, edition, history):
    formatted_history = [f"{m['role']}: {m['text']}" for m in history[-6:]]
    prompt = ''
    context = []
    if not history or should_retrieve(history, question):
        
        documents, metadatas = query_router(question, edition, n_results = 5)
        context.append(documents)
        if not history: 
            
            prompt = form_new_prompt(question, context, game, edition)
        else:
            prompt = form_prompt(question, formatted_history.apped(context))
    else:
        prompt = form_prompt(question, formatted_history)
    return query(prompt)    