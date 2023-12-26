from os import listdir
from json import dumps, load, loads
import textwrap
import google.generativeai as genai
from IPython.display import Markdown


genai.configure(api_key='AIzaSyBW8_tDl2flqdvqcxbhLDHfGNroGLetnQQ')

model = genai.GenerativeModel("gemini-pro")

chat = None

def main():
  global chat

  prompts, niches = get_data()

  niches = expand_niches(niches)

  for niche in niches:
    chat = model.start_chat(history=[])
    products = [x for x in niches[niche]['products']]
    generate(prompts['general'], ['${products}'], [str(products)])


def check_results(function):

  def wrapper(*args, **kwargs):
    while True:
      returned = function(*args, **kwargs)
      print(dumps(list(returned), indent=4))
      match input("Are you happy with the results? y\\n\n").lower():
        case 'y':
          return returned
        case _:
          continue
  
  return wrapper

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def expand_niches(niches : dict):
  return niches


def get_data():
  with open("posts_template.json") as file:
    prompts = dict(load(file)['prompts'])
  
  with open("products.json") as file:
    niches = dict(load(file))
    for key in niches:
      try:
        if niches[key]['phase'] != 'register':
          del niches[key]
      except KeyError:
        niches[key].update({'phase' : 'register'})
  
  return prompts, niches

@check_results
def generate(prompts : dict, unwanted : list = [], replacements : list = []):
  
  for key in prompts:
    prompt = prompts[key]['prompt']
    extracted_data = prompts[key]['extracted_data']

    for i in range(len(unwanted)):
      prompt = prompt.replace(unwanted[i], replacements[i])

    with open("file.json", 'a') as file:
      yield (str(exec_prompt(prompt, extracted_data)))


def exec_prompt(prompt, extracted_data):
  response = chat.send_message(f"Respond to the following prompt as valid json format that can be loaded with json.load without the word json with the keys: {extracted_data}\n\nThe prompt: {prompt}")
  return to_markdown(response.text).data.replace('>', '')


if __name__ == "__main__":
   main()