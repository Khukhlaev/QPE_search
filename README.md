# QPE_search

Right now some early drafts for detection algorithm and curves generation can be found here.

## Curve generation

2 classes for curve generation can be found in [`curve_generation.py`](curve_generation.py). 

First class named ```LightCurveGenerator``` can be used to generate single curve with predetermined parameters:

```python
from curve_generation import LightCurveGenerator

dt = 500.  # In sec, time bins size
noise_std_coef = 0.3  # noise std = noise_std_coef * noise_level

generator = LightCurveGenerator(noise_std_coef, dt)

params = {"number QPEs": 2, 
          "QPE 1": {"start": 4000, "width": 4000, "height": 0.07}, 
          "QPE 2": {"start": 35000, "width": 4000, "height": 0.05}
         }  # All in seconds
         
         
signal_duration = 60000 # In sec
noise_level = 0.01

signal, times = generator.generate(noise_level, signal_duration, params)
```

Second class named ```CurvesGenerator``` can be used to generate a chunck of curves with randomized parameters, all randomization is for now happening in ```CurvesGenerator._generate_params()``` method. Example:

```python
from curve_generation import CurvesGenerator

noise_std_coef = 0.3 # Noise std = noise_level * noise_std_coef 

curves_gen = CurvesGenerator(noise_std_coef)

result = curves_gen.generate_chunk(10)
```

In this example ```result``` is a list with size 10x3, for each curve ```result[i][0]``` is signal array, ```result[i][1]``` is times array, ```result[i][2]``` is QPE presence in the generated signal, either true or false.

More examples can be found in the notebook [`test_curve_generation.ipynb`](test_curve_generation.ipynb).


## Detection algorithm

Early version of detection algorithm can be found in [`detection.py`](detection.py), function which perform a check to determine whether the curve have QPE candidate in it is named ```check_curve```. It takes as arguments signal array, times array, errors array (now doesn't do anything), max_val and prominence. Right now checking is performed in 2 steps: 

1. Maximum value of signal / mean value of signal should be higher than max_val

2. Signal should contain at least one peak with prominence = signal mean * prominence (argument of the ```check_curve``` function)

What is prominence can be seen ["here"](https://en.wikipedia.org/wiki/Topographic_prominence).

Example of usage:

```python
>>> max_val = 2.5
>>> prominence = 2.5
>>> check_curve(signal, times, np.zeros_like(signal), max_val, prominence)
True
```

## Testing of detection algorithm

Testing function can be found in [`test_detection.py`](test_detection.py). It uses generated curve to check how well algorithm is performing. 


Example of usage:

```python
>>> max_val = 2.3
>>> prominence = 2.3
>>> num_curves = 1000
>>> true_positive, true_negative, false_positive, false_negative = test_detection(num_curves, max_val, prominence)
```


More examples can be found in the notebook [`detection_test_plots.ipynb`](detection_test_plots.ipynb).



