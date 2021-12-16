import sys

from Render import Render

if __name__ == "__main__":
    render = Render()
    render.run()
    del render
    sys.exit()

