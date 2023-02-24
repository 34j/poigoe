import click

from ._main import main


@click.command()
@click.option("--pitch", "-p", default=1, help="Pitch factor", type=float)
def cli(pitch: float) -> None:
    main(pitch)


cli()
