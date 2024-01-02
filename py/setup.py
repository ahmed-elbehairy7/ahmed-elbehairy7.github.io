from pam import HeroApp, InApp

blog = HeroApp(
    "blog",
    "00.00.00",
    "web",
    "Ai affiliate blog",
    "24/12/2023",
    ["Ahmed Elbehairy", "Mohamed Elmalah"],
    execute=False,
)
posts = InApp("posts", "00.00.01", "24/12/2023", "Automation", blog)

niches = InApp(
    "niches",
    "00.01.00",
    "1/1/2024",
    "Including the funcs responsible of expanding niches",
    blog,
)
inout = InApp(
    "inout",
    "00.00.01",
    "1/1/2024",
    "Including the i/o funcs to input and output data from and to json files",
    blog,
    execute=False,
)
if __name__ == "__main__":
    blog.printApps()
    blog.printApplication()
