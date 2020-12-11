# Dumble

GZM hack to matchmake GZM members #MarriagePact #TraditionalFamilyValues #Feminism

Maintainers: 
andrew (msg @andrew in GZM discord for help)
Eric (@erictrimbs#6511 on Discord)


## Quickstart
1. Clone the source
`git clone git@github.com:ajroberts0417/dumble.git`

2. Navigate into the project directory
`cd dumble`

3. Install dependencies
`pipenv install`

4. Create a bot account and add it to your test discord server following this guide https://discordpy.readthedocs.io/en/latest/discord.html

5. Create a file `.env` with keys AIRTABLE_API_KEY, AIRTABLE_BASE, and DISCORD_TOKEN from Airtable and from the Discord bot in the format: KEY="[ key ]"

6. Enter the pipenv virtual environment
`pipenv shell`

7. Run the bot:
`python matchmaker.py`

Boom! You're now hosting Dumble locally.

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
