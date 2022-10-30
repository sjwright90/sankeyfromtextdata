# sankey-diagrams
Make a sankey diagram

This file contains a series of functions used to transform and manipulate tabular text data into
a format appropriate for drawing a Sankey diagram and then producing said sankey diagram.
The tabular data does already need to be in a specific format. Each column should represent 
one event (in this case a given class offered in a given year). Each row will be an individual 
path through said events (in this case the grades a student got in a given class). Each cell 
contains the given result of the individual and that event (for example a "B" in "Calc1_2020"). 
The functions were built assuming string data would be the input, but I think numerical data 
would work. The intent of this work was to make a Sankey plot to track how students flowed 
through a series of college courses, the data set provided as an example is just randomly 
generated data, but shows how the process works. I believe the code should be highly adaptable 
to any instance where one is trying to make a sankey plot of categorical data, again some 
formating of your data set might be needed before it will work though.

The repository is set up as a library so I could install it on my local machine, I have not pushed it to PyPI as a) I do not think there is enough here to warrant distribution and b) I have not had the time to build a test file. I just set it up as a package because I was using it in multiple different scripts and was sick of copy pasting the functions. If you pull the whole repository it should be good to go for installing it locally.

To install clone the repository, navigate to the top level and run
```
~/local/path/sankeydiagrams>pip3 install -e .
```
Would be best to set up a virtual environment first just in case

```
>conda create -n NAMEYOURENV
>conda activate NAMEYOURENV
```
then do the local install, it should auto install all dependencies.

<p align="center">
 <img src= https://github.com/sjwright90/masterfigures/blob/main/sankeyplotofgrades.png height="500" width="2000"/>
    <br>
    <em>Figure 1: Example of script output</em>
</p>
