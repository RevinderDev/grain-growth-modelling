# import the library
from appJar import gui

# handle button events
from src.grid_drawing import Grid, PyGameWindow


def press(button):
    if button == "Exit":
        app.stop()
    elif button == "Start":
        grid = Grid()
        pyWindow = PyGameWindow()

# create a GUI variable called app
app = gui("Login Window", "400x200")
app.setFont(18)

# link the buttons to the function called press
app.addButtons(["Start","Exit"], press)


# start the GUI
app.go()