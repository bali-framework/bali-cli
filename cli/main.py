import os

import typer

from cli import biz, __version__
from . import run

app = typer.Typer()


@app.command()
def add(service: str, target_dir: str = ''):
    """Add input_service_name's proto_file to current_dir/service_name"""
    proto_repo = 'proto'

    typer.echo(f'{os.linesep} 🏝 bali-cli v{__version__}')
    typer.echo(f'{os.linesep} 🚀 Start adding {service} ...')
    biz.add_service(proto_repo, service, target_dir=target_dir)
    typer.echo(f'{os.linesep} ✅ Service added successfully !')


@app.command()
def build():
    """Compile proto_file under cwd/services/rpc"""
    typer.echo(f'{os.linesep} 🏝 bali-cli v{__version__}')
    typer.echo(f'{os.linesep} 🚀 Start build ...')
    biz.build_service()
    typer.echo(f'{os.linesep} ✅ Service build successfully !')


@app.command()
def shell():
    """Enter Bali App shell"""
    os.system("python3 main.py launch --shell")


app.add_typer(run.app, name="run")
