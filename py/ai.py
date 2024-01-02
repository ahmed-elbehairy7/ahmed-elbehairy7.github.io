from pam import err, check_results, save_prog, manual_edit
from json import dumps, loads
from IPython.display import Markdown
from textwrap import indent
from google.generativeai import ChatSession

ChatSession.send_message = save_prog(return_func=lambda x : to_markdown(x.text).data)(ChatSession.send_message)


def generate(prompts: dict, chat : ChatSession, unwanted: list = [], replacements: list = []):
    values = {}
    for key in prompts:
        prompt = prompts[key]["prompt"]
        extracted_data = prompts[key]["extracted_data"]
        formats = prompts[key]["formats"]

        for i in range(len(unwanted)):
            prompt = prompt.replace(unwanted[i], replacements[i])

        format = {}
        for i in range(len(extracted_data)):
            format = dict(list(format.items()) + list({extracted_data[i] : formats[i]}.items()))

        values.update(dict(exec_prompt(chat, prompt, format)))

    return values

def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(indent(text, "", predicate=lambda _: True))

@manual_edit(write_func= lambda x : dumps(x, indent=4))
@err()
@check_results(show_func=lambda x: dumps(x, indent=4))
@save_prog(return_func=lambda x: dumps(x, indent=4))
def exec_prompt(chat, prompt, format):
    response = chat.send_message(
        f"""Respond to the following prompt as valid json format that can be loaded with json.load without the word json. you should include strings in double qoutes '"'. The returned object should be like:\n{format}\n\nThe prompt: {prompt}"""
    )
    return loads(r"""{}""".format(response.text.replace("`", "").replace("'", '"')))
