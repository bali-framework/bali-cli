import typer

from cli import biz

app = typer.Typer()


@app.command()
def add(service: str):
    """add input_service_name's proto_file to current_dir/service_name"""
    typer.echo(f'Start adding {service} ...')
    biz.get_newest_proto_file_to_current_repo("proto", service)


@app.command()
def update(service: str):
    """update input_service_name's proto_file to current_dir/service_name"""
    biz.get_newest_proto_file_to_current_repo("proto", service)
