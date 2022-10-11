import os

import typer

app = typer.Typer()


@app.callback()
def callback():
    """Start Bali App"""


@app.command()
def http():
    os.system("python3 main.py launch --http")


@app.command()
def rpc():
    os.system("python3 main.py launch --rpc")


@app.command()
def event():
    os.system("python3 main.py launch --event")
