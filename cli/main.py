import os
import typer

from cli import biz

app = typer.Typer()


@app.command()
def add(service: str):
    """add input_service_name's proto_file to current_dir/service_name"""
    typer.echo(f'{os.linesep} 🚀 Start adding {service} ...')
    biz.get_newest_proto_file_to_current_repo("proto", service)
    typer.echo(f'{os.linesep} ✅ Service added successfully !')
