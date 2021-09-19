import os
import re

import git
from rich import box
from rich.console import Console
from rich.table import Table


class Gitignoregh:
    def __init__(self):
        self.repository = TemplatesRepository()
        self.gitignore_files = []

    def init(self):
        self.repository.init()
        self.load_gitignore_files()

    def load_gitignore_files(self):
        for dirpath, dirnames, filenames in os.walk(self.repository.path):
            filenames = [filename for filename in filenames if filename.endswith(".gitignore")]
            filenames.sort()
            for gitignore_path in filenames:
                self.gitignore_files.append(
                    Gitignore(os.path.join(dirpath, gitignore_path))
                )

    def print_all_gitignore_files(self):
        self.print_gitignore_files(self.gitignore_files)

    def print_gitignore_by_id(self, gitignore_id):
        gitignore_files = [
            gitignore
            for gitignore in self.gitignore_files
            if gitignore_id.lower() == gitignore.id.lower()
        ]

        if len(gitignore_files) == 0:
            console = Console()
            console.print("[red]Gitignore not found[red]")
        else:
            gitignore_files[0].load()
            gitignore_files[0].print()

    def print_gitignore_files_by_id(self, gitignore_id):
        gitignore_files = [
            gitignore
            for gitignore in self.gitignore_files
            if re.match(".*({}).*".format(gitignore_id).lower(), gitignore.id.lower())
        ]

        if len(gitignore_files) == 0:
            console = Console()
            console.print("[red]Gitignore files not found[red]")
        else:
            self.print_gitignore_files(gitignore_files)

    def print_gitignore_files(self, gitignore_files):
        console = Console()

        table = Table(box=box.HORIZONTALS)
        table.add_column("Id", style="cyan", justify="right")

        for gitignore in gitignore_files:
            table.add_row(gitignore.id)

        console.print(table)

    def save_gitignore_by_id(self, gitignore_id):
        gitignore_files = [
            gitignore
            for gitignore in self.gitignore_files
            if gitignore_id.lower() == gitignore.id.lower()
        ]

        if len(gitignore_files) == 0:
            console = Console()
            console.print("[red]Gitignore not found[red]")
        else:
            gitignore_files[0].load()
            gitignore_files[0].save()


class Gitignore:
    def __init__(self, path):
        self.path = path
        self.directory, self.file_name = os.path.split(self.path)
        self.id = self.file_name.replace(".gitignore", "")
        self.text = ""

    def load(self):
        with open(self.path, "r") as file:
            self.text = file.read()

    def print(self):
        console = Console()
        console.print(
            "[green]Name:[green]\t[magenta bold]{}[magenta bold]".format(self.file_name)
        )
        console.print(
            "[green]Id:[green]\t[magenta bold]{}[magenta bold]".format(self.id)
        )
        console.rule()
        console.print(self.text)

    def save(self):
        with open(".gitignore", "w") as file:
            file.write(self.text)

    def __eq__(self, o):
        return self.id == o.id


class TemplatesRepository:
    def __init__(self):
        self.path = os.path.expanduser("~/.gitignoregh/gitignore")
        self.remote = "https://github.com/github/gitignore.git"

    def init(self):
        if os.path.isdir(self.path):
            repo = git.Repo(self.path)
            repo.remotes.origin.pull()
        else:
            git.Repo.clone_from(self.remote, self.path)
