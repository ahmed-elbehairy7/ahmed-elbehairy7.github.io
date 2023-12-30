from pam import HeroApp, InApp

blog = HeroApp('blog', '00.00.00', 'web', 'Ai affiliate blog', '24/12/2023', ['Ahmed Elbehairy' , 'Mohamed Elmalah'], execute=False)
posts = InApp('posts', '00.00.01', '24/12/2023', 'Automation', blog)

if __name__ == "__main__":
    blog.printApps()
    blog.printApplication()