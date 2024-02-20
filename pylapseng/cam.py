# Perform imports.
import cv2

# Camera class.
class Camera:

    # Initializor.
    def __init__(self, portID:int):

        # Initialize properties.
        self.portID = portID
        self.camera = None
        self.size   = None

    # Open method.
    # Returns a success value.
    def open(self) -> bool:

        # Create object.
        camera = cv2.VideoCapture(self.portID)

        # Check if device is there.
        opened = camera.isOpened()
        if not(opened):
            return False
        
        # Check if device can capture images.
        reading, image = camera.read()
        if not(reading):
            return False

        # All is well, set it up.
        self.camera =  camera
        self.size   = (int(camera.get(3)), int(camera.get(4)))
        return True
    
    # Read method.
    # Returns success value and image.
    def read(self):
        return self.camera.read()
    
    # Close method.
    def close(self):
        self.camera.release()
        self.camera = None
        self.size   = None

# Camera list retreival method.
def getCameras(maxFails = 5) -> list[Camera]:

    # Initialize.
    cameras  = []
    numFails = 0
    
    # Test ports.
    thisPort = 0
    while (numFails <= maxFails):
        camera = Camera(thisPort)
        if (camera.open()):
            numFails = 0
            cameras.append(camera)
        else:
            numFails += 1
        thisPort += 1

    # Return list.
    return cameras
