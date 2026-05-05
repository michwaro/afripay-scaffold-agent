"""Command-line interface for AfriPay."""

import typer
from rich.console import Console

app = typer.Typer(help="Generate secure African payment and communications API scaffolds.")
console = Console()


@app.callback()
def root() -> None:
    """Generate secure African payment and communications API scaffolds."""


@app.command()
def scaffold(
    provider: str = typer.Option(..., "--provider", help="Provider name, for example mpesa."),
    framework: str = typer.Option(..., "--framework", help="Target framework, for example fastapi."),
) -> None:
    """Generate a placeholder scaffold for a provider and framework."""
    console.print(f"{provider} scaffold for {framework} coming soon")


def main() -> None:
    """Run the AfriPay CLI."""
    app()
