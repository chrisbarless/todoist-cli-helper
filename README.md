# Todoist CLI

A command-line interface for automating Todoist tasks.

## Features

- List all tasks
- Add new tasks
- Open links in inbox tasks and clear them
- Clear due dates from overdue and today's non-recurring tasks

## Installation

1. Clone the repository
2. Install dependencies:

```

pip install -e .

```

3. Set your Todoist API token as an environment variable:

```

export TODOIST_API_TOKEN=your_api_token_here

```

## Usage

Run the CLI with:

```

python -m todoist_cli.cli [COMMAND]

```

Available commands:

- `list-tasks`: List all tasks
- `add-task`: Add a new task
- `open-inbox-links`: Open web links in inbox tasks and clear them
- `clear-today`: Remove due dates from overdue and today's non-recurring tasks

For more information on each command, use:

```

python -m todoist_cli.cli [COMMAND] --help

```

## License

This project is open-source and available under the MIT License.
