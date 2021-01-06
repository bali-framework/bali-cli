from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["add", "quota"])
    assert result.exit_code == 0
