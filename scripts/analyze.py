from scripts import CommandProcessor


def main():
    init_commands = {
        "black": "poetry run black --check .",
        "ruff": "poetry run ruff check .",
    }
    command_processor = CommandProcessor(init_commands)
    command_processor.run()


if __name__ == "__main__":
    main()
