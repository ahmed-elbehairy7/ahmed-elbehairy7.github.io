from itertools import product
from setup import niches


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
