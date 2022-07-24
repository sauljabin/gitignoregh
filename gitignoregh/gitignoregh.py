import os
import re
import shutil

import git
from rich.columns import Columns
from rich.console import Console


class Gitignoregh:
    def __init__(self):
        self.repository = TemplatesRepository()
        self.gitignore_files = []

    def init(self):
        self.repository.init()
        self.load_gitignore_files()

    def load_gitignore_files(self):
        for dirpath, dirnames, filenames in os.walk(self.repository.path):
            filenames = [
                filename for filename in filenames if filename.endswith(".gitignore")
            ]
            filenames.sort()
            for gitignore_path in filenames:
                self.gitignore_files.append(
                    Gitignore(os.path.join(dirpath, gitignore_path))
                )

    def print_all_gitignore_files(self):
        self.print_gitignore_files(self.gitignore_files)

    def print_gitignore_by_id(self, gitignore_id_list):
        if len(gitignore_id_list) == 0:
            gitignore_files = []
        else:
            gitignore_files = [
                gitignore
                for gitignore in self.gitignore_files
                if gitignore_id_list[0].lower() == gitignore.id.lower()
            ]

        if len(gitignore_files) == 0:
            console = Console()
            console.print("[red]Gitignore not found[/]")
        else:
            gitignore_files[0].load()
            gitignore_files[0].print()

    def print_gitignore_files_by_id(self, gitignore_id_list):
        gitignore_files = [
            gitignore
            for gitignore in self.gitignore_files
            if re.match(
                ".*({}).*".format("|".join(gitignore_id_list)).lower(),
                gitignore.id.lower(),
            )
        ]

        if len(gitignore_files) == 0:
            console = Console()
            console.print("[red]Gitignore files not found[/]")
        else:
            self.print_gitignore_files(gitignore_files)

    def print_gitignore_files(self, gitignore_files):
        console = Console()
        columns = Columns(
            [
                "[purple]:arrow_forward:[/] {}".format(gitignore.id)
                for gitignore in gitignore_files
            ],
            equal=True,
            expand=False,
        )
        console.print(columns)

    def save_gitignore_by_id(self, gitignore_id_list):
        gitignore_files = [
            gitignore
            for gitignore in self.gitignore_files
            if gitignore.id.lower() in [id.lower() for id in gitignore_id_list]
        ]

        if len(gitignore_files) == 0:
            console = Console()
            console.print("[red]Gitignore not found[/]")
        else:
            with open(".gitignore", "w") as file:
                for gitignore_file in gitignore_files:
                    gitignore_file.load()
                    gitignore_file.save(file)

    def reset_repository(self):
        self.repository.remove()


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
        console.print("[green]Name:[/]\t[magenta bold]{}[/]".format(self.file_name))
        console.print("[green]Id:[/]\t[magenta bold]{}[/]".format(self.id))
        console.rule()
        console.print(self.text.replace("[", r"\["))

    def save(self, file_append=None):
        if file_append:
            file_append.write(self.full_text())
            return

        with open(".gitignore", "w") as file:
            file.write(self.full_text())

    def full_text(self):
        return "# >>> {}\n{}\n\n".format(self.id, self.text.strip())

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

    def remove(self):
        shutil.rmtree(self.path)
