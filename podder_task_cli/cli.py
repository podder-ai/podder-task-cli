from pathlib import Path

import click

from podder_task_cli.commands import Inspect, New


@click.group()
def main():
    pass


@main.command()
@click.argument('name')
def new(name: str):
    New(name=name, path=Path("./")).process()


@main.command()
def inspect():
    pass
