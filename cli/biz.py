import os
import re
from pathlib import Path
from shutil import copyfile

import typer
import decamelize
from git import Repo
from jinja2 import PackageLoader, Environment, select_autoescape

jinja2_env = Environment(
    loader=PackageLoader("cli"),
    autoescape=select_autoescape(["jinja2"]),
)
jinja2_env.filters["decamelize"] = decamelize.convert


def prepare_source_repo(work_dir: Path, repo_name: str) -> Path:
    source_repo_dir = work_dir.parent / repo_name
    source_repo = Repo(source_repo_dir)
    source_repo.git.checkout("master")
    source_repo.git.pull()
    source_repo.close()
    return source_repo_dir


# noinspection PyTypeChecker
def prepare_current_repo(work_dir: Path) -> Path:
    dst_dir = work_dir / "clients" / "intermediates"
    os.makedirs(dst_dir, exist_ok=True)
    return dst_dir


def compile_proto_file(output_dir: Path, proto_file_name: str) -> None:
    """Compile protobuf to pb2 & pb2_grpc files"""
    options = [f"-I{output_dir}", f"--python_out={output_dir}", f"--grpc_python_out={output_dir}"]
    os.system(f"python -m grpc_tools.protoc {' '.join(options)} {proto_file_name}")

    service = proto_file_name.replace(".proto", "")

    # Modified import in *_pb2_grpc.py files
    pb2_grpc_file = f'{service}_pb2_grpc.py'
    pb2_grpc_path: Path = output_dir / pb2_grpc_file
    with pb2_grpc_path.open(mode="r+") as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(
            f'import {service}_pb2 as',
            f'from . import {service}_pb2 as',
        ))


def compile_client_file(proto_path: Path, service_name: str):
    service_pattern = re.compile(r"^service\s+(.*?)\s+{$")
    rpc_pattern = re.compile(r"\s+rpc\s+(.*?)[\s(]+(.*?)[)\s]+returns[\s(]+(.*?)[)\s]+{")

    # 按照项目约定，一个 proto 文件中只有一个 service
    service, methods = None, []
    with proto_path.open(encoding='utf-8') as f:
        for i in f.readlines():
            _service = service_pattern.match(i)
            _rpc = rpc_pattern.match(i)
            if _service:
                service = _service.group(1).strip()
            if _rpc:
                methods.append([i.strip() for i in _rpc.groups()])

    template = jinja2_env.get_template("client.jinja2")

    # service is like `UserService`
    # service abbreviation is like `User`
    service_abbr_camelcase = service.replace('Service', '')
    service_abbr = decamelize.convert(service_abbr_camelcase)

    content = template.render(
        service=service,
        service_abbr=service_abbr,
        service_cls=f'{service_abbr_camelcase}Client',
        methods=methods,
        filename=proto_path.stem,
    )
    with (proto_path.parent / f"{service_name}_client.py").open(mode="w") as f:
        f.write(content)


def create_config_file(config_path: Path):
    if config_path.exists():
        return

    typer.echo(f"{os.linesep} !!!!! The generated file needs to be rewritten: {config_path} !!!!!")
    template = jinja2_env.get_template("config.jinja2")
    content = template.render()
    with config_path.open(mode="w") as f:
        f.write(content + os.linesep)


# noinspection PyTypeChecker
def create_init_file(init_path: Path):

    # get custom imports
    custom_imports = []
    try:
        with init_path.open(mode="r") as f:
            while True:
                # Read next line
                line = f.readline()
                # If line is blank, then you struck the EOF
                if not line:
                    break

                if 'intermediates' not in line and not line.startswith('#'):
                    if line.strip():
                        custom_imports.append(line.strip() + os.linesep)
    except FileNotFoundError:
        pass

    services = set()
    for _1, _2, filenames in os.walk(init_path.parent / "intermediates"):
        services |= {i.rsplit("_", 1)[0] for i in filenames if i.endswith("_client.py")}

    template = jinja2_env.get_template("clients.init.jinja2")
    content = template.render(services=sorted(list(services)))
    with init_path.open(mode="w") as f:
        f.write(content + os.linesep)

        f.write('# Custom imports' + os.linesep)
        for custom_import in custom_imports:
            f.write(custom_import)


def create_utils_file(utils_path: Path):
    template = jinja2_env.get_template("utils.jinja2")
    content = template.render()
    with utils_path.open(mode="w") as f:
        f.write(content + os.linesep)


# noinspection PyTypeChecker
def add_service(repo_name: str, service: str, target_dir: str) -> None:
    work_dir = Path.cwd()
    typer.echo(f' > Current work directory is `{work_dir}`')
    typer.echo(f' > Target client path is `{target_dir or "."}`')

    source_repo_dir = prepare_source_repo(work_dir, repo_name)

    # target dir
    client_dir = work_dir
    if target_dir:
        client_dir = client_dir / target_dir

    dst_dir = prepare_current_repo(client_dir)

    # copy proto files
    proto_file_name = f"{service}.proto"
    dst_proto_path = dst_dir / proto_file_name
    copyfile(
        source_repo_dir / service / proto_file_name,
        dst_proto_path,
    )

    compile_proto_file(dst_dir, proto_file_name)
    compile_client_file(dst_proto_path, service)
    os.system(f"pb2py {dst_dir / f'{service}_pb2.py'} > {dst_dir / f'{service}_schema.py'}")
    create_init_file(dst_dir.parent / "__init__.py")
    create_config_file(dst_dir.parent / "_config.py")
    create_utils_file(dst_dir.parent / "_utils.py")

    typer.echo()


def build_service() -> None:
    """Build protobuf files to python files

    Before v2.1.7, build command will find protobuf file in `/services/rpc`
    from v2.1.7, `/protos` is OK, and prefer.
    """
    current_dir = Path.cwd()
    proto_dirs = [
        current_dir / "protos",
        current_dir / "services" / "rpc",
    ]
    base_command = (
        'python3 -m grpc_tools.protoc '
        ' -I{dir} --python_out={dir} --grpc_python_out={dir} {file}'
    )

    for proto_dir in proto_dirs:
        for _1, _2, filenames in os.walk(proto_dir):
            for i in filenames:
                file = proto_dir / i
                if file.suffix == ".proto":
                    command = base_command.format(dir=proto_dir, file=i)
                    typer.echo(command)
                    os.system(command)
