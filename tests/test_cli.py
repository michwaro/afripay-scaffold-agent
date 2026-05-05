from typer.testing import CliRunner

from afripay.cli import app


def test_scaffold_command_prints_placeholder() -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["scaffold", "--provider", "mpesa", "--framework", "fastapi"],
    )

    assert result.exit_code == 0
    assert "mpesa scaffold for fastapi coming soon" in result.output
