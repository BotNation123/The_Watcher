import random

from database import test, get_links, get_all_links, delete_link, delete_all_link


def handle_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hello, how are you?"
    if p_message == "roll":
        return str(random.randint(1, 6))
    if p_message == "!help":
        return "`this is a default message.`"


def handle_numbers(num1: int, num2: int) -> int:
    return num1 + num2


def handle_roll() -> str:
    return str(random.randint(1, 6))


def handle_submit(arg, author) -> str:
    test(arg, author)
    return str("se ha insertado correctamente" + arg)


def handle_getLinks():
    return get_links()


def handle_getAllLinks():
    return get_all_links()

def handle_deleteLink(arg:str):
    delete_link(arg)
    return "se ha eliminado correctamente"