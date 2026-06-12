from backend.prompt import PROMPT_TEMPLATES


def get_system_prompt(game, edition):
    key = f"{game.upper().strip()}_{edition.upper().strip()}_PROMPT"
    template = PROMPT_TEMPLATES.get(key)
    
    if template is None:
        raise ValueError(f"no prompt template for {game} - {edition}")
    return template

def form_new_prompt(question, context, game, edition):
    base_prompt = get_system_prompt(game, edition)
    
    prompt = f"""{base_prompt}
    RULES CONTEXT : {context}
    
    Question: {question}
    """
    return prompt

def form_prompt(question, context):
    prompt = f"""{context}
    Question: {question}"""

    return prompt
    
    
    
