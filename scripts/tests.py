from scripts import CommandProcessor


def main():
    init_commands = {
        "tests": "poetry run python -m unittest -v",
    }
    command_processor = CommandProcessor(init_commands)
    command_processor.run()


if __name__ == "__main__":
    main()
