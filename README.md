# 3DEngine
Simple 3D renderer in Python

Uses pygame for display screen and drawing.
This engine is capable of displaying simple meshes of obj files. 
For this project I wanted to use linear algebra to implement 3D projection onto a 2D surface.
My original plan was to use this to create a more fleshed out game engine, but I realized it would make more
sense to just use a library. 
However, before I finished, I figured out how to rotate the camera the same way video games do it, where pitching
up and down is localized to the camera's "right" vector, and yawing is done around the world axis.
I then quickly implemented a simple way to control the camera using a mouse.
The effect is certainly not polished, but still gave off the feel of a video gaame.
