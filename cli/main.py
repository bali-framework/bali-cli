from typer import Typer

from cli import biz, options

app = Typer()


@app.command()
def add(service: str, remote: str = options.PROTO_REPO_GIT_URL):
    """add input_service_name's proto_file to current_dir/service_name"""
    biz.get_newest_proto_file_to_current_repo(service, remote)


@app.command()
def update(service: str, remote: str = options.PROTO_REPO_GIT_URL):
    """update input_service_name's proto_file to current_dir/service_name"""
    biz.get_newest_proto_file_to_current_repo(service, remote)
