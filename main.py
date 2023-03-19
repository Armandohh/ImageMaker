import random
from enum import Enum
import numpy
import fileinput

# constants
MAX_WIDTH = 800
MAX_HEIGHT = 800
MAX_COLOR = 255


# COLOR enum
class COLOR(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


# used for the s triangle
class PointT:
    x = 0
    y = 0


# IMAGEMAKER CLASS
class ImageMaker:
    # variables
    magic = ""
    height = 0
    width = 0
    pen_red = 0
    pen_green = 0
    pen_blue = 0
    image = numpy.zeros((MAX_WIDTH, MAX_HEIGHT, 3), dtype=int)

    # default constructor
    def __init__(self):
        self.height = 0
        self.width = 0
        self.pen_red = 0
        self.pen_blue = 0
        self.pen_green = 0

        # initialize image variable to white
        for i in range(MAX_HEIGHT):
            for j in range(MAX_WIDTH):
                self.image[j, i, COLOR.RED.value] = MAX_COLOR
                self.image[j, i, COLOR.GREEN.value] = MAX_COLOR
                self.image[j, i, COLOR.BLUE.value] = MAX_COLOR

    '''
    # SETTERS --------------------------------------------------------------
    # set the height
    def setHeight(self, height):
        #check for valid height
        if height < 0 or height > MAX_HEIGHT:
            raise Exception ("Height Out of Bounds!")

        #set height
        self.height = height

    # set the width
    def setWidth(self, width):
        # check for valid height
        if width < 0 or width > MAX_WIDTH:
            raise Exception("Width Out of Bounds!")

        # set height
        self.width = width

    # set the red pen
    def setRedPen(self, newR):
        # check for valid red pen color value
        if newR < 0 or newR > MAX_COLOR:
            raise Exception("Color Value Invalid!")

        # set red pen
        self.pen_red = newR

    # set the green pen
    def setGreenPen(self, newG):
        # check for valid green pen color value
        if newG < 0 or newG > MAX_COLOR:
            raise Exception("Color Value Invalid!")
        # set green pen
        self.pen_green = newG

    # set the blue pen
    def setBluePen(self, newB):
        # check for valid blue pen color value
        if newB < 0 or newB > MAX_COLOR:
            raise Exception("Color Value Invalid!")

        # set blue pen
        self.pen_blue = newB
    '''

    # load an image onto our image matrix
    def loadImage(self, filename):
        # check that the file opens
        try:
            inputFile = open(filename, "r")
        except IOError:
            print("File failed to open!")

        # initialize image variable to white
        for i in range(MAX_HEIGHT):
            for j in range(MAX_WIDTH):
                self.image[i, j, COLOR.RED.value] = 255
                self.image[i, j, COLOR.GREEN.value] = 255
                self.image[i, j, COLOR.BLUE.value] = 255

        # variables to be read from file
        magicNumber = ""
        number = 0
        r = 0
        g = 0
        b = 0

        # check for magic number P3
        magicNumber = inputFile.readLine()
        if magicNumber != "P3":
            raise Exception("Bad Magic Number")

        # set/check for width
        number = inputFile.readline()
        # SET WIDTH AFTER FUNCTION IS DONE
        number = inputFile.readline()
        # SET HEIGHT AFTER FUNCTION IS DONE

        # check for max color value
        number = inputFile.readline()
        if number != 255:
            raise Exception("Max Color Range is not 255")

        # load ppm image to image matrix
        for i in range(self.height):
            for j in range(self.width):
                r = inputFile.readLine()
                g = inputFile.readLine()
                b = inputFile.readLine()

                # check for bad pixel color
                if (r < 0 or r > MAX_COLOR) or (g < 0 or g > MAX_COLOR) or (b < 0 or b > MAX_COLOR):
                    raise Exception("Color Value Invalid!")
                # load rgb values to image matrix
                self.image[i, j, COLOR.RED.value] = r
                self.image[i, j, COLOR.GREEN.value] = g
                self.image[i, j, COLOR.BLUE.value] = b

        # close file
        inputFile.close()

    # save ppm image into a file
    def saveImage(self, filename):
        # create and open a text file
        outputFile = open(filename, "a")

        # check for non zero dimensions
        if self.height == 0 or self.width == 0:
            raise Exception("Image Must Have Non-Zero Dimensions!")

        # save header information to file
        outputFile.write("P3\n" + str(self.width) + " " + str(self.height) + "\n" + str(MAX_COLOR) + "\n")

        # save rgb values from image matrix onto the file
        for i in range(self.height):
            for j in range(self.width):
                outputFile.write(str(self.image[i, j, COLOR.RED.value]) + " ")
                outputFile.write(str(self.image[i, j, COLOR.GREEN.value]) + " ")
                outputFile.write(str(self.image[i, j, COLOR.BLUE.value]) + " ")

        # close the file
        outputFile.close()

    # draw a pixel
    def drawPixel(self, x, y):
        # check if point is in bounds
        if not self.pointInBounds(x, y):
            raise Exception("Point Out of Bounds!")

        self.image[y][x][COLOR.RED.value] = self.pen_red
        self.image[y][x][COLOR.GREEN.value] = self.pen_green
        self.image[y][x][COLOR.BLUE.value] = self.pen_blue

    # draw a line
    def drawLine(self, x1, y1, x2, y2):
        # check if points are in bounds
        if not self.pointInBounds(x1, y1) or not self.pointInBounds(x2, y2):
            raise Exception("Point Out of Bounds!")

        # variables
        slope = 0.0
        b = 0.0
        lowestY = 0
        highestY = 0
        lowestX = 0
        highestX = 0

        # find the highest x coordinate value
        if x1 < x2:
            lowestX = x1
            highestX = x2
        else:
            lowestX = x2
            highestX = x1

        # check if points are the same, if so behave like DrawPixel
        if x1 == x2 and y1 == y2:
            self.drawPixel(x1, y1)
            return
        # check for vertical lines
        elif x1 == x2:
            # find highest y value
            if y1 < y2:
                lowestY = y1
                highestY = y2
            else:
                lowestY = y2
                highestY = y2

            # draw pixels to mak the vertical line
            for i in range(lowestY, highestY + 1):
                self.drawPixel(x1, i)
            return
        # draw horizontal line
        else:
            # calculate slope
            slope = float(y2 - y1) / float(x2 - x1)

            # calculate y intercept
            b = y2 - (slope * x2)

            # draw pixels to make horizontal line
            for i in range(lowestX, highestX + 1):
                # draw pixel using x value and formula to figure out y coordinate
                self.drawPixel(i, int(round(slope * i) + b))

    # draw a rectangle
    def drawRectangle(self, x1, y1, x2, y2):
        # call draw line to draw the rectangle
        self.drawLine(x1, y1, x2, y2)

    # check if point is in bounds
    def pointInBounds(self, x, y):
        # check that x and y coordinates arent out of bounds and that we have non zero dimensions
        if (x < 0 or x > self.width) or (y < 0 or y > self.height) or (self.width == 0 or self.height == 0):
            return False
        else:
            return True


# drawing a house using image maker
img = ImageMaker()

# set the size of the house to 450x450
img.width = 450
img.height = 450

# draw a brown roof
img.pen_red = 165
img.pen_green = 42
img.pen_blue = 42
img.drawLine(50, 200, 200, 50)
img.drawLine(200, 50, 350, 200)
img.drawLine(50, 200, 350, 200)

# draw brick walls
img.pen_red = 255
img.pen_green = 50
img.pen_blue = 57

# draw 25x20 bricks
for y in range(200, 400, 20):
    for x in range(100, 300, 25):
        img.drawRectangle(x, y, x + 25, y + 20)

# draw a brown door
img.pen_red = 165
img.pen_green = 42
img.pen_blue = 42

for y in range(280, 401):
    img.drawLine(175, y, 225, y)

img.saveImage("redBrickHouse.ppm")

# -----------------------------------------
# draw a sierpinski triangle
img2 = ImageMaker()

# set the height and width
img2.width = 800
img2.height = 800

# create a list of Point T's
pts = []
pts.append(PointT())
pts.append(PointT())
pts.append(PointT())

# set the x
pts[0].x = img2.width / 2
pts[1].x = 0
pts[2].x = img.width - 1

# set the y
pts[0].y = 0
pts[1].y = img2.width - 1
pts[2].y = img2.width - 1

# create a Point T
r = PointT
r.x = 41
r.y = 67

for i in range(1000000):
    p = PointT
    p = pts[random.randint(0, 2)]
    x = (p.x + r.x) / 2
    y = (p.y + r.y) / 2

    img2.drawPixel(int(x), int(y))

    r.x = x
    r.y = y

img2.saveImage("caca.ppm")
