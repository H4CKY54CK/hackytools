import os
import sys
from PIL import Image
import argparse


def gifit(args=None, directory=None):

    if directory is None:
        source = args.source
    if not args.output.endswith('.gif'):
        output = f"{args.output.rstrip('.gif')}.gif"
    else:
        output = args.output

    frames = []
    for item in os.scandir(source):
        img = Image.open(item.path)
        frames.append(img.copy())

    frames[0].save(output, save_all=True, append_images=frames[1:], loop=0)
    print(f"Gif {output} created. Enjoy!")
    if sys.platform == 'win32':
        os.system(output)
