**Introduction**
================

Preface
-------

I've written various die rolling programs for various computers over the decades. Every computer language had its own way of randomly generating numbers for dice results. These were pseudo random results, but still pseudo random enough to be useful for what I needed. I remember writing a Risk! game on the computer, and programming the die rolls needed for comparisons between players. That was back in 1989. I wish I still had listings from that program. And from others. That was back when computer programmers printed out their program listings and desk-checked them in 24-hour restaurants at 2am.

The reason I wrote a "calculator" for Mongoose Traveller 2nd Edition was because I had tried some from other programmers (most of them were web-based and for Classic Traveller, if I recall), but none of them did more than 2D rolls. I'm guessing by now they do, because more people are playing Mongoose Traveller 2nd Edition.

Anyway, at the time when I first made this program, I didn't know how to write programs that ran in the browser. So my other option was to write the program in Windows, and use whatever GUI for Python that looked best. At the time, it was `PyQt
<https://en.wikipedia.org/wiki/PyQt>`__ that I liked. `wxPython
<https://en.wikipedia.org/wiki/WxPython>`__ and `Tkinter
<https://en.wikipedia.org/wiki/Tkinter>`__ didn't have nearly the ease-of-use and production value that PyQt had.

Seven years ago, when I released very early versions that would eventually lead up to this program's design, I knew that very few people were still using computers. Most were using their phones to roll dice on. I see the reasons for it. I happen to have a computer while I play Traveller online with other players. So my program is right there on the screen if needed.

Now that I know how to program for the browser, I might one day try doing this for the web. We'll have to see.

-Shawn


Requirements
------------

* **Microsoft Windows**
   
   **PyTravCalc** is being tested on Windows 10.
   It has not been tested on MacOS or Linux.
   
* **Python 3.9**
   
   **PyTravCalc** was written using the C implementation of Python
   version 3.9. Also known as CPython.
   
* **PyQt5 5.15.4**

   PyQt5 is the framework used for displaying the Window GUI and buttons, etc.

* **numpy 1.20.2**

   For building arrays.

* **matplotlib 3.4.2**

   For graphics plotting.
   
.. Warning::
   **PyTravCalc** will not work with **Python 2.7-**.
   

Not Using Python?
-----------------

You can always run the .EXE version for Windows 10 if you don't have the Python language installed.
