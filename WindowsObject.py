import time
from win32 import win32gui
from win32.lib import win32con

class WindowsObject:
    """
    This object will be used in order to save the window handle information
    gathered from the win32gui.EnumWindows function.
    """
    def __init__(self, title):
        self._initWindowsObject(title)
        
    def getHandle(self):
        return self._handle
    def setHandle(self, handle):
        self._handle = handle

    def getTitle(self):
        return self._title
    def setTitle(self, title):
        self._title = title

    def maximizeWindow(self):
        """
        Maximizes the specified window.
        """
        print("Maximizing {}...".format(self.getTitle()))
        win32gui.ShowWindow(self.getHandle(), win32con.SW_MAXIMIZE)
    
    def moveWindow(self, x, y, width, height):
        """
        Moves the specified WindowsObject to the screen coordinates.
        The width and the height dimensions are applied to the window.
        """
        print("Moving {} to position ({},{})...".format(self.getTitle(), x, y))
        win32gui.MoveWindow(self.getHandle(), x, y, width, height, False)

    def moveWindowToTop(self):
        """
        Moves the WindowsObject to the top.
        """
        print("Moving {} to the top...".format(self.getTitle()))
        #win32gui.SetForegroundWindow(self.getHandle())
        self.maximizeWindow()
    

    def _initWindowsObject(self, windowTitle):
        """
        Initializes the object with the specified window title and the win32
        handle that matches the title. If the window is not found, a KeyError
        is raised.
        """
        self.setTitle(windowTitle)
        if not(self._getWindowsObjectHandle()):
            raise KeyError("Window not found: " + self.getTitle())

    def _getWindowsObjectHandle(self):
        """
        Saves the handle for a window that matches the title property of the object.
        If found, a StopIteration should be raised.
        This function catches the error and returns True. If not found, return False.
        """
        try:
            win32gui.EnumWindows(self._getWindowsObjectHandleCallback, self)
        except StopIteration as e:
            return True
        return False

    def _getWindowsObjectHandleCallback(self, handle, windowsObject):
        """
        Callback function needed for getWindowsObjectHandle. Will save the handle
        into the WindowsObject if correct title found. If found, raises a StopIteration
        in order to stop the search. Else, returns True to continue the search.
        """
        title = win32gui.GetWindowText(handle)
        if (title == windowsObject.getTitle()):
            windowsObject.setHandle(handle)
            raise StopIteration #stop the enumeration by raising StopIteration
        return True

    @staticmethod
    def anchorWindow(windowTitle, x, y):
        """
        Anchors the specified window to the specified coordinates. The window will be resized
        to 1920 x 1080 to ensure consistency.
        """
        windowsObject = WindowsObject(windowTitle)
        windowsObject.moveWindow(x, y, 1920, 1080)
        windowsObject.moveWindowToTop()
        windowsObject.maximizeWindow()
        time.sleep(1)

    @staticmethod
    def sleepUntilWindowIsInitialized(windowTitle, maxCount):
        """
        Sleeps until the specified window is initialized.
        """
        print("Waiting until {} initializes...".format(windowTitle))
        failsafeCount = 0
        while(failsafeCount != maxCount):
            try:
                #If windowTitle not found, it throws a KeyError
                window = WindowsObject(windowTitle) 
                time.sleep(2)
                break;
            except KeyError as e:
                print("Waiting...")
                time.sleep(1)
                failsafeCount = failsafeCount + 1
        print("Window initialized")
