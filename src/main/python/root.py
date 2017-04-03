import os


def path():
    """
    Returns path to root of the project
    """
    return os.path.abspath(
        os.environ.get('JOB_HOME', os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)))


def resources():
    """
    Returns absolute path to resources directory
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "resources"))
