# Dumble

GZM hack to matchmake GZM members #MarriagePact #TraditionalFamilyValues #Feminism

Maintainer: andrew (msg @andrew in GZM discord for help)


## Quickstart
1. Clone the source
`git clone git@github.com:ajroberts0417/dumble.git`

2. Navigate into the project directory
`cd dumble`

3. Install dependencies
`pipenv install`

4. Enter the pipenv virtual environment
`pipenv shell`

5. Run the bot:
`python matchmaker.py`

Boom! It's that easy -- you're now hosting Dumble locally.

## Contributing
Follow the quickstart guide to clone the source.

We use [Black](https://pypi.org/project/black/#:~:text=Black%20is%20the%20uncompromising%20Python,energy%20for%20more%20important%20matters.) for code formatting.
Before submitting code run: `pipenv run black .` to autoformat your code.

## Dependencies
- A version of python 3.8 installed and added to your PATH (for help: [install python 3](https://www.codecademy.com/articles/install-python3))
- A version of [pipenv](https://pypi.org/project/pipenv/) installed

## Installing Python
Managing python environments can be tricky, even for experienced developers. One easy tool to do so is [pyenv](https://github.com/pyenv/pyenv).
Here's how you can use a python 3.8 environment in your `dumble` directory:

1. Install pyenv (see [pyenv installer](https://github.com/pyenv/pyenv-installer))
`curl https://pyenv.run | bash` 

1.5.

2. Install the latest version of python 3.8 using pyenv
`pyenv install 3.8.6`

3. Use this version locally in your dumble project
(Note: make sure you're in the dumble directory)
`pyenv local 3.8.6`

3b. Alternatively, if you want 3.8.6 to be your global version of python:
`pyenv global 3.8.6`
