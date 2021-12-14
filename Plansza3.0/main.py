from Render import Render

if __name__ == "__main__":
    print("czy chcesz grac z SI? y/n")
    gametype = input()
    gametype = gametype.startswith("y")
    render = Render(gametype)
    render.run()
