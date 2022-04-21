from codecs import BufferedIncrementalEncoder
import random, argparse, sys, datetime
import numpy as np
import cWrapper
 
from PIL import Image
 
# luminocity groups. Char will be chosen randomly from each group
luminosityGroups = ['1', '73', '4', '089']

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

            # if no border then make sure first and last digits are odd, and not 5
            if borderWidth == 0:
                if (i == 0 and j == 0) or (i == cols-1 and j == rows-1):
                    if int(gsval) % 2 == 0 or int(gsval) % 5 == 0:

                        # first try to find odd digit in same luminosity group
                        for digit in luminosityGroups[luminosityNumber]:
                            if int(digit) % 2 != 0 and int(digit) % 5 != 0:
                                gsval = digit
                                break
                        
                        # if all are even then just use borderChar
                    if int(gsval) % 2 == 0 or int(gsval) % 5 == 0:
                        gsval = borderChar

            # looks better if border width on top is half of side border (aspect ratio) 
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
    global luminosityGroups
    # ------------------------------- ARGUMENT PARSER ---------------------------------
    # create parser
    descStr = "This program converts an image into a prime number that is also ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True, help='path to image file')
    parser.add_argument('--scale', dest='scale', required=False, help='Vertical scaling of input image to compensate for non square "ascii pixels"')
    parser.add_argument('--cols', dest='cols', required=False, help='width of the final ascii image')
    parser.add_argument('--borderWidth', dest='borderWidth', required=False, help='width of the border')
    parser.add_argument('--borderChar', dest='borderChar', required=False, help='character to use for border, must be and odd number')
    parser.add_argument('--invert', dest='invert', action='store_true', required=False, help='inverts colors of input image')
    parser.add_argument('--autoSave', dest='autoSave', action='store_true', required=False, help='automatically saves ascii art to file, without prompting user')
 
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
    borderWidth = 0
    if args.borderWidth:
        borderWidth = int(args.borderWidth)

    # set borderChar
    borderChar = '1'
    if args.borderChar:
        try: 
            int(args.borderChar)
        except ValueError:
            print("borderChar must be an odd digit and not 5")
            sys.exit(0)

        if int(args.borderChar) % 2 == 0 or int(args.borderChar) % 5 == 0:
            print("borderChar must odd and not 5!")
            sys.exit(0)

        borderChar = args.borderChar

    # set invert
    if args.invert:
        luminosityGroups = luminosityGroups[::-1]

    # set autoSave
    autoSave = False
    if args.autoSave:
        autoSave = True

    numberOfPrimeChecks = 25

    # ------------------------------- Generate Ascii image ---------------------------------

    print('generating ASCII art...\n')
    # convert image to ascii txt
    asciiImage = covertImageToAscii(imgFile, cols, scale, borderWidth, borderChar)

    #print image to terminal
    print('')
    for row in asciiImage:
        print(row)

    # ------------------------------- Estimate calc time ---------------------------------

    # estimate how long it will take to primify the image
    print("\nEstimating time to primify image...", end="")
    sys.stdout.flush()
    durationForSingleCheck = cWrapper.estimateCalcDuration(asciiImage, numberOfPrimeChecks=25, maxNumberOfTrails=100, maxDuration=10)

    # clear previous print
    print('', end="\r")

    # probability of a number of the order 10^(cols*rows) being prime
    power = cols*rows
    primeProbability = (9*power - 1 ) / (9*power *(power + 1) * np.log(10))

    # function that returns number of trails needed to find a prime with probability S
    probableTrailCountEstimate = lambda S: np.log(1 - S) / np.log(1 - primeProbability)

    # display time estimates for different probabilities
    for prob in [0.5, 0.9, 0.99, 0.999]:
        print(f"    {100*prob:.1f}% probability of finding prime within: {str(datetime.timedelta(seconds=round(durationForSingleCheck * probableTrailCountEstimate(prob))))}")

    # ------------------------------- Ask user if they want to primify the image ---------------------------------

    # ask user if they want to move on
    print('\nWould you like to primify this image? (y/n)')
    ans = input('--> ')
    print('')

    if ans != 'y' and ans != 'Y':
        print('Image not primified.')
        print("\n-------------------------------- Program Terminated --------------------------------\n")
        sys.exit(0)

    # ------------------------------- PRIMIFY IMAGE ---------------------------------
    asciiImage = cWrapper.primify(asciiImage, cols, rows, borderWidth, luminosityGroups, primeProbability, numberOfPrimeChecks)

    # print image to terminal
    print("\n------------------------------------- SUCESSFULLY PRIMIFIED IMAGE -------------------------------------\n")
    for row in asciiImage:
        print(row)

    # print extra info
    print(f'\nThe probability of this number being truly prime is:\t{(1- 0.25**numberOfPrimeChecks)*100:.20f}%')

    # ------------------------------- Ask user if they want to save the image ---------------------------------

    if not autoSave:
        print('\nWould you like to save this image? (y/n)')    
        ans = input('--> ')
        if ans != 'y' and ans != 'Y':
            print("\n-------------------------------- Program Terminated --------------------------------\n")
            sys.exit(0)

    # ------------------------------- SAVE IMAGE ---------------------------------

    fileName = imgFile.rsplit(".", 1)[0].rsplit("/", 1)[1] + f"_primified_cols_{cols}.txt"
    with open(fileName, "w") as f:
        
        f.write("\n------------------------------------- Sucessfully primified image -------------------------------------\n\n")

        for row in asciiImage:
            f.write(row + "\n")
        
        f.write("\n------------------------------------- Number as single string -------------------------------------\n\n")
        f.write(''.join(asciiImage))

        f.write("\n\n-------------------------------------------- Properties --------------------------------------------\n\n")
        f.write(f"Number of columns: {cols}\n")
        f.write(f"Number of rows: {rows}\n")
        f.write(f"Number of digits: {cols*rows}\n")

    print("\nSaved image to: ", fileName)
    print("\n-------------------------------- Program Terminated --------------------------------\n")



# call main
if __name__ == '__main__':
    main()
