# Perform imports.
print("\nPerforming imports...")
from . import cam
from . import ui
from . import util
import cv2
import os
import sys
import time
import tkinter.simpledialog as sd
import tkinter.filedialog   as fd
import tkinter.messagebox   as mb
print("Libraries ready.")

# Set configuration.
print("\nSetting configuration...")
camFails    = 5
initialDir  = os.path.expanduser("~/Desktop")
windowName  = "PylapseNG"
print("Configuration ready.")

# Get a list available cameras.
print("\nFinding cameras...")
cameras = cam.getCameras(camFails)
print(f"Found {len(cameras)} camera{util.lenSuffix(cameras)}.")
if (len(cameras) <= 0):
    print("No usable cameras found, cannot continue.")
    mb.showerror(
        "Fatal Error", 
          "No cameras could be found.\n\n"
        + "Please check your connections."
    )
    sys.exit()

# Select a camera.
print("\nAsking user to choose a camera...")
port = ui.chooseInt(
    "Setup: Camera",
      "Choose a camera:\n\n"
    + "\n".join([f"{c.portID}: {c.size[0]} x {c.size[1]}" for c in cameras]),
    [c.portID for c in cameras],
    cameras[0].portID
)
if (port is None):
    print("No camera was selected, cannot continue.")
    mb.showerror(
        "Fatal Error",
          "No camera selected."
    )
    sys.exit()
print(f"Will use camera on port {port}.")

# Release other cameras.
print("\nReleasing any other cameras...")
camera = None
for c in cameras:
    if (c.portID == port):
        camera = c
    else:
        c.close()
print(f"Released {len(cameras)-1} camera{util.lenSuffix(cameras, offset=-1)}.")
cameras.clear()

# Select a capture interval.
print("\nAsking user to choose an interval...")
interval = sd.askfloat(
    "Setup: Interval",
      "How many seconds between each capture?\n\n"
    + "Minimum interval is 0.1 seconds.\n"
    + "An interval of 1-5 second(s) is recommended.",
    initialvalue=1.0, minvalue=0.1
)
if (interval is None):
    print("No interval was selected, cannot continue.")
    mb.showerror(
        "Fatal Error",
          "No interval selected."
    )
    sys.exit()
print(f"Will use an interval of {interval} second{util.numSuffix(interval)}.")

# Select an output framerate.
print("\nAsking user to choose an output framerate...")
framerate = sd.askfloat(
    "Setup: Output Framerate",
      "What will the framerate of the output be?\n\n"
    + "Minimum framerate is 0.1 FPS.\n"
    + "Maximum framerate is 120 FPS.\n"
    "A framerate of 30 or 60 FPS is recommended.",
    initialvalue=30.0, minvalue=0.1, maxvalue=120.0
)
if (framerate is None):
    print("No output framerate was selected, cannot continue.")
    mb.showerror(
        "Fatal Error",
          "No output framerate selected."
    )
    sys.exit()
print(f"Will use an output framerate of {framerate} FPS.")

# Choose an output file.
print("\nAsking user to choose an output file...")
outputPath = fd.asksaveasfilename(
    confirmoverwrite=True,
    defaultextension=".mp4",
    filetypes=[
        ("MPEG-4 video", "*.mp4"),
        ("all files",    "*")
    ],
    initialdir=initialDir,
    title="Setup: Output File"
)
if (outputPath is None) or (outputPath == "") or (outputPath == ()):
    print("No output file was selected, cannot continue.")
    mb.showerror(
        "Fatal Error",
          "No output file selected."
    )
    sys.exit()
print(f"Will output to file: {outputPath}")

# Remove old output file, if it exists.
if (os.path.isfile(outputPath)):
    print("\nOutput file already exists, deleting the old one...")
    try:
        os.remove(outputPath)
    except:
        print("File could not be removed, cannot continue.")
        mb.showerror(
            "Fatal Error",
              "Output file could not be overwritten."
        )
        sys.exit()
    print("File removed successfully.")

# Open output writer.
print("\nOpening output writer...")
fourCC = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(outputPath, fourCC, framerate, camera.size)
print("Output ready.")

# Set up preview window.
print("\nSetting up preview window...")
cv2.namedWindow(windowName)
cv2.setWindowProperty(windowName, 1, cv2.WINDOW_NORMAL)
cv2.resizeWindow(windowName, 512, 512)
def updateWindowTitle(newMessage:str|None = None) -> None:
    cv2.setWindowTitle(windowName, f"{windowName} ({newMessage})" if newMessage else windowName)
print("Ready.")

# Display a preview, if requested.
print("\nAsking the user about possibly previewing the output before starting...")
updateWindowTitle("Not running")
if (mb.askyesno(
    "Setup: Preview",
    "Would you like to preview the camera output before starting your capture?"
)):
    print("Giving instructions...")
    mb.showinfo(
        "Instructions",
        "When you are ready to capture, press any key on the following window."
    )
    print("Previewing...")
    updateWindowTitle("Press any key to start capture")
    key = 0xFF
    while (key == 0xFF):
        result, image = camera.read()
        if result:
            cv2.imshow(windowName, image)
            key = cv2.waitKey(100) & 0xFF
        else:
            print("Camera capture failed, cannot continue.")
            mb.showerror(
                "Fatal Error",
                  "Camera capture failed."
            )
            sys.exit()
    print("Preview closed, waiting for a few seconds...")
    time.sleep(1.5)
    print("Done.")
else:
    print("User did not request a preview before capturing.")

# Start capture.
print("\nStarting capture...")
print("Giving instructions...")
updateWindowTitle("Not running")
mb.showinfo(
    "Instructions",
    "When you are ready to end the capture, press any key on the following window."
)
print("Capture running...")
updateWindowTitle("Press any key to finish capture")
key = 0xFF
while (key == 0xFF):
    result, image = camera.read()
    if result:
        cv2.imshow(windowName, image)
        writer.write(image)
        key = cv2.waitKey(int(interval * 1000)) & 0xFF
    else:
        print("Camera capture failed, ending capture early.")
        mb.showerror(
            "Error",
              "Camera capture failed.\n\n"
            + "A partial output will still be available."
        )
        key = 0x00
print("Capture complete.")

# Close all preview windows.
print("Closing preview window...")
cv2.destroyAllWindows()
print("Done.")

# Finalize output.
print("Finalizing output...")
writer.release()
print("Completed.")
mb.showinfo(
    "Capture Complete",
      "Output saved to the following path:\n\n"
    + outputPath
)
