# RubikQuat
![Alt RubikQuatScreen](/docs/RubiqQuat_scr1_small.png)

RubikQuat is a 3D Rubik Simulator program, written entirelly in Python by means of [Pygame] modules. 
A simple 3D-Engine is implemented using only the basic 2D-graphics.
The orientation in space and rotation is calculated using Quaternions.
The purpose for which RubikQuat was created:
  - Learn Python and experiment with Pygame
  - Study Rubik's mechanics
  - Research Quaternions
  - Implement simple 3D-Engine

# Run
Using python:
```sh
$ python -m rubikquat_src
```
Under Windows:
There is a build for Windows (using py2exe) which allows to run the application even without Python. 
Unpack the content of the build_zip folder and execute .\build\rubikquat.exe.

# Help
![Alt RubikQuatHelp](/docs/RubiqQuat_help_small.png)

Help screen is displayed when RubikQuat application starts. It can also be invoked each time by pressing the F1 Key or clicking the '?'-button (top-left). Press Esc or mouse left-click to close the help and return to Rubik screen.
# Controls
| Key | Function | Key | Function |
| --- | -------- | --- | -------- |
| L | Flip Left-Face clockwise | Left | Rotate Rubik along Y-axis |
| Shift+L | Flip Left-Face counterclockwise | Right | Rotate Rubik along Y-axis |
| R | Flip Right-Face clockwise | Up | Rotate Rubik along X-axis |
| Shift+R | Flip Right-Face counterclockwise | Down | Rotate Rubik along X-axis |
| F | Flip Front-Face clockwise | Pg-Up | Rotate Rubik along Z-axis |
| Shift+F | Flip Front-Face counterclockwise | Pg-Down | Rotate Rubik along Z-axis |
| U | Flip Top-Face clockwise | Ctrl+Z | Undo the last move |
| Shift+U | Flip Top-Face counterclockwise | Ctrl+Y | Redo a move |
| F1 | Show Help | S | Scramble the Rubik |

You can also do all the above actions by clicking with mouse on corresponding button. 
Rotate the Rubik using mouse - just drag the Rubik in the direction you want to rotate it.
The mouse-wheel rotates the Rubik along Z-axis.

# Development
Clean the build:
```sh
> make clean
```
Build the .\build\rubikquat.exe using py2exe:
```sh
> make setup
```
Virtual environment:
```sh
> virtualenv venv
> venv\Scripts\activate
> pip install -r requirements.txt
```

# License
GNU GPL3. See the [LICENSE.md](LICENSE.md) file for details.

# Author
Igor Marinescu

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen.)

[Pygame]: <https://www.pygame.org>
