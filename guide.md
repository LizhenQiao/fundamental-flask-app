> This file basically explains how to run the project.

### Prepare  
- Import dataset into your MySQL system. The simplest way of doing this is importing '/ece1779_project1.sql' .
- Build your virtual environment for python.
    > python -m venv venv

    After create your own venv, you could activate it, your subsequent development should based on this virtual environment.
    > venv/Scripts/activate

    This is for Windows, Macos have other command pretty similar.

- Use the requirements.txt to download all dependencies in one time.
    > pip install -r requirements.txt

    One thing worth mentioning is that after each time you add some new dependencies. Before push your code to the repository. You should run the command below. This will update the dependencies in the requirement.txt
    > pip freeze > requirements.txt

By now, you've got your development environment ready.

### Run the code.
Just type in the command below.
    
    > python run.py