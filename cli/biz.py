from os import system, makedirs
from shutil import copyfile
from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError


def prepare_source_repo(work_dir: Path, remote: str) -> Path:
    parent_dir = work_dir.parent
    source_repo_dir = parent_dir / remote.split("/")[-1]
    try:
        source_repo = Repo(source_repo_dir)
    except (NoSuchPathError, InvalidGitRepositoryError):
        source_repo_dir.mkdir(exist_ok=True)
        source_repo = Repo.clone_from(remote, source_repo_dir)
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


def get_newest_proto_file_to_current_repo(service: str, remote: str) -> None:
    work_dir = Path.cwd()
    source_repo_dir = prepare_source_repo(work_dir, remote)
    dst_dir = prepare_current_repo(work_dir)

    # 拷贝 proto 文件
    proto_file_name = f"{service}.proto"
    copyfile(
        source_repo_dir / service / proto_file_name,
        dst_dir / proto_file_name,
    )

    compile_proto_file(dst_dir, proto_file_name)
