from pathlib import Path
from filecmp import cmpfiles
from shutil import rmtree
from os import makedirs

import pytest
from git import Repo
from git.exc import NoSuchPathError, InvalidGitRepositoryError

from cli import biz


class TestPrepareSourceRepo:
    test_repo_name = "bali-cli-example-proto"
    work_dir = Path.cwd()

    @property
    def repo_base_git_url(self):
        return f"https://github.com/JoshYuJump/{self.test_repo_name}.git"

    @property
    def source_repo_dir(self):
        return self.work_dir.parent / self.test_repo_name

    def test_prepare_source_repo_with_repo_dir_not_exist(self):
        with pytest.raises(NoSuchPathError):
            biz.prepare_source_repo(self.work_dir, self.test_repo_name)

    def test_prepare_source_repo_with_repo_dir_exist_but_not_repo(self):
        self.source_repo_dir.mkdir()

        with pytest.raises(InvalidGitRepositoryError):
            biz.prepare_source_repo(self.work_dir, self.test_repo_name)

    def test_prepare_source_repo_with_repo_dir_exist_and_is_repo(self):
        self.source_repo_dir.mkdir()
        Repo.clone_from(self.repo_base_git_url, self.source_repo_dir)

        biz.prepare_source_repo(self.work_dir, self.test_repo_name)

        assert self.source_repo_dir.exists()
        Repo(self.source_repo_dir)

    def teardown_method(self):
        if self.source_repo_dir.exists():
            rmtree(self.source_repo_dir)

    setup_method = teardown_method


class TestPrepareCurrentRepo:
    work_dir = Path.cwd()
    test_repo_name = "bali-cli-example-proto"
    dst_dir = work_dir / "clients" / "intermediates"
    source_repo_dir = work_dir.parent / test_repo_name
    repo_base_git_url = f"https://github.com/JoshYuJump/{test_repo_name}.git"

    def setup_class(self):
        Repo.clone_from(self.repo_base_git_url, self.source_repo_dir)
        biz.prepare_source_repo(self.work_dir, self.test_repo_name)

    def teardown_class(self):
        rmtree(self.source_repo_dir)

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
    test_repo_name = "bali-cli-example-proto"
    dst_dir = work_dir / "clients" / "intermediates"
    service = "greeter"
    repo_base_git_url = f"https://github.com/JoshYuJump/{test_repo_name}.git"
    source_repo_dir = work_dir.parent / test_repo_name

    def setup_class(self):
        self.source_repo_dir.mkdir(exist_ok=True)
        Repo.clone_from(self.repo_base_git_url, self.source_repo_dir)

    def teardown_class(self):
        rmtree(self.source_repo_dir, ignore_errors=True)
        rmtree(self.dst_dir.parent, ignore_errors=True)

    def test_proto_file_equal(self):
        biz.get_newest_proto_file_to_current_repo(self.test_repo_name, self.service)

        assert cmpfiles(self.source_repo_dir, self.dst_dir, f"{self.service}.proto")
        assert (self.dst_dir / f"{self.service}_pb2.py").exists()
        assert (self.dst_dir / f"{self.service}_pb2_grpc.py").exists()
