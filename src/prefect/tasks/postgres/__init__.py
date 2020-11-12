"""
This module contains a collection of tasks for interacting with Postgres databases via
the psycopg2 library.
"""

try:
<<<<<<< HEAD
    from prefect.tasks.postgres.postgres import (
        PostgresExecute,
        PostgresExecuteMany,
        PostgresFetch,
    )
=======
    from prefect.tasks.postgres.postgres import PostgresExecute, PostgresFetch
>>>>>>> prefect clone
except ImportError:
    raise ImportError(
        'Using `prefect.tasks.postgres` requires Prefect to be installed with the "postgres" extra.'
    )
