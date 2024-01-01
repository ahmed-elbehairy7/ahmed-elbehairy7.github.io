from pam import err, check_results, save_prog
from json import dumps, loads
from IPython.display import Markdown
from textwrap import indent


@err()
@check_results(show_func=lambda x: dumps(x, indent=4))
@save_prog(return_func=lambda x: dumps(x, indent=4))
def generate(prompts: dict, chat, unwanted: list = [], replacements: list = []):
    values = {}
    for key in prompts:
        prompt = prompts[key]["prompt"]
        extracted_data = prompts[key]["extracted_data"]

        for i in range(len(unwanted)):
            prompt = prompt.replace(unwanted[i], replacements[i])

        values.update(dict(exec_prompt(chat, prompt, extracted_data)))

    return values


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(indent(text, "", predicate=lambda _: True))


def exec_prompt(chat, prompt, extracted_data):
    response = chat.send_message(
        f"Respond to the following prompt as valid json format that can be loaded with json.load without the word json with the keys: {extracted_data}\n\nThe prompt: {prompt}"
    )
    return loads(r"""{}""".format(to_markdown(response.text).data))
