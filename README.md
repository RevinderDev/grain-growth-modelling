# Grain growth modelling
Simple application written in python to showcase cellular automatons. 
It uses very naive approach of drawing grid of squares and to see how the system would change over time.
You can read about them more [here](https://en.wikipedia.org/wiki/Cellular_automaton).

# Features
* Allows for different grid sizes
* Supported neighbourhoods: [Moore](https://en.wikipedia.org/wiki/Moore_neighborhood), [Von Neumann](https://en.wikipedia.org/wiki/Von_Neumann_neighborhood), Hexagonal Left/Right, Random Hexagonal and Random Pentagonal.
* Periodical and non periodical neighbourhoods (meaning they can or cannot cross over border).
* Initialize system with: random grains on random positions, evenly distributed or randomized with specified radius.
* Ability to pause and start on a whim.

# Example gif!

![](https://media.giphy.com/media/chzxShioR2Msc0RE3H/giphy.gif)

# Installation and running
Create venv first:
```
$ virtualenv $(your_project_name)
```
Run venv:
```
[Linux]   $ source $(your_project_name)/bin/activate 
[Windows] C:\$(your_project_dir)\Scripts\activate
```

Install all dependencies:
```
$ pip install -r requirements.txt
```
To run use:
```
$ python main.py
```

# Last words

You cannot have 2 opens at one time.
The limitation sadly comes from the PyGame library which is used to draw said grid as it can have only one context window at once.
Feel free to download the code and play with it however you like. Don't expect too much of it, as it was only students project from years ago and it does include
some terrible design flaws. Have fun!