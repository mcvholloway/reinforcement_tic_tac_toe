import sys
import time
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from celluloid import Camera

FILENAME = 'log.json'

if __name__ == '__main__':
    i = sys.argv[1]
    with open(FILENAME, 'r') as fi:
        paths = json.load(fi)

    fig, ax = plt.subplots()
    camera = Camera(fig)

    path = paths[i]
    plt.title('Path {}'.format(i))

    for point in path:

        plt.hlines(y = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], xmin = -0.5, xmax = 4.5)
        plt.vlines(x = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], ymin = -0.5, ymax = 4.5)

        rect = Rectangle(xy = (3.5,3.5), width = 1, height = 1, color = 'lightblue')
        ax.add_patch(rect)

        rect = Rectangle(xy = (-0.5, 3.5), width = 1, height = 1, color = 'red')
        ax.add_patch(rect)
        
        ax.scatter(point[0], point[1], color = 'black', zorder = 100)
        camera.snap()
        #pts.remove()

animation = camera.animate()
animation.save('animation.gif', writer = 'imagemagick')
