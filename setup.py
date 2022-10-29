# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Samuel JS Wright",
    description="Functions to make a plot Sankey diagram with Plotly",
    name = "sankey-diagrams",
    version = "0.1.0",
    packages=find_packages(include = ["sankey-diagrams", "sankey-diagrams.*"]),
    install_requires=["pandas >= 1.1.4", "numpy >= 1.23.3", \
        "plotly >= 5.11.0", "seaborn >= 0.12.1"],
    python_requires=">=3.6"
)