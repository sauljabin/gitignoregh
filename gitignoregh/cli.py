import click

from gitignoregh import __version__
from gitignoregh.gitignoregh import Gitignoregh


class Cli:
    def __init__(self):
        self.gitignoregh = Gitignoregh()

    def run(self, print, search, list, reset, gitignore_ids):
        if reset:
            self.gitignoregh.reset_repository()
            return

        self.gitignoregh.init()

        if list:
            self.gitignoregh.print_all_gitignore_files()
            return

        if search:
            self.gitignoregh.print_gitignore_files_by_id(gitignore_ids)
            return

        if print:
            self.gitignoregh.print_gitignore_by_id(gitignore_ids)
            return

        if gitignore_ids:
            self.gitignoregh.save_gitignore_by_id(gitignore_ids)
            return

        with click.get_current_context() as context:
            click.echo(context.get_help())


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--print", "-p", is_flag=True, help="Print a gitignore file.")
@click.option(
    "--search", "-s", is_flag=True, help="Search gitignore templates and shows a list."
)
@click.option("--list", "-l", is_flag=True, help="List all found gitignore templates.")
@click.option("--reset", is_flag=True, help="Reset the template source.")
@click.version_option(__version__)
@click.argument("gitignore_ids", metavar="<gitignore ids>", nargs=-1, required=False)
def main(print, search, list, reset, gitignore_ids):
    """
    gitignoregh is a CLI tool to search and generate gitignore file templates.
    Example: gitignoregh java gradle.
    """
    cli = Cli()
    cli.run(print, search, list, reset, gitignore_ids)


if __name__ == "__main__":
    main()
