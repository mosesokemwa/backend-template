import os
import sys
from pathlib import Path

from invoke import task


def taskfile_dir() -> str:
    """Returns the absolute path of the directory containing the current script."""
    directory = Path(__file__).parent.absolute()
    return str(directory)


@task()
def clean(ctx):
    """Remove python cache files"""
    ctx.run("find ./ -type d -name __pycache__ | xargs rm -rf", echo=True)


@task()
def show_urls(ctx):
    """Shows available URLs"""
    ctx.run("python manage.py show_urls", pty=True)


@task()
def migrations(ctx, app=None):
    """Shows available URLs"""
    ctx.run(f"python manage.py makemigrations {app or ''}", pty=True)


@task()
def migrate(ctx, app=None, database=None):
    """Shows available URLs"""
    if app is None:
        app = []
    args = f"--database {database}" if database else ""
    apps = " ".join(app)
    with ctx.cd(taskfile_dir()):
        ctx.run(f"python manage.py migrate {apps} {args}", pty=True, echo=True)


@task()
def run(
        ctx,
        plus=False,
        debugtoolbar=False,
        joblib_cache=False,
        ip="127.0.0.1",
        port=os.getenv("PORT", "8000"),
):
    """Runs development server"""
    if os.getenv("SENTRY_DSN", ""):
        print(
            "\nPlease consider unsetting SENTRY_DSN to preserve monthly transactions\n",
            file=sys.stderr,
        )

    env = {}
    if joblib_cache:
        env.update(ENABLE_JOBLIB_CACHE="1")
    if debugtoolbar:
        env.update(DEBUGTOOLBAR="1")

    command = "runserver_plus --nopin" if plus else "runserver"
    command = f"{command} {ip}:{port}"
    ctx.run(f"python manage.py {command}", echo=True, pty=True, env=env)


@task()
def test(ctx, coverage=False, verbose=False, failfast=False):
    """Run tests"""
    args = "--cov" if coverage else ""
    args = f"{args} --verbose" if verbose else args
    args = f"{args} --failfast" if failfast else args
    ctx.run(f"python manage.py test --pattern='tests_*.py' {args} ", echo=True, pty=True)


@task()
def freeze(ctx):
    """freeze installed packages in requirements.txt"""
    ctx.run("pip freeze > requirements.txt", echo=True)


@task()
def shell(ctx):
    """Runs Django shell"""
    ctx.run("python manage.py shell", echo=True, pty=True)


@task()
def shell_plus(ctx):
    """Runs Django shell_plus"""
    ctx.run("python manage.py shell_plus", echo=True, pty=True)


@task()
def startapp(ctx, app):
    """Runs Django startapp"""
    ctx.run(f"python manage.py startapp {app}", echo=True, pty=True)


@task()
def superuser(ctx):
    """Create superuser"""
    ctx.run("python manage.py createsuperuser", echo=True, pty=True)


@task()
def collectstatic(ctx):
    """Collect static files"""
    ctx.run("python manage.py collectstatic --noinput", echo=True, pty=True)
