<<<<<<< HEAD
import warnings
from typing import Any

from prefect.executors import LocalExecutor as _LocalExecutor


class LocalExecutor(_LocalExecutor):
    def __new__(cls, *args: Any, **kwargs: Any) -> "LocalExecutor":
        warnings.warn(
            "prefect.engine.executors.LocalExecutor has been moved to "
            "`prefect.executors.LocalExecutor`, please update your imports",
            stacklevel=2,
        )
        return super().__new__(cls)
=======
from typing import Any, Callable

from prefect.engine.executors.base import Executor


class LocalExecutor(Executor):
    """
    An executor that runs all functions synchronously and immediately in
    the main thread.  To be used mainly for debugging purposes.
    """

    def submit(
        self, fn: Callable, *args: Any, extra_context: dict = None, **kwargs: Any
    ) -> Any:
        """
        Submit a function to the executor for execution. Returns the result of the computation.

        Args:
            - fn (Callable): function that is being submitted for execution
            - *args (Any): arguments to be passed to `fn`
            - extra_context (dict, optional): an optional dictionary with extra information
                about the submitted task
            - **kwargs (Any): keyword arguments to be passed to `fn`

        Returns:
            - Any: the result of `fn(*args, **kwargs)`
        """
        return fn(*args, **kwargs)

    def wait(self, futures: Any) -> Any:
        """
        Returns the results of the provided futures.

        Args:
            - futures (Any): objects to wait on

        Returns:
            - Any: whatever `futures` were provided
        """
        return futures
>>>>>>> prefect clone
