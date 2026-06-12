from backend.services.chat_services import get_answer


def handle_ask(body):
    answer = get_answer(body.question, body.game, body.edition, body.history)
    return {"answer": str(answer), "retrieved": True}