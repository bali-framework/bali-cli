from pathlib import Path
from os import makedirs
from filecmp import cmpfiles
from shutil import rmtree

from git import Repo

from cli import biz, options


class TestPrepareSourceRepo:
    work_dir = Path.cwd()
    source_repo_dir = work_dir.parent / options.PROTO_REPO_GIT_URL.split("/")[-1]

    def test_prepare_source_repo_with_repo_dir_not_exist(self):
        biz.prepare_source_repo(self.work_dir, options.PROTO_REPO_GIT_URL)

        assert self.source_repo_dir.exists()
        _ = Repo(self.source_repo_dir)

    def test_prepare_source_repo_with_repo_dir_exist_but_not_repo(self):
        self.source_repo_dir.mkdir()

        biz.prepare_source_repo(self.work_dir, options.PROTO_REPO_GIT_URL)

        assert self.source_repo_dir.exists()
        _ = Repo(self.source_repo_dir)

    def test_prepare_source_repo_with_repo_dir_exist_and_is_repo(self):
        self.source_repo_dir.mkdir()
        Repo.clone_from(options.PROTO_REPO_GIT_URL, self.source_repo_dir)

        biz.prepare_source_repo(self.work_dir, options.PROTO_REPO_GIT_URL)

        assert self.source_repo_dir.exists()
        _ = Repo(self.source_repo_dir)

    def teardown_method(self):
        if self.source_repo_dir.exists():
            rmtree(self.source_repo_dir)

    setup_method = teardown_method


class TestPrepareCurrentRepo:
    work_dir = Path.cwd()
    dst_dir = work_dir / "clients" / "intermediates"

    def setup_class(self):
        biz.prepare_source_repo(self.work_dir, options.PROTO_REPO_GIT_URL)

    def teardown_class(self):
        source_repo_dir = self.work_dir.parent / options.PROTO_REPO_GIT_URL.split("/")[-1]
        rmtree(source_repo_dir)

    def teardown_method(self):
        if self.dst_dir.exists():
            rmtree(self.dst_dir.parent)

    setup_method = teardown_method

    def test_clients_dir_exist_but_intermediates_not_exist(self):
        makedirs(self.dst_dir, exist_ok=True)
        self.dst_dir.rmdir()

        biz.prepare_current_repo(self.work_dir)

        assert self.dst_dir.exists()

    def test_clients_dir_exist_and_intermediates_exist(self):
        makedirs(self.dst_dir, exist_ok=True)

        biz.prepare_current_repo(self.work_dir)

        assert self.dst_dir.exists()

    def test_clients_dir_not_exist(self):
        makedirs(self.dst_dir, exist_ok=True)
        parent = self.dst_dir.parent
        self.dst_dir.rmdir()
        parent.rmdir()

        biz.prepare_current_repo(self.work_dir)

        assert self.dst_dir.exists()


class TestGetNewestProtoFileToCurrentRepo:
    work_dir = Path.cwd()
    source_repo_dir = work_dir.parent / options.PROTO_REPO_GIT_URL.split("/")[-1]
    dst_dir = work_dir / "clients" / "intermediates"
    service = "user"

    def teardown_method(self):
        if self.source_repo_dir.exists():
            rmtree(self.source_repo_dir)

        if self.dst_dir.exists():
            rmtree(self.dst_dir.parent)

    setup_method = teardown_method

    def test_proto_file_equal(self):
        biz.get_newest_proto_file_to_current_repo(self.service, options.PROTO_REPO_GIT_URL)

        assert cmpfiles(self.source_repo_dir, self.dst_dir, f"{self.service}.proto")
        assert (self.dst_dir / f"{self.service}_pb2.py").exists()
        assert (self.dst_dir / f"{self.service}_pb2_grpc.py").exists()
