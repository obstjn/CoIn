# CoIn v2                                                                                             
This is a simple documentation for the **Co**ndition **In**vestigator (CoIn) version 2.0.             
                                                                                                      
## Installation                                                                                       
CoIn consists of 4 different Python scripts: `DataGen.py`, `Param2d.py`, `gui.py` and `CoIn.py`.   
                                                                                                      
To execute them you will need python3 and the packages `numpy`, `matplotlib` and **TODO:GUILIBRARY**.
You can install them with `requirements.txt` either systemwide or in a virtual environment:

#### Systemwide

* `git clone https://github.com/obstjn/CoIn.git`
* `cd CoIn`
* `pip install -r requirements.txt`

<!--
or

* `pip install numpy`
* `pip install matplotlib`
* `pip install TODO:GUILIBRARY`
-->

#### Virtual environment

Alternatively you may use a virtual environment to easily delete the packages later:


* ``sudo -H pip install virtualenv`` (if you don't have virtualenv installed)
* ``git clone https://github.com/obstjn/CoIn.git``
* ``cd CoIn``
* ``virtualenv venv`` (create virtualenv named 'venv')
* ``source venv/bin/activate`` (enter virtualenv; in Windows systems activate might be in ``venv/Scripts``)
* ``pip install -r requirements.txt`` (install application requirements)

## Execution

If you use the virtual environment you first need to activate it with ``source venv/bin/activate`` , then simply execute
```bash
python CoIn.py
```
With ``cache_2D_scan.npy`` placed in the same folder as the scripts you can try the example system, a system consisting of 5 piecewise linear functions.

## Usage

The use of CoIn should be self explanatory.
There is the main plot of the cobweb that shows the behaviour of the system and other windows where the parameters can be adjusted.

Since CoIn is written with matplotlib, it comes with nice features for [Interactive Navigation](https://matplotlib.org/3.2.2/users/navigation_toolbar.html).
The use of these features is highly recommended.

The 2D Parameter selector displays a 2D scan of the parameter space.
This Scan needs to be created beforehand with AnT.
To select parameters, simply click into a point in the scan.
A crosshair should appear and the parameter values are displayed at the top right.
Clicking outside the plot hides the crosshair.
For the crosshair to work you must not have any other tools of the interactive navigation selected (e.g. zoom-to-rectangle or panning).

**TODO: GUI USAGE**

## Quick Start

**TODO**

## Structure

The central point of the program is ``CoIn.py``.
It is responsible for the plots of the system that should be investigated. 
The other scripts are modules designed to aid the investigation, they mainly facilitate easy parameter selection and data generation.

``DataGen.py`` generates the data that is later plotted, ``Param2d.py`` provides an intuitive way of selecting parameters based on a 2D-scan and with **TODO:GUI** the parameters can be easily adjusted.

``CoIn.py`` connects to ``DataGen.py`` via the `ant` object.
It is responsible for all the calculations.
With `ant`, the functions can be called and parameters can be accessed and set.

## Config 

This section describes how to configure CoIn and how to adapt it to your needs.
In general places that can (and should) be modified are marked with ``$$$$``.
This is often at the beginning of the file.

### DataGen.py

This module generates all the data.
Here you define your system and the functions generating the data.
Parameters and things you can change are:

* ``x_init`` The initial x that is iterated through the system. 
* ``iterations`` The number of iterations performed for the x value.
* ``f()`` The function defining the output value for a specific x.
* ``criticalpoints()`` The critical points of the system e.g. discontinuities in a piecewise linear map.

The system should be defined in the method ``f()``.
You should also specify the defaults/initial values of the parameters here.
You can name these parameters how you want, however there might be some changes needed in the ``CoIn.py`` module.
Namely the update functions access these parameters and for instance the initialization of the ``Cursor`` object (see section "Adding interactive controls").

Some parameters whose names shouldn't be changed are ``x_init`` and ``iterations``.
These are used in calculations of the other methods and should therefore stay with that name.

Additionally you should define the location of the criticalpoints in the method ``criticalpoints``.
It should return a list of these points, where one point is given by its (x,y)-coordinates.
You can change ``cp_iterations`` but don't have to, since it is usually overwritten by ``CoIn.py``. 
See section "CoIn.py" ``cp_initial`` for more details.

### Param2d.py

At the top there are several Parameters that can be adjusted:

* ``file_name`` String of the name of the ``*.tna`` file containing the 2D scan data.
* ``force_reload`` Bool indicating, if a new cache file should be created.
* ``dimensions`` (Integer-) Tupel (x,y) where x is the number of scan points in x-direction, same for y.
* ``L, R, D, U`` The bounds (float) of the parameters/2D-scan (left, right, down, up) e.g. ``L`` is the minimum of the Parameter in scanned in x-direction.
* ``xlabel, ylabel`` String labels for x and y-axis.

After the first execution a cache file is created named ``cache_2D_scan.py``.
This significantly speeds up the following startups.
You must delete old cache files if your 2D scan changes or you can set ``force_reload`` to `True`.
> If your `*.tna` file has a maximum bandcount that exceeds 127, you must change the data type when loading from txt.
> You can change `'b'` to `'i'` in the line containing ``img = np.loadtxt(file_name, ...)``.

You may disable the colorbar by commenting the line ``plt.colorbar()``.
Although not recommended you may change the color palette.

To properly integrate and use this tool, some adjustments in ``CoIn.py`` may be needed.
Specifically take a look at the ``update_cursor()`` method and see description in the following section CoIn.py.

### CoIn.py

In ``CoIn.py`` you can configure the plots.

* ``L, R, D, U`` The bounds of the cobweb plot (left, right, down, up) e.g. ``L`` is the minimum x value.
* ``x_range`` The range used to calculate the function plot. 
    Usually can stay as is.
    To have finer samples increase the third argument (number of points).
* ``cp_colors`` The colors used for the critical points.
    There should be as many colors as critical points.
* ``cp_initial`` A vector describing how many iterations of each critical point should be plotted.
    A `0` displays the critical point in the plot as a square but without iterations.
    To hide the critical point use `-1`. 
    For example `[4, 0, -1, -1, -1, -1, -1, -1]` performs 4 iterations for the first critical point, displays the second and hides the other 6.

##### Adding interactive controls.

The main benefit of CoIn is its interactive controls.
You can add The 2D Parameter selector by initializing the `Cursor()` object and connect it to button presses.

```python
cursor = Cursor(x_init=ant.aM3, y_init=ant.mM3)  # cursor with (optional) initial parameters 
cursor.fig.canvas.mpl_connect('button_press_event', update_cursor)
```

Everytime a mouse button is pressed the `update_cursor()` method is called.

The cursor should modify aM3 and mM3.
It is therefore initialized with these initial parameters.
However to modify these parameters the `update_cursor()` method needs to be adjusted.
Namely, the parameters that need to be changed must be connected to `x` and `y`.
For example, if the x-axis of my 2D scan describes the parameter `aM3`, I can connect it like so,

```python
ant.aM3 = x     
```

You can look for `$$$$` to find the line of code.

## Troubleshooting

#### There are a lot of gray pixels where there shouldn't be.

* Does your maximum bandcount exceed 127?
  If so, in ``Param2d.py`` you should change the data type, that is read, from byte to int.
  To do so, change `'b'` to `'i'` in the line 
  ```python
  img = np.loadtxt(file_name, dtype=np.dtype('b'), usecols=2))
  ```

#### The plotted 2D scan does not look like the one that I specified in `file_name`.

* Does the file `cache_2D_scan.npy` exist in the folder where `CoIn.py` is located?
  The program reads the cache instead of reloading from the `.tna` file.
  Either delete the file `cache_2D_scan.npy` or set `force_reload` in `Param2d.py` to `True`.
  Afterwards set it to `False` again for faster startup.
