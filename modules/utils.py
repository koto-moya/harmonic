from config import chat_interface_html_head


def create_message(direction, message):
    return f'''<div class="{direction}">{message}</div>'''

def create_chat(formatted_chat_history):
    return chat_interface_html_head + "<body>" + formatted_chat_history + "</body>"