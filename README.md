# PylapseNG
*All it does is timelapses.*

Seriously, that's really it.

---

### Why?

A friend and I were getting really sick of no super-simple timelapse software packages existing for Windows, MacOS, or Linux so we basically took the *"Fine, i'll just have to do it myself."* approach to software development and made our own. Thus, PylapseNG was born.

PylapseNG is based (in concept) on my earlier Pylapse project, which you will never see here because that code is a dumpster fire. Hence, the "NG" stands for "Next Generation" as this is much better.

Fun fact: I wrote all the code for the first version of this project in just over an hour.

---

### How?

Making cross-platform software sucks, so PylapseNG relies heavily on built-in Python libraries and only has one dependancy: OpenCV. Thankfully OpenCV runs on basically anything, so as long as `pip` or whatever you use can get it installed, it should be fine.

Here's how each library is used:
* `cv2`:
    - Camera discovery.
    - Image capture.
    - Realtime video generation.
    - Preview windows.
* `os`:
    - Output file initialization.
    - "Save as" path discovery.
* `sys`:
    - Program exiting.
* `time`:
    - A single `sleep()` call.
* `tkinter`:
    - Every message box you see.
    - Every dialog box you use.

There really isn't a lot going on, as you can see. However, PylapseNG does do something somewhat cool: It uses the `VideoWriter` class built into OpenCV to write to the output video in real-time, which keeps the overall disk usage down. In addition, there's no waiting for something to finish "compiling" the video, which is nice.

---

### Demo

https://github.com/sykeben/PylapseNG/assets/33205078/1dce673d-5c9e-48a4-a24c-f3737056266c

See? Super easy!
