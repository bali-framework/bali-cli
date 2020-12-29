from pathlib import Path
from filecmp import cmpfiles
from shutil import rmtree
from os import makedirs

from git import Repo

from cli import biz


class TestGetNewestProtoFileToCurrentRepo:
    work_dir = Path.cwd()
    source_repo_dir = work_dir.parent / "proto"
    dst_dir = work_dir / "clients" / "intermediates"
    service = "hello_world"
    proto_content = """
    syntax = "proto3";
    // The greeting service definition.
    service Greeter {
      // Sends a greeting
      rpc SayHello (HelloRequest) returns (HelloReply) {}
    }
    
    // The request message containing the user's name.
    message HelloRequest {
      string name = 1;
    }
    
    // The response message containing the greetings
    message HelloReply {
      string message = 1;
    }
    """

    def setup_class(self):
        Repo.init(self.source_repo_dir, mkdir=True)
        service_dir = self.source_repo_dir / self.service
        service_dir.mkdir(exist_ok=True)
        proto = service_dir / f"{self.service}.proto"
        with proto.open(mode="w+") as f:
            f.write(self.proto_content)

        makedirs(self.dst_dir, exist_ok=True)

    def teardown_class(self):
        rmtree(self.source_repo_dir, ignore_errors=True)
        rmtree(self.dst_dir.parent, ignore_errors=True)

    def test_proto_file_equal(self):
        biz.get_newest_proto_file_to_current_repo(self.service)

        assert cmpfiles(self.source_repo_dir, self.dst_dir, f"{self.service}.proto")
        assert (self.dst_dir / f"{self.service}_pb2.py").exists()
        assert (self.dst_dir / f"{self.service}_pb2_grpc.py").exists()
