import sys
import os
import argparse
import math
from PIL import Image

def sliceit(args):

    startup = [args.source]
    images = []
    while startup:
        if os.path.isdir(startup[0]):
            for item in os.scandir(startup[0]):
                startup.append(item.path)
        else:
            images.append(startup[0])
        startup.pop(0)

    with Image.open(args.source) as img:
        if args.rows and args.columns:
            args.width = img.width / args.columns
            args.height = img.height / args.rows
        height = img.height
        width = img.width
    rows = math.ceil(height / args.height)
    cols = math.ceil(width / args.width)
    total = rows * cols

    zf = len(str(total))
    x = 0
    y = 0
    xx = args.width
    yy = args.height
    z = 0
    img = Image.open(args.source)
    while True:
        base, ext = os.path.splitext(args.source)
        output = f"{base}-{str(z).zfill(zf)}{ext}"
        if xx > width:
            x = 0
            xx = args.width
            y += args.height
            yy += args.height
        if yy > height:
            print(f"Sliced out a total of {total} images!")
            sys.exit()
        box = (x,y,xx,yy)
        img.crop(box).save(output)
        x += args.width
        xx += args.width
        z += 1

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help="source image to slice")
    parser.add_argument('-x', '--width', dest='width', type=int)
    parser.add_argument('-y', '--height', dest='height', type=int)
    parser.add_argument('-r', '--rows', dest='rows', type=int)
    parser.add_argument('-c', '--columns', dest='columns', type=int)

    parser.set_defaults(func=sliceit)
    args, options = parser.parse_known_args(argv)
    if not args.width and not args.height and options and not args.rows and not args.columns:

        args.width = int(options[0])
        args.height = int(options[1])
    if not isinstance(args.height, int) and not isinstance(args.width, int) and not args.rows and not args.columns:
        parser.error('error')

    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
