import pyautogui
from lib.WindowsObject import *
from win32 import win32gui

def setProperties():
    """
    Sets the pyatuogui properties to allow exiting the script during runtime.
    Moving the mouse to the upper left corner of the screen will exit the program.
    """
    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True

def hotkey(modifiers:'list', key:'string') -> 'void':
    """
    Takes in a list of modifiers and a key to press for the
    hotkey.
    """
    #Creates the print statement
    combo = "".join(map(lambda x: x.title() + " + ",modifiers))
    print("Pressing {}{} ...".format(combo, key.title()))

    for mod in modifiers:
        pyautogui.keyDown(mod)

    pyautogui.press(key)

    for mod in modifiers:
        pyautogui.keyUp(mod)

def waitForImageToAppear(imagePath:'string', retry=5) -> 'tuple':
    """
    Waits for the image to load. Each retry is
    about a 1 second wait.
    """
    print("Searching for image ({})...".format(imagePath))
    attempts = 0
    
    for i in range(retry):
        imageCoordTuple = pyautogui.locateOnScreen(imagePath)
        attempts = attempts + 1
        if(imageCoordTuple != None): #Image found                    
            time.sleep(1) #safety sleep to make sure it is loaded all the way
            print("Image ({}) found!".format(imagePath))
            return imageCoordTuple
        else:
            print("Image ({}) not found. Attempt ({})".format(imagePath, attempts))
            if(attempts == retry):
                raise LookupError
            time.sleep(1)

def centerMouseOnImage(imagePath, click=False, rightClick=False, retry=5):
    """
    Takes the image path and centers the mouse on that image. The retry
    parameter is the amount of times it will retry the search
    """
    try:
        x,y,xMid,yMid = waitForImageToAppear(imagePath, retry)
        
        #center coords on image
        print("Centering mouse on image ({})...".format(imagePath))
        x = x + int(xMid/2)
        y = y + int(yMid/2)
        
        if(click):
            print("Clicking ({})...".format(imagePath))
            moveToAndClick(x,y,isRightClick=rightClick)
        else:
            print("Moving mouse to ({},{})...".format(x,y))
            pyautogui.moveTo(x,y)
        return (x,y)
    except LookupError as e:
        raise LookupError("The image at ({}) was not found.".format(imagePath))

def moveToAndClick(x, y, isRightClick = False, isRelative = False, sleep = 0):
    """
    Moves the mouse to the coordinates and clicks.
    """
    clickOption = "right" if isRightClick else "left"
    time.sleep(sleep)
    
    if(isRelative):
        pyautogui.moveRel(x, y)
    else:
        pyautogui.moveTo(x, y, duration=0.25)
        
    pyautogui.click(button=clickOption)

def calculateRelativeMovesFromCoord(x:'int', y:'int', nextMoves:'list<tuple>') ->'list<tuple>':
    """
    Takes in a starting coord and a list of destination coordinates.
    Returns a list of relative move instructions to string together
    the moves from the start.
    """
    relativeMoves = []
    currentX = x
    currentY = y
    for nextMove in nextMoves:
        relativeMoves.append((nextMove[0]-currentX, nextMove[1]-currentY))
        currentX = nextMove[0]
        currentY = nextMove[1]
    return relativeMoves        

def printAllWindows():
    """
    Prints all of the window titles found on the computer to the console.
    """
    placeholder = None
    win32gui.EnumWindows(printAllWindowsCallback, placeholder)

def printAllWindowsCallback(handle, placeholder):
    """
    Callback function for printAllWindows. Prints out window titles
    that aren't empty.
    """
    windowTitle = win32gui.GetWindowText(handle)
    if (len(windowTitle.strip()) != 0):        
        print("-------------------------------")
        print(windowTitle)
    return True

def displayMouseCoordinatesLoop():
    """
    Displays the position of the mouse to the console every second.
    Use a keyboard interrupt to stop the loop. (CTRL + C)
    """
    while True:
        mousePositionTuple = pyautogui.position()
        print("Mouse Position: ({}, {})".format(mousePositionTuple[0],mousePositionTuple[1]))
        time.sleep(1)

if __name__ == '__main__':
    pass
