from pathlib import Path

from podder_task_cli.services.podder_service.entities import Package


def test_package_config_load():
    path = Path(__file__).parent.parent.joinpath("_data", "podder.yaml")
    package = Package(path=path)
    assert package is not None
    assert package.name == "test"


def test_package_config_to_dict():
    path = Path(__file__).parent.parent.joinpath("_data", "podder.yaml")
    package = Package(path=path)
    dict_data = package.to_dict()
    assert dict_data is not None
    assert dict_data["name"] is not None
    assert len(dict_data["imports"]) == 2
