from setuptools import setup

setup(
    name="podder-task-cli",
    install_requires=["click", "poetry"],
    entry_points={
        "console_scripts": [
            "podder=podder_task_cli.cli:main"
        ]
    }
)
