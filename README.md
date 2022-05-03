### Dependency setup

In `environment.yml` and `requirement.txt` at the root folder, you can use them for project dependencies.  `environment.yml` is for setting up conda and `requirement.txt is for setting up venv.

The yaml file is generater bu using `conda create --name dev --file environment.yml`

### Install dependencies

For conda `conda install --name dev --file environment.yml`, it will direct you to the dev virtual enviroment

Alternatively, if you want to setup virtualenv, you first do `pip install virtualenv` to install the virtualenv package. Then you run `virtualenv venv` To create a virtualenv called venv. Depends on your operating system, you will be running either commands below to activate the environment:

on Mac OS / Linux
`sourcevenv/bin/activate`

On Windows
`venv\Scripts\activate`


### Run Programme
Method 1: 
activate conda environment as above, then run `python main.py` in current folder

Method 2: 
1. Set up development environment in jupyter notebook, using command 
`python -m ipykernel install --user --name=dev`
2. Go to Jupyter notebook, open up the `Run_Programme.ipynb`
3. Select 'dev' to be your kernel
3. Press run to run the project

