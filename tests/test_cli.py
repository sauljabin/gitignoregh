import unittest
from unittest.mock import MagicMock, patch

from faker import Faker

from gitignoregh.cli import Cli

faker = Faker()


class TestCli(unittest.TestCase):
    def setUp(self):
        self.cli = Cli()
        self.cli.gitignoregh = MagicMock()

    @patch("gitignoregh.cli.click")
    def test_cli_call_gitignoregh_init(self, click_mock):
        self.cli.run(False, False, False, False, None)

        self.cli.gitignoregh.init.assert_called_once()

    def test_cli_print_all_gitignore_files(self):
        self.cli.run(False, False, True, False, None)

        self.cli.gitignoregh.print_all_gitignore_files.assert_called_once()

    def test_cli_print_gitignore_files_by_id(self):
        gitignore_id = faker.word()
        self.cli.run(False, True, False, False, gitignore_id)

        self.cli.gitignoregh.print_gitignore_files_by_id.assert_called_once_with(gitignore_id)

    def test_cli_print_gitignore_by_id(self):
        gitignore_id = faker.word()
        self.cli.run(True, False, False, False, gitignore_id)

        self.cli.gitignoregh.print_gitignore_by_id.assert_called_once_with(gitignore_id)

    def test_save_gitignore_by_id(self):
        gitignore_id = faker.word()
        self.cli.run(False, False, False, False, gitignore_id)

        self.cli.gitignoregh.save_gitignore_by_id.assert_called_once_with(gitignore_id)

    def test_reset_repository(self):
        self.cli.run(False, False, False, True, None)

        self.cli.gitignoregh.reset_repository.assert_called_once()
        self.cli.gitignoregh.init.assert_not_called()

    @patch("gitignoregh.cli.click")
    def test_cli_shows_help_when_gitignore_id_does_not_exists(self, click_mock):
        self.cli.run(False, False, False, False, None)

        self.cli.gitignoregh.save_gitignore_by_id.assert_not_called()
        click_mock.get_current_context.assert_called_once()
        click_mock.echo.assert_called_once()
