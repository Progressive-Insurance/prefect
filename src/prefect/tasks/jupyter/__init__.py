"""
A collection of tasks for running Jupyter notebooks.
"""
try:
    from prefect.tasks.jupyter.jupyter import ExecuteNotebook
<<<<<<< HEAD
except ImportError as import_error:
    raise ImportError(
        'Using `prefect.tasks.jupyter` requires Prefect to be installed with the "jupyter" extra.'
    ) from import_error
=======
except ImportError:
    raise ImportError(
        'Using `prefect.tasks.jupyter` requires Prefect to be installed with the "jupyter" extra.'
    )
>>>>>>> prefect clone
