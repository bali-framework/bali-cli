import re
from os import system, makedirs
from pathlib import Path
from shutil import copyfile

import typer
import decamelize
from git import Repo
from jinja2 import PackageLoader, Environment, select_autoescape


def prepare_source_repo(work_dir: Path, repo_name: str) -> Path:
    source_repo_dir = work_dir.parent / repo_name
    source_repo = Repo(source_repo_dir)
    source_repo.git.checkout("master")
    source_repo.git.pull()
    source_repo.close()
    return source_repo_dir


def prepare_current_repo(work_dir: Path) -> Path:
    dst_dir = work_dir / "clients" / "intermediates"
    makedirs(dst_dir, exist_ok=True)
    return dst_dir


def compile_proto_file(output_dir: Path, proto_file_name: str) -> None:
    options = [f"-I{output_dir}", f"--python_out={output_dir}", f"--grpc_python_out={output_dir}"]
    system(f"python -m grpc_tools.protoc {' '.join(options)} {proto_file_name}")


def compile_client_file(proto_path: Path, service_name: str):
    service_pattern = re.compile(r"^service (.*) {$")
    rpc_pattern = re.compile(r"\s+ rpc (.*?)[(](.*?)[)] returns [(](.*?)[)] {")

    # 按照项目约定，一个 proto 文件中只有一个 service
    service, methods = None, []
    with proto_path.open() as f:
        for i in f.readlines():
            _service = service_pattern.match(i)
            _rpc = rpc_pattern.match(i)
            if _service:
                service = _service.group(1).strip()
            if _rpc:
                methods.append([i.strip() for i in _rpc.groups()])

    env = Environment(
        loader=PackageLoader("cli"),
        autoescape=select_autoescape(["jinja2"]),
    )
    env.filters["decamelize"] = decamelize.convert
    template = env.get_template("client.jinja2")
    content = template.render(
        service=service, methods=methods, filename=proto_path.name.split(".")[0]
    )
    with (proto_path.parent / f"{service_name}_client.py").open(mode="w") as f:
        f.write(content)


def get_newest_proto_file_to_current_repo(repo_name: str, service: str) -> None:
    work_dir = Path.cwd()
    typer.echo(f'> Current work directory is {work_dir}')

    source_repo_dir = prepare_source_repo(work_dir, repo_name)
    dst_dir = prepare_current_repo(work_dir)

    # 拷贝 proto 文件
    proto_file_name = f"{service}.proto"
    dst_proto_path = dst_dir / proto_file_name
    copyfile(
        source_repo_dir / service / proto_file_name,
        dst_proto_path,
    )

    compile_proto_file(dst_dir, proto_file_name)
    compile_client_file(dst_proto_path, service)
    system(f"pb2py {dst_dir / f'{service}_pb2.py'} > {dst_dir / f'{service}_schema.py'}")
