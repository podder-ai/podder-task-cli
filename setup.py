from setuptools import setup

setup(
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "podder = podder_task_cli:cli:main"
        ]
    }
)