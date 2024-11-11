import os

import click
from todoist_api_python.api import TodoistAPI

# Initialize the Todoist API client
api = TodoistAPI(os.environ.get("TODOIST_API_TOKEN"))


@click.group()
def cli():
    """Todoist automation CLI"""
    pass


@cli.command()
def list_tasks():
    """List all tasks"""
    try:
        tasks = api.get_tasks()
        for task in tasks:
            print(
                f"Task: {task.content}, Project: {task.project_id}, Due: {task.due.date if task.due else 'No due date'}"
            )
    except Exception as error:
        print(f"Error: {error}")


@cli.command()
@click.option("--content", prompt="Task content", help="Content of the task")
@click.option("--project-id", prompt="Project ID", help="ID of the project")
@click.option("--due-date", prompt="Due date (YYYY-MM-DD)", help="Due date of the task")
def add_task(content, project_id, due_date):
    """Add a new task"""
    try:
        task = api.add_task(content=content, project_id=project_id, due_date=due_date)
        print(f"Task added: {task.content}")
    except Exception as error:
        print(f"Error: {error}")


@cli.command()
def complete_overdue_tasks():
    """Complete all overdue tasks"""
    try:
        tasks = api.get_tasks(filter="overdue")
        for task in tasks:
            api.close_task(task_id=task.id)
            print(f"Completed overdue task: {task.content}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    cli()
