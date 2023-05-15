# AI helps PWR
Repository for [Hack4WroclawTech](https://hack4wroclawtech.my.canva.site/) hackhaton with project which will improve 
working at Wroclaw University of Science and Technology applying some AI solution.

## Installation
Required:
 - python 3.9
 - [poetry](https://python-poetry.org/)

The project uses [poetry](https://python-poetry.org/) tool. So you should have it preinstalled

```bash
poetry install  # create venv and install all dependencies
poetry shell  # activate venv
```

### Adding pre-commit hooks
```bash
pre-commit install
pre-commit run --all-files
```

## Running demo
```
demo_app
```
It should run streamlit app and open it in a browser.


## Use GPT
You should copy the config file from `config/config` to `config/config.local` and complete with your key.
```
[eventRegistry]
    apiKey = yourapiKey
```
Then you can use:
```
experiments/scripts/conversation.py
```
where example input prompt you can find in `data/test_prompt.json`