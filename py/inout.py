from pam import find
from json import load, dump, dumps
from setup import inout
from os import path as os_path


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

def put_data(data, file, niche, key):
    with open(file) as file_obj:
        file_data = dict(load(file_obj))
    
    dump(file_data, fp=open(f"{file.split(".")[0]}_backup.{file.split(".")[1]}", "w"), indent=4)

    file_data[niche] = file_data.get(niche, {})
    file_data[niche][key] = {**file_data[niche].get(key, {}), **data}

    dump(file_data, fp=open(file, "w"), indent=4)

if __name__ == "__main__":
    print(inout)
