from pathlib import Path

import click

from podder_task_cli.commands import Eject, Inspect, New, Process

from . import __version__


@click.group()
@click.version_option(__version__, prog_name="Podder Task CLI")
def main():
    pass


@main.command()
@click.argument('name')
def new(name: str):
    New(name=name, path=Path("./")).process()


@main.command()
@click.argument('name')
def process(name: str):
    Process(name=name, base_directory=Path("./")).process()


@main.command()
def inspect():
    Inspect(path=Path("./")).process()


@main.command()
def eject():
    Eject(path=Path("./")).process()
