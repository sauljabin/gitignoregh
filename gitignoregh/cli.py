import click

from gitignoregh import __version__
from gitignoregh.gitignoregh import Gitignoregh


class Cli:
    def __init__(self):
        self.gitignoregh = Gitignoregh()

    def run(self, print, search, list, gitignore_id):
        self.gitignoregh.init()

        if list:
            self.gitignoregh.print_all_gitignore_files()
            return

        if search:
            self.gitignoregh.print_gitignore_files_by_id(gitignore_id)
            return

        if print:
            self.gitignoregh.print_gitignore_by_id(gitignore_id)
            return

        if gitignore_id:
            self.gitignoregh.save_gitignore_by_id(gitignore_id)
            return

        with click.get_current_context() as context:
            click.echo(context.get_help())


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--print", "-p", is_flag=True, help="Print a gitignore file.")
@click.option(
    "--search", "-s", is_flag=True, help="Search gitignore templates and shows a list."
)
@click.option("--list", "-l", is_flag=True, help="List all found gitignore templates.")
@click.version_option(__version__)
@click.argument("gitignore_id", metavar="<gitignore id>", nargs=1, required=False)
def main(print, search, list, gitignore_id):
    cli = Cli()
    cli.run(print, search, list, gitignore_id)


if __name__ == "__main__":
    main()
