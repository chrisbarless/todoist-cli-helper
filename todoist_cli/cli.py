import os
import re
import subprocess
from datetime import datetime

import click
from todoist_api_python.api import TodoistAPI

# Initialize the Todoist API client
api = TodoistAPI(os.environ.get("TODOIST_API_TOKEN"))
inbox_id = os.environ.get("TODOIST_INBOX_ID")


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
def open_inbox_links():
    """Open links in the inbox and clear their tasks"""

    try:
        tasks = api.get_tasks(project_id=inbox_id)
        for task in tasks:
            # Check if the task content contains a URL
            url_match = re.search(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                task.content,
            )
            if url_match:
                url = url_match.group(0)
                print(f"Opening URL: {url}")
                subprocess.run(["open", url], check=True)

                # Delete the task
                api.delete_task(task_id=task.id)
                print(f"Deleted task: {task.content}")
            else:
                print(f"No URL found in task: {task.content}")
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


@cli.command()
def clear_today():
    """Remove due dates from overdue and today's non-recurring tasks"""
    try:
        # Get overdue and today's tasks
        tasks = api.get_tasks(filter="overdue & !recurring")

        for task in tasks:
            # Remove the due date
            api.update_task(task_id=task.id, due_string="no due date")
            print(f"Removed due date from task: {task.content}")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"Completed removing due dates from overdue and today's non-recurring tasks at {current_time}."
        )
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    cli()
