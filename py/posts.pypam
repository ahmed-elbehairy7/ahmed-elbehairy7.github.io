from os import chdir, path as os_path
from json import dumps, load, loads
import google.generativeai as genai
from pam import check_results, find, err, save_prog
from setup import posts
from niches import expand_niches
from inout import get_data, put_data
from ai import generate

__version__ = "00.00.01"


genai.configure(api_key="AIzaSyBW8_tDl2flqdvqcxbhLDHfGNroGLetnQQ")

model = genai.GenerativeModel("gemini-pro")

if not os_path.exists(f"{posts.name}.py"):
    chdir(find("py"))


def main():
    print(posts)

    prompts, niches = get_data()

    for niche in niches:
        chat = model.start_chat(history=[])
        products = [x for x in niches[niche]["products"]]
        put_data(
            generate(prompts["general"], chat, ["${products}"], [str(products)]),
            "data.json",
            niche,
            "general"
        )
        
        for product in products:
            put_data(
                {product : generate(prompts["product"], chat, ["${product}"], [product])},
                "data.json",
                niche,
                "site_content"
            )


if __name__ == "__main__":
    main()
