import sys, random, argparse
import numpy as np
import math
 
from PIL import Image
 
# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = '@%#*+=-:. '

# 10 levels of numeric grey
gscale3 = '0896453271'

# luminocity groups. Char will be chosen randomly from each group
lumaGroups = ['086','4', '7', '1']
 
def getAverageL(image):

    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)
 
    # get shape
    w,h = im.shape
 
    # get average
    return np.average(im.reshape(w*h))
 
def covertImageToAscii(fileName, cols, scale, borderWidth, borderChar):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2, gscale3, lumaGroups
 
    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')
 
    # store dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))
 
    # compute width of tile
    w = W/cols
 
    # compute tile height based on aspect ratio and scale
    h = w/scale
 
    # compute number of rows
    rows = int(H/h)
     
    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
 
    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
 
    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
 
        # correct last tile
        if j == rows-1:
            y2 = H
 
        # append an empty string
        aimg.append("")
 
        for i in range(cols):
 
            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
 
            # correct last tile
            if i == cols-1:
                x2 = W
 
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
 
            # get average luminance
            avg = int(getAverageL(img))
            
            # find which luma group tile corresponds to
            lumaNumber = int((avg*(len(lumaGroups)-1))/255)

            # pick a random value within that group for the tile
            gsval = lumaGroups[lumaNumber][random.randint(0, len(lumaGroups[lumaNumber])-1)]
            
            topBorderWidth = round(borderWidth / 2.0)
            # check if current tile is part of the border and if so change it to borderChar
            if (j in [*[r for r in range(0, topBorderWidth)], *[r for r in range(rows-topBorderWidth, rows)]]) or (i in [*[c for c in range(0, borderWidth)], *[c for c in range(cols-borderWidth, cols)]]):
                gsval = borderChar
            
            # append ascii char to string
            aimg[j] += gsval

     
    # return txt image
    return aimg
 
# main() function
def main():
    # create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--border', dest='border', action='store_true', required=False)
    parser.add_argument('--borderWidth', dest='borderWidth', required=False)
    parser.add_argument('--borderChar', dest='borderChar', required=False)
 
    # parse args
    args = parser.parse_args()
   
    imgFile = args.imgFile
 
    # set output file
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile
 
    # set scale default as 0.43 which suits
    # a Courier font
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
 
    # set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)
    
    # set border
    borderWidth = 0
    if args.border:
        borderWidth = 3
    if args.borderWidth:
        borderWidth = int(args.borderWidth)

    # set borderChar
    borderChar = '0'
    if args.borderChar:
        borderChar = args.borderChar

    print('generating ASCII art...')
    # convert image to ascii txt
    aimg = covertImageToAscii(imgFile, cols, scale, borderWidth, borderChar)

    # write to file
    with open(outFile, 'w') as f:
        for row in aimg:
            f.write(row + '\n')

        print("ASCII art written to %s" % outFile)
 
# call main
if __name__ == '__main__':
    main()
