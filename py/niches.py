from itertools import product
from setup import niches
from pam import find
from json import load, dump


def main():
    initial_niches = dict(load(open(find("products.json"))))

    content_niches = dict(load(open(find("niches.json"))))

    initial_niches = expand_niches(initial_niches)

    for key in content_niches:
        content_niches[key]["products"] = initial_niches[key]["products"]

    join_niches(initial_niches, content_niches)


def join_niches(beta_niche, alpha_niche):

    dump(
        dict(list(beta_niche.items()) + list(alpha_niche.items())),
        open(find("niches.json"), "w"),
        indent=4,
    )


def expand_niches(niches: dict):
    """Function to expand niches and posts for every niche"""
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


if __name__ == "__main__":
    print(niches)

    main()
