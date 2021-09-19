import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

from faker import Faker

from gitignoregh.gitignoregh import Gitignore, Gitignoregh, TemplatesRepository

faker = Faker()
gitignore_text = """
##### github.com: Python.gitignore #####

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
"""


class TestGitignore(unittest.TestCase):
    def setUp(self):
        self.gitignore = Gitignore(faker.file_path(depth=5, extension="gitignore"))

    def test_gitignore_get_id_file_name_and_directory(self):
        head, tail = os.path.split(self.gitignore.path)

        self.assertEqual(tail.replace(".gitignore", ""), self.gitignore.id)
        self.assertEqual(tail, self.gitignore.file_name)
        self.assertEqual(head, self.gitignore.directory)

    @patch("builtins.open", new_callable=mock_open, read_data=gitignore_text)
    def test_gitignore_calls_open_file_read_only(self, open_mock):
        self.gitignore.load()

        open_mock.assert_called_with(self.gitignore.path, "r")

    @patch("builtins.open", new_callable=mock_open, read_data=gitignore_text)
    def test_gitignore_get_text_from_file(self, open_mock):
        self.gitignore.load()

        self.assertEqual(self.gitignore.text, gitignore_text)

    @patch("gitignoregh.gitignoregh.Console")
    def test_print_gitignore_text(self, console_class_mock):
        self.gitignore.text = faker.text()

        console_mock = MagicMock()
        console_class_mock.return_value = console_mock

        self.gitignore.print()

        console_mock.print.assert_called_with(self.gitignore.text)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_gitignore_text(self, console_class_mock):
        self.gitignore.text = faker.text()

        self.gitignore.save()

        console_class_mock.assert_called_once_with(".gitignore", "w")
        console_class_mock.return_value.write.assert_called_once_with(
            self.gitignore.text
        )


