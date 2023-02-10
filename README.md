# Tools package to develop Sankey Diagram from text data in tabular form

This package contains a series of functions used to transform and manipulate tabular text data into
a format appropriate for drawing a Sankey diagram and then producing said sankey diagram.

The tabular data does already need to be in a specific format. Each column should represent 
one event (in this case a given class offered in a given year). Each row will be an individual 
path through said events (in this case the grades a student got in a given class). Each cell 
contains the given result of the individual and that event (for example a "B" in the "Calc1_2020" column). 

The functions were built assuming string data would be the input, but I think numerical data 
would work. The intent of this work was to make a Sankey plot to track how students flowed 
through a series of college courses, the data set provided as an example is just randomly 
generated data, but shows how the process works. I believe the code should be highly adaptable 
to any instance where one is trying to make a sankey plot of categorical data, again some 
formating of your data set might be needed before it will work. The functions are set up
to handle missing values, but they need to be encoded as np.NaN.

To install clone the repository then navigate to the top level of the repository and from the command line run:
```
(base) user ~ % cd local/path/to/sankeyfromtextdata
(base) user sankeyfromtextdata % pip3 install -e .
```
Would be best to set up a virtual environment first to avoid clashes between dependencies

```
(base) user ~ % conda create -n NAMEYOURENV
(base) user ~ % conda activate NAMEYOURENV
(NAMEYOURENV) user ~ % cd local/path/to/sankeyfromtextdata
(NAMEYOURENV) user sankeyfromtextdata % pip3 install -e .
```
then do the local install, it will auto install all dependencies.

Once the package is installed load it to your workspace using

```
from sankeydiagrams import makesankeyfuncs as snkyfnc
```

<p align="center">
 <img src= https://github.com/sjwright90/sankeyfromtextdata/blob/main/images/sankeyplotofgrades.png height="500" width="2000"/>
    <br>
    <em>Figure 1: Example of script output</em>
</p>
