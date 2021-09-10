from PIL import Image

from os import listdir
from os.path import isfile, join

mypath = 'resources/pieces/white'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for file in onlyfiles:

    image = Image.open(join(mypath, file))
    new_image = image.resize((100, 100))
    new_image.save(join(mypath, file))