class TestGitignoregh(unittest.TestCase):
    def setUp(self):
        self.gitignoregh = Gitignoregh()
        self.gitignoregh.repository = MagicMock()

    def test_it_starts_templates_repository(self):
        self.gitignoregh.repository.path = faker.file_path()

        self.gitignoregh.init()

        self.gitignoregh.repository.init.assert_called_once()

    @patch("gitignoregh.gitignoregh.os.walk")
    def test_it_loads_all_template_list_when_init(self, walk_mock):
        walk_mock.return_value = [
            ("/foo", ["bar"], ["baz.gitignore"]),
            (
                "/foo/bar",
                [],
                ["spam.gitignore", "eggs.gitignore", "eggs.txt", faker.file_name()],
            ),
        ]

        self.gitignoregh.init()

        walk_mock.assert_called_once_with(self.gitignoregh.repository.path)
        self.assertListEqual(
            self.gitignoregh.gitignore_files,
            [
                Gitignore("/foo/baz.gitignore"),
                Gitignore("/foo/bar/eggs.gitignore"),
                Gitignore("/foo/bar/spam.gitignore"),
            ],
        )

    def test_print_gitignore_list_files_by_id(self):
        gitignore1 = Gitignore("/foo/bar/SPAM.gitignore")
        gitignore2 = Gitignore("/foo/bar/spam-2.0.gitignore")

        self.gitignoregh.gitignore_files = [
            Gitignore("/foo/bar/baz.gitignore"),
            Gitignore("/foo/bar/eggs.gitignore"),
            gitignore1,
            gitignore2,
        ]

        self.gitignoregh.print_gitignore_files = MagicMock()

        self.gitignoregh.print_gitignore_files_by_id("spam")

        self.gitignoregh.print_gitignore_files.assert_called_once_with(
            [gitignore1, gitignore2]
        )

    @patch("gitignoregh.gitignoregh.Console")
    def test_print_gitignore_files_not_found(self, console_class_mock):
        self.gitignoregh.gitignore_files = []

        console_mock = MagicMock()
        console_class_mock.return_value = console_mock

        self.gitignoregh.print_gitignore_files_by_id(faker.word())

        console_mock.print.assert_called_once_with(
            "[red]Gitignore files not found[red]"
        )

    def test_print_gitignore_by_id(self):
        gitignore1 = MagicMock()
        gitignore1.id = "spam"

        self.gitignoregh.gitignore_files = [
            Gitignore("/foo/bar/baz.gitignore"),
            Gitignore("/foo/bar/eggs.gitignore"),
            gitignore1,
            Gitignore("/foo/bar/spam-2.0.gitignore"),
        ]

        self.gitignoregh.print_gitignore_by_id("spam")

        gitignore1.load.assert_called_once()
        gitignore1.print.assert_called_once()

    def test_print_gitignore_by_id_uppercase(self):
        gitignore1 = MagicMock()
        gitignore1.id = "SPAM"

        self.gitignoregh.gitignore_files = [
            Gitignore("/foo/bar/baz.gitignore"),
            Gitignore("/foo/bar/eggs.gitignore"),
            gitignore1,
            Gitignore("/foo/bar/spam-2.0.gitignore"),
        ]

        self.gitignoregh.print_gitignore_by_id("spam")

        gitignore1.load.assert_called_once()
        gitignore1.print.assert_called_once()

    @patch("gitignoregh.gitignoregh.Console")
    def test_print_gitignore_not_found(self, console_class_mock):
        self.gitignoregh.gitignore_files = MagicMock()

        console_mock = MagicMock()
        console_class_mock.return_value = console_mock

        self.gitignoregh.print_gitignore_by_id(faker.word())

        console_mock.print.assert_called_once_with("[red]Gitignore not found[red]")

    def test_print_all_gitignore_files(self):
        self.gitignoregh.gitignore_files = MagicMock()
        self.gitignoregh.print_gitignore_files = MagicMock()

        self.gitignoregh.print_all_gitignore_files()

        self.gitignoregh.print_gitignore_files.assert_called_once_with(
            self.gitignoregh.gitignore_files
        )

    @patch("gitignoregh.gitignoregh.Console")
    @patch("gitignoregh.gitignoregh.Columns")
    def test_it_prints_table(self, columns_class_mock, console_class_mock):
        columns_mock = MagicMock()
        columns_class_mock.return_value = columns_mock

        console_mock = MagicMock()
        console_class_mock.return_value = console_mock

        gitignore1 = MagicMock()
        gitignore1.id = faker.word()
        gitignore2 = MagicMock()
        gitignore2.id = faker.word()
        gitignore_files = [gitignore1, gitignore2]

        self.gitignoregh.print_gitignore_files(gitignore_files)

        columns_class_mock.assert_called_with(
            [":arrow_forward: " + gitignore1.id, ":arrow_forward: " + gitignore2.id],
            equal=True,
            expand=False,
        )
        console_mock.print.assert_called_once_with(columns_mock)

    def test_save_gitignore_by_id(self):
        gitignore = MagicMock()

        self.gitignoregh.gitignore_files = [gitignore]

        self.gitignoregh.save_gitignore_by_id(gitignore.id)

        gitignore.save.assert_called_once()

    def test_save_gitignore_by_id_lowercase(self):
        gitignore = MagicMock()
        gitignore.id = "TEST"
        self.gitignoregh.gitignore_files = [gitignore]

        self.gitignoregh.save_gitignore_by_id(gitignore.id.lower())

        gitignore.save.assert_called_once()

    @patch("gitignoregh.gitignoregh.Console")
    def test_print_gitignore_not_found_when_save(self, console_class_mock):
        self.gitignoregh.gitignore_files = []

        console_mock = MagicMock()
        console_class_mock.return_value = console_mock

        self.gitignoregh.save_gitignore_by_id(faker.word())

        console_mock.print.assert_called_once_with("[red]Gitignore not found[red]")

    def test_remove_repository(self):
        self.gitignoregh.reset_repository()

        self.gitignoregh.repository.remove.assert_called_once()


class TestTemplateRepository(unittest.TestCase):
    def setUp(self):
        self.path = os.path.expanduser("~/.gitignoregh/gitignore")
        self.remote = "https://github.com/github/gitignore.git"
        self.templates_repository = TemplatesRepository()

    def test_repository_attributes(self):
        self.assertEqual(self.templates_repository.remote, self.remote)
        self.assertEqual(self.templates_repository.path, self.path)

    @patch("gitignoregh.gitignoregh.git")
    @patch("gitignoregh.gitignoregh.os")
    def test_repository_clone_if_does_not_exist(self, os_mock, git_mock):
        os_mock.path.isdir = MagicMock(return_value=False)

        self.templates_repository.init()

        git_mock.Repo.clone_from.assert_called_with(self.remote, self.path)

    @patch("gitignoregh.gitignoregh.git")
    @patch("gitignoregh.gitignoregh.os")
    def test_repository_does_not_clone_if_does_exist(self, os_mock, git_mock):
        os_mock.path.isdir = MagicMock(return_value=True)

        self.templates_repository.init()

        git_mock.Repo.clone_from.assert_not_called()

    @patch("gitignoregh.gitignoregh.git")
    @patch("gitignoregh.gitignoregh.os")
    def test_repository_does_pull_if_exists(self, os_mock, git_mock):
        os_mock.path.isdir = MagicMock(return_value=True)
        repo_mock = MagicMock()
        git_mock.Repo = MagicMock(return_value=repo_mock)

        self.templates_repository.init()

        repo_mock.remotes.origin.pull.assert_called()

    @patch("gitignoregh.gitignoregh.shutil")
    def test_remove_repository(self, shutil_mock):
        self.templates_repository.remove()

        shutil_mock.rmtree.assert_called_with(self.path)
