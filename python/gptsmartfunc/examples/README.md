# Jupyter Notebooks in vscode

To use a specific Poetry environment for Jupyter notebooks in Visual Studio Code:

Open a terminal in VSCode.
Activate the Poetry environment (usually with poetry shell or . $(poetry env info -p)/bin/activate).
Install the IPython kernel into your environment with python -m pip install ipykernel.
Add your virtual environment to Jupyter with python -m ipykernel install --user --name=myenv, where myenv can be replaced with a name for your environment.
Now, when you open a Jupyter notebook, you should be able to select your Poetry environment from the kernel list.
If VSCode doesn't recognize the kernel, you may need to point VSCode to the correct Python interpreter in your settings (.vscode/settings.json):

json
Copy code
{
    "python.pythonPath": "<path to your Poetry environment>/bin/python"
}
The <path to your Poetry environment> can be found with poetry env info -p.
