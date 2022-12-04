# CSE-6140-project

## Instructions
### Running exec.py
To execute the code as set by the project requirements: 
<br>
`$ python -m exec -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>`
<br>
<br>
### Running exec.py on all graphs using all algorithms
To generate all solution and trace files from all algorithms running on all graphs: 
<br>
`$ python -m runner -inst <directory of graphs> -time <cutoff in seconds> -seed <random seed>`
<br>
<br>
## Dependencies
* `numpy`
* `psutil`