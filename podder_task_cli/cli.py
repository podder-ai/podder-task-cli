from pathlib import Path

import click

from podder_task_cli.commands import (Analyze, Eject, Import, Inspect, New,
                                      Process)

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


@main.command()
@click.option('-j', '--json_output', 'json_output', is_flag=True)
def analyze(json_output):
    Analyze(path=Path("./")).process(json_output=json_output)


@main.command(name='import')
@click.option('-p', '--process', 'process_name', multiple=True)
@click.argument('target_repository')
def _import(process_name: str, target_repository: str):
    Import(target_repository=target_repository,
           processes=process_name,
           base_path=Path("./")).process()
