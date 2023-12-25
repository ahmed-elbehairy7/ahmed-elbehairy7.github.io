from os import listdir
from json import dumps, load
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown


def main():

  with open("posts_template.json") as file:
      prompts = dict(load(file)['prompts'])




  genai.configure(api_key='AIzaSyBW8_tDl2flqdvqcxbhLDHfGNroGLetnQQ')

  model = genai.GenerativeModel("gemini-pro")

  response = model.generate_content("What is the meaning of life?")

  print(to_markdown(response.text))


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



if __name__ == "__main__":
   main()