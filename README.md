Hand Tracking Arcade Game

Quick Summary

A simple, real-time computer vision arcade game where players use their index finger to "hit" a virtual target on screen, scoring points upon successful collision. Built using MediaPipe for hand tracking and OpenCV for video capture and display.

Setup & Run

Install:

pip install opencv-python mediapipe numpy


Run:
Save the code as main.py and execute

Bash

python main.py

⚙️ Core Logic

The game works by:

Using MediaPipe to detect and locate the pixel coordinates of the INDEX_FINGER_TIP.


Implementing simple collision detection to check if the finger tip falls within a small bounding box around the target circle.


Incrementing the score and resetting the target's random position on a successful hit.


✨ Features & Improvements

Features: Real-time Hand Tracking, Collision Detection, Scoring System.

Ideas for Contribution: 
Add a timer, 
implement difficulty levels,
or use a different gesture (like a closed fist) for the hit action.
