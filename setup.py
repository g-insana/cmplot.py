import setuptools

with open("README_brief.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmplot",
    version="0.9.0",
    author="Dr Giuseppe Insana",
    author_email="insana@insana.net",
    description="Cloudy Mountain Plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/g-insana/cmplot.py",
    license='AGPL',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: AGPL License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "plotly",
        "numpy",
        "pandas",
        "scipy"
    ],
    python_requires='>=3.6',
)