import click


class TerminalUtility(object):
    class Style:
        Normal = {"color": None, "bold": False},
        Info = {"color": "green", "bold": False},
        Warning = {"color": "yellow", "bold": False},
        Error = {"color": "red", "bold": False},
        Header = {"color": "green", "bold": True},

    @staticmethod
    def print(message: str, new_line=True, style: dict = Style.Normal):
        click.secho(message,
                    nl=new_line,
                    color=style["color"],
                    bold=style["bold"])
