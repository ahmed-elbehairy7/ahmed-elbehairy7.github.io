from os import listdir
from json import dumps, load, loads
import textwrap
import google.generativeai as genai
from IPython.display import Markdown
from pam import check_results, find, err
from itertools import product
from setup import posts

__version__ = "00.00.01"


genai.configure(api_key="AIzaSyBW8_tDl2flqdvqcxbhLDHfGNroGLetnQQ")

model = genai.GenerativeModel("gemini-pro")


def main():
    print(posts)

    prompts, niches = get_data()

    niches = expand_niches(niches)

    for niche in niches:
        chat = model.start_chat(history=[])
        products = [x for x in niches[niche]["products"]]
        generate(prompts["general"], chat, ["${products}"], [str(products)])

        for product in products:
            generate(prompts["product"], chat, ["${product}"], [product])


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "", predicate=lambda _: True))


def expand_niches(niches: dict):
    new_niches = {}
    for niche in niches:
        products_data = niches[niche]["products"]

        products = all_combinations(products_data)

        for combination in products:
            new_products = {}
            for product in combination:
                new_products[product] = products_data[product]

            new_niches.update(
                {
                    f"{' & '.join(combination)}": {
                        "phase": "register",
                        "products": new_products,
                    }
                }
            )
    return new_niches


def all_combinations(values):
    combinations = []
    for i in range(1, len(values) + 1):
        combinations += list(product(values, repeat=i))

    clean = []
    for i in range(len(combinations)):
        combinations[i] = sorted(set(combinations[i]))
        if not combinations[i] in clean and len(combinations[i]) > 1:
            clean.append(combinations[i])

    return clean


def get_data():
    with open(find("prompts.json")) as file:
        prompts = dict(load(file))

    with open(find("products.json")) as file:
        niches = dict(load(file))
        for key in niches:
            try:
                if niches[key]["phase"] != "register":
                    del niches[key]
            except KeyError:
                niches[key].update({"phase": "register"})

    return prompts, niches

@err
@check_results
def generate(prompts: dict, chat, unwanted: list = [], replacements: list = []):
    for key in prompts:
        prompt = prompts[key]["prompt"]
        extracted_data = prompts[key]["extracted_data"]

        for i in range(len(unwanted)):
            prompt = prompt.replace(unwanted[i], replacements[i])

        yield exec_prompt(chat, prompt, extracted_data)


def exec_prompt(chat, prompt, extracted_data):
    response = chat.send_message(
        f"Respond to the following prompt as valid json format that can be loaded with json.load without the word json with the keys: {extracted_data}\n\nThe prompt: {prompt}"
    )
    return loads(to_markdown(response.text).data)


if __name__ == "__main__":
    main()
