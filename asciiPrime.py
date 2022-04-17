import random, argparse, sys, datetime
import numpy as np
import cWrapper
 
from PIL import Image
 
# luminocity groups. Char will be chosen randomly from each group
luminosityGroups = ['089','4', '73', '1']
 
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
    global luminosityGroups, rows
 
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
    asciiImage = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
 
        # correct last tile
        if j == rows-1:
            y2 = H
 
        # append an empty string
        asciiImage.append("")
 
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
            luminosityNumber = int((avg*(len(luminosityGroups)-1))/255)

            # pick a random value within that group for the tile
            gsval = luminosityGroups[luminosityNumber][random.randint(0, len(luminosityGroups[luminosityNumber])-1)]
            
            topBorderWidth = round(borderWidth / 2.0)
            # check if current tile is part of the border and if so change it to borderChar
            if (j in [*[r for r in range(0, topBorderWidth)], *[r for r in range(rows-topBorderWidth, rows)]]) or (i in [*[c for c in range(0, borderWidth)], *[c for c in range(cols-borderWidth, cols)]]):
                gsval = borderChar
            
            # append ascii char to string
            asciiImage[j] += gsval

    # return txt image
    return asciiImage
 
# main() function
def main():

    # ------------------------------- ARGUMENT PARSER ---------------------------------
    # create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--border', dest='border', action='store_true', required=False)
    parser.add_argument('--borderWidth', dest='borderWidth', required=False)
    parser.add_argument('--borderChar', dest='borderChar', required=False)
 
    # parse args
    args = parser.parse_args()
   
    imgFile = args.imgFile
 
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
    borderWidth = 1
    if args.border:
        borderWidth = 3
    if args.borderWidth:
        borderWidth = int(args.borderWidth)

    # set borderChar
    borderChar = '1'
    if args.borderChar:
        if int(borderChar) % 2 == 0:
            print("borderChar must be an odd number!")
            sys.exit(0)

        borderChar = args.borderChar

    # ------------------------------- Generate Ascii image ---------------------------------

    print('generating ASCII art...\n')
    # convert image to ascii txt
    asciiImage = covertImageToAscii(imgFile, cols, scale, borderWidth, borderChar)

    #print image to terminal
    for row in asciiImage:
        print(row)

    # ------------------------------- Estimate calc time ---------------------------------

    # estimate how long it will take to primify the image
    durationForSingleCheck = cWrapper.estimateCalcDuration(asciiImage, numberOfPrimeChecks=25, numberOfTrails=30)

    # probability of a number of the order 10^(cols*rows) being prime
    power = cols*rows
    primeProbability = (9*power - 1 ) / (9*power *(power + 1) * np.log(10))

    # function that returns number of trails needed to find a prime with probability S
    probableTrailCountEstimate = lambda S: np.log(1 - S) / np.log(1 - primeProbability)

    # display time estimates for different probabilities
    print('\n')
    for prob in [0.5, 0.9, 0.99, 0.999]:
        print(f"Estimated time to find prime with {100*prob:.1f}% probability: {str(datetime.timedelta(seconds=round(durationForSingleCheck * probableTrailCountEstimate(prob))))}")

    # ------------------------------- Ask user if they want to primify the image ---------------------------------

    # ask user if they want to move on
    print('\nWould you like to primify this image? (y/n)')
    ans = input('--> ')
    print('')

    if ans != 'y' and ans != 'Y':
        print('Image not primified.\nTerminating program.')
        sys.exit(0)

    # ------------------------------- PRIMIFY IMAGE ---------------------------------
    asciiImage = cWrapper.primify(asciiImage, cols, rows, borderWidth, luminosityGroups, numberOfPrimeChecks=25)

    # print image to terminal
    print("\nYour primified image:\n")
    for row in asciiImage:
        print(row)


# call main
if __name__ == '__main__':
    main()
