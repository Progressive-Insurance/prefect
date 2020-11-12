import uuid
import warnings
<<<<<<< HEAD
from typing import Tuple, Union
import io
from time import sleep
=======
from typing import Union
import io
>>>>>>> prefect clone

from google.cloud.exceptions import NotFound

from prefect import context
from prefect.client import Secret
from prefect.core import Task
from prefect.utilities.gcp import get_storage_client
from prefect.utilities.tasks import defaults_from_attrs

<<<<<<< HEAD
from google.cloud import storage
from prefect.engine.signals import FAIL

=======
>>>>>>> prefect clone

class GCSBaseTask(Task):
    def __init__(
        self,
        bucket: str = None,
        blob: str = None,
        project: str = None,
        create_bucket: bool = False,
<<<<<<< HEAD
        chunk_size: int = 104857600,  # 1024 * 1024 B * 100 = 100 MB
        encryption_key_secret: str = None,
        request_timeout: Union[float, Tuple[float, float]] = 60,
        **kwargs,
=======
        encryption_key_secret: str = None,
        **kwargs
>>>>>>> prefect clone
    ):
        self.bucket = bucket
        self.blob = blob
        self.project = project
        self.create_bucket = create_bucket
        if encryption_key_secret is not None:
            warnings.warn(
                "The `encryption_key_secret` argument is deprecated. Use a `Secret` task "
                "to pass the key value at runtime instead.",
                UserWarning,
                stacklevel=2,
            )
<<<<<<< HEAD
        self.chunk_size = chunk_size
        self.encryption_key_secret = encryption_key_secret
        self.request_timeout = request_timeout
=======
        self.encryption_key_secret = encryption_key_secret
>>>>>>> prefect clone
        super().__init__(**kwargs)

    def _retrieve_bucket(self, client, bucket: str, create_bucket: bool):
        "Retrieves a bucket based on user settings"
        try:
            bucket = client.get_bucket(bucket)
        except NotFound as exc:
            if create_bucket is True:
                self.logger.debug("Bucket {} not found; creating...".format(bucket))
                bucket = client.create_bucket(bucket)
            else:
                raise exc
        return bucket

    def _get_blob(
        self,
        bucket: str,
        blob: str,
<<<<<<< HEAD
        chunk_size: int = None,
=======
>>>>>>> prefect clone
        encryption_key: str = None,
        encryption_key_secret: str = None,
    ):
        "Retrieves blob based on user settings."
        if blob is None:
            blob = "prefect-" + context.get("task_run_id", "no-id-" + str(uuid.uuid4()))

<<<<<<< HEAD
        if chunk_size is None:
            chunk_size = self.chunk_size

=======
>>>>>>> prefect clone
        # pull encryption_key if requested
        if encryption_key_secret is not None:
            warnings.warn(
                "The `encryption_key_secret` argument is deprecated. Use a `Secret` task "
                "to pass the credentials value at runtime instead.",
                UserWarning,
                stacklevel=2,
            )
            encryption_key = Secret(encryption_key_secret).get()

<<<<<<< HEAD
        return bucket.blob(blob, encryption_key=encryption_key, chunk_size=chunk_size)
=======
        return bucket.blob(blob, encryption_key=encryption_key)
>>>>>>> prefect clone


class GCSDownload(GCSBaseTask):
    """
    Task template for downloading data from Google Cloud Storage as a string.

    Args:
        - bucket (str): default bucket name to download from
        - blob (str, optional): default blob name to download.
        - project (str, optional): default Google Cloud project to work within.
            If not provided, will be inferred from your Google Cloud credentials
<<<<<<< HEAD
        - chunk_size (int, optional): The size of a chunk of data whenever iterating (in bytes).
            This must be a multiple of 256 KB per the API specification.
        - encryption_key_secret (str, optional, DEPRECATED): the name of the Prefect Secret
            storing an optional `encryption_key` to be used when downloading the Blob
        - request_timeout (Union[float, Tuple[float, float]], optional): default number of
            seconds the transport should wait for the server response.
            Can also be passed as a tuple (connect_timeout, read_timeout).
=======
        - encryption_key_secret (str, optional, DEPRECATED): the name of the Prefect Secret
            storing an optional `encryption_key` to be used when downloading the Blob
>>>>>>> prefect clone
        - **kwargs (dict, optional): additional keyword arguments to pass to the Task constructor

    Note that the design of this task allows you to initialize a _template_ with default
    settings.  Each inidividual occurence of the task in a Flow can overwrite any of these
    default settings for custom use (for example, if you want to pull different credentials for
    a given Task, or specify the Blob name at runtime).
    """

    def __init__(
        self,
        bucket: str,
        blob: str = None,
        project: str = None,
<<<<<<< HEAD
        chunk_size: int = None,
        encryption_key_secret: str = None,
        request_timeout: Union[float, Tuple[float, float]] = 60,
        **kwargs,
=======
        encryption_key_secret: str = None,
        **kwargs
>>>>>>> prefect clone
    ):
        super().__init__(
            bucket=bucket,
            blob=blob,
            project=project,
<<<<<<< HEAD
            chunk_size=chunk_size,
            encryption_key_secret=encryption_key_secret,
            request_timeout=request_timeout,
            **kwargs,
        )

    @defaults_from_attrs(
        "blob", "bucket", "project", "encryption_key_secret", "request_timeout"
    )
=======
            encryption_key_secret=encryption_key_secret,
            **kwargs
        )

    @defaults_from_attrs("blob", "bucket", "project", "encryption_key_secret")
>>>>>>> prefect clone
    def run(
        self,
        bucket: str = None,
        blob: str = None,
        project: str = None,
<<<<<<< HEAD
        chunk_size: int = None,
        credentials: dict = None,
        encryption_key: str = None,
        encryption_key_secret: str = None,
        request_timeout: Union[float, Tuple[float, float]] = 60,
=======
        credentials: dict = None,
        encryption_key: str = None,
        encryption_key_secret: str = None,
>>>>>>> prefect clone
    ) -> str:
        """
        Run method for this Task.  Invoked by _calling_ this Task after initialization
        within a Flow context.

        Note that some arguments are required for the task to run, and must be provided
        _either_ at initialization _or_ as arguments.

        Args:
            - bucket (str, optional): the bucket name to upload to
            - blob (str, optional): blob name to download from
            - project (str, optional): Google Cloud project to work within. If not provided
                here or at initialization, will be inferred from your Google Cloud credentials
<<<<<<< HEAD
            - chunk_size (int, optional): The size of a chunk of data whenever iterating (in bytes).
                This must be a multiple of 256 KB per the API specification.
=======
>>>>>>> prefect clone
            - credentials (dict, optional): a JSON document containing Google Cloud
                credentials.  You should provide these at runtime with an upstream Secret task.
                If not provided, Prefect will first check `context` for `GCP_CREDENTIALS` and
                lastly will use default Google client logic.
            - encryption_key (str, optional): an encryption key
            - encryption_key_secret (str, optional, DEPRECATED): the name of the Prefect Secret
                storing an optional `encryption_key` to be used when uploading the Blob
<<<<<<< HEAD
            - request_timeout (Union[float, Tuple[float, float]], optional): the number of
                seconds the transport should wait for the server response.
                Can also be passed as a tuple (connect_timeout, read_timeout).
=======
>>>>>>> prefect clone

        Returns:
            - str: the data from the blob, as a string

        Raises:
            - google.cloud.exception.NotFound: if `create_bucket=False` and the bucket
                name is not found
            - ValueError: if `blob` name hasn't been provided

        """
        # create client
        client = get_storage_client(project=project, credentials=credentials)

        # retrieve bucket
        bucket = self._retrieve_bucket(
            client=client, bucket=bucket, create_bucket=False
        )

        # identify blob name
<<<<<<< HEAD
        blob = self._get_blob(
            bucket,
            blob,
            chunk_size=chunk_size,
            encryption_key=encryption_key,
            encryption_key_secret=encryption_key_secret,
        )
        # Support GCS < 1.31
        return (
            blob.download_as_bytes(timeout=request_timeout)
            if hasattr(blob, "download_as_bytes")
            else blob.download_as_string(timeout=request_timeout)
        )
=======
        gcs_blob = self._get_blob(
            bucket,
            blob,
            encryption_key=encryption_key,
            encryption_key_secret=encryption_key_secret,
        )
        data = gcs_blob.download_as_string()
        return data
>>>>>>> prefect clone


class GCSUpload(GCSBaseTask):
    """
    Task template for uploading data to Google Cloud Storage.  Data can be a string or bytes.

    Args:
        - bucket (str): default bucket name to upload to
        - blob (str, optional): default blob name to upload to; otherwise a random string
            beginning with `prefect-` and containing the Task Run ID will be used
        - project (str, optional): default Google Cloud project to work within.
            If not provided, will be inferred from your Google Cloud credentials
<<<<<<< HEAD
        - chunk_size (int, optional): The size of a chunk of data whenever iterating (in bytes).
            This must be a multiple of 256 KB per the API specification.
=======
>>>>>>> prefect clone
        - create_bucket (bool, optional): boolean specifying whether to create the bucket if it
            does not exist, otherwise an Exception is raised. Defaults to `False`.
        - encryption_key_secret (str, optional, DEPRECATED): the name of the Prefect Secret
            storing an optional `encryption_key` to be used when uploading the Blob
<<<<<<< HEAD
        - request_timeout (Union[float, Tuple[float, float]], optional): default number of
            seconds the transport should wait for the server response.
            Can also be passed as a tuple (connect_timeout, read_timeout).
=======
>>>>>>> prefect clone
        - **kwargs (dict, optional): additional keyword arguments to pass to the Task constructor

    Note that the design of this task allows you to initialize a _template_ with default
    settings.  Each inidividual occurence of the task in a Flow can overwrite any of
    these default settings for custom use (for example, if you want to pull different
    credentials for a given Task, or specify the Blob name at runtime).
    """

    def __init__(
        self,
        bucket: str,
        blob: str = None,
        project: str = None,
<<<<<<< HEAD
        chunk_size: int = 104857600,  # 1024 * 1024 B * 100 = 100 MB
        create_bucket: bool = False,
        encryption_key_secret: str = None,
        request_timeout: Union[float, Tuple[float, float]] = 60,
        **kwargs,
=======
        create_bucket: bool = False,
        encryption_key_secret: str = None,
        **kwargs
>>>>>>> prefect clone
    ):
        super().__init__(
            bucket=bucket,
            blob=blob,
            project=project,
<<<<<<< HEAD
            chunk_size=chunk_size,
            create_bucket=create_bucket,
            encryption_key_secret=encryption_key_secret,
            request_timeout=request_timeout,
            **kwargs,
        )

    @defaults_from_attrs(
        "bucket",
        "blob",
        "project",
        "create_bucket",
        "encryption_key_secret",
        "request_timeout",
=======
            create_bucket=create_bucket,
            encryption_key_secret=encryption_key_secret,
            **kwargs
        )

    @defaults_from_attrs(
        "bucket", "blob", "project", "create_bucket", "encryption_key_secret"
>>>>>>> prefect clone
    )
    def run(
        self,
        data: Union[str, bytes],
        bucket: str = None,
        blob: str = None,
        project: str = None,
<<<<<<< HEAD
        chunk_size: int = None,
=======
>>>>>>> prefect clone
        credentials: dict = None,
        encryption_key: str = None,
        create_bucket: bool = False,
        encryption_key_secret: str = None,
        content_type: str = None,
        content_encoding: str = None,
<<<<<<< HEAD
        request_timeout: Union[float, Tuple[float, float]] = 60,
=======
>>>>>>> prefect clone
    ) -> str:
        """
        Run method for this Task.  Invoked by _calling_ this Task after initialization
        within a Flow context.

        Note that some arguments are required for the task to run, and must be
        provided _either_ at initialization _or_ as arguments.

        Args:
            - data (Union[str, bytes]): the data to upload; can be either string or bytes
            - bucket (str, optional): the bucket name to upload to
            - blob (str, optional): blob name to upload to
                a string beginning with `prefect-` and containing the Task Run ID will be used
            - project (str, optional): Google Cloud project to work within. Can be inferred
                from credentials if not provided.
<<<<<<< HEAD
            - chunk_size (int, optional): The size of a chunk of data whenever iterating (in bytes).
                This must be a multiple of 256 KB per the API specification.
=======
>>>>>>> prefect clone
            - credentials (dict, optional): a JSON document containing Google Cloud credentials.
                You should provide these at runtime with an upstream Secret task.  If not
                provided, Prefect will first check `context` for `GCP_CREDENTIALS` and lastly
                will use default Google client logic.
            - encryption_key (str, optional): an encryption key
            - create_bucket (bool, optional): boolean specifying whether to create the bucket
                if it does not exist, otherwise an Exception is raised. Defaults to `False`.
            - encryption_key_secret (str, optional, DEPRECATED): the name of the Prefect Secret
                storing an optional `encryption_key` to be used when uploading the Blob.
            - content_type (str, optional): HTTP ‘Content-Type’ header for this object.
            - content_encoding (str, optional): HTTP ‘Content-Encoding’ header for this object.
<<<<<<< HEAD
            - request_timeout (Union[float, Tuple[float, float]], optional): the number of
                seconds the transport should wait for the server response.
                Can also be passed as a tuple (connect_timeout, read_timeout).

        Raises:
            - TypeError: if data is neither string nor bytes.
=======

        Raises:
>>>>>>> prefect clone
            - google.cloud.exception.NotFound: if `create_bucket=False` and the bucket name is
                not found

        Returns:
            - str: the blob name that now stores the provided data
        """
        # create client
        client = get_storage_client(project=project, credentials=credentials)

        # retrieve bucket
        bucket = self._retrieve_bucket(
            client=client, bucket=bucket, create_bucket=create_bucket
        )

        # identify blob name
        gcs_blob = self._get_blob(
            bucket,
            blob,
<<<<<<< HEAD
            chunk_size=chunk_size,
=======
>>>>>>> prefect clone
            encryption_key=encryption_key,
            encryption_key_secret=encryption_key_secret,
        )

        # Upload
        if type(data) == str:
<<<<<<< HEAD
            gcs_blob.upload_from_string(data, timeout=request_timeout)
=======
            gcs_blob.upload_from_string(data)
>>>>>>> prefect clone
        elif type(data) == bytes:
            # Set content type and encoding if supplied.
            # This is likely only desirable if uploading gzip data:
            # https://cloud.google.com/storage/docs/metadata#content-encoding
            if content_type:
                gcs_blob.content_type = content_type
            if content_encoding:
                gcs_blob.content_encoding = content_encoding
<<<<<<< HEAD
            gcs_blob.upload_from_file(io.BytesIO(data), timeout=request_timeout)
        else:
            raise TypeError(f"data must be str or bytes: got {type(data)} instead")
=======
            gcs_blob.upload_from_file(io.BytesIO(data))
>>>>>>> prefect clone
        return gcs_blob.name


class GCSCopy(GCSBaseTask):
    """
    Task template for copying data from one Google Cloud Storage bucket to another, without
    downloading it locally.

    Note that some arguments are required for the task to run, and must be
    provided _either_ at initialization _or_ as arguments.

    Args:
        - source_bucket (str, optional): default source bucket name.
        - source_blob (str, optional): default source blob name.
        - dest_bucket (str, optional): default destination bucket name.
        - dest_blob (str, optional): default destination blob name.
        - project (str, optional): default Google Cloud project to work within.
            If not provided, will be inferred from your Google Cloud credentials
<<<<<<< HEAD
        - request_timeout (Union[float, Tuple[float, float]], optional): default number of
            seconds the transport should wait for the server response.
            Can also be passed as a tuple (connect_timeout, read_timeout).
=======
>>>>>>> prefect clone
        - **kwargs (dict, optional): additional keyword arguments to pass to the
            Task constructor

    Note that the design of this task allows you to initialize a _template_ with default
    settings.  Each inidividual occurence of the task in a Flow can overwrite any of these
    default settings for custom use (for example, if you want to pull different credentials for
    a given Task, or specify the Blob name at runtime).
    """

    def __init__(
        self,
        source_bucket: str = None,
        source_blob: str = None,
        dest_bucket: str = None,
        dest_blob: str = None,
        project: str = None,
<<<<<<< HEAD
        request_timeout: Union[float, Tuple[float, float]] = 60,
        **kwargs,
=======
        **kwargs
>>>>>>> prefect clone
    ):
        self.source_bucket = source_bucket
        self.source_blob = source_blob
        self.dest_bucket = dest_bucket
        self.dest_blob = dest_blob

<<<<<<< HEAD
        super().__init__(project=project, request_timeout=request_timeout, **kwargs)

    @defaults_from_attrs(
        "source_bucket",
        "source_blob",
        "dest_bucket",
        "dest_blob",
        "project",
        "request_timeout",
=======
        super().__init__(project=project, **kwargs)

    @defaults_from_attrs(
        "source_bucket", "source_blob", "dest_bucket", "dest_blob", "project"
>>>>>>> prefect clone
    )
    def run(
        self,
        source_bucket: str = None,
        source_blob: str = None,
        dest_bucket: str = None,
        dest_blob: str = None,
        project: str = None,
        credentials: dict = None,
<<<<<<< HEAD
        request_timeout: Union[float, Tuple[float, float]] = 60,
=======
>>>>>>> prefect clone
    ) -> str:
        """
        Run method for this Task. Invoked by _calling_ this Task after initialization
        within a Flow context.

        Note that some arguments are required for the task to run, and must be
        provided _either_ at initialization _or_ as arguments.

        Args:
            - source_bucket (str, optional): default source bucket name.
            - source_blob (str, optional): default source blob name.
            - dest_bucket (str, optional): default destination bucket name.
            - dest_blob (str, optional): default destination blob name.
            - project (str, optional): default Google Cloud project to work within.
                If not provided, will be inferred from your Google Cloud credentials
            - credentials (dict, optional): a JSON document containing Google Cloud credentials.
                You should provide these at runtime with an upstream Secret task.  If not
                provided, Prefect will first check `context` for `GCP_CREDENTIALS` and lastly
                will use default Google client logic.
<<<<<<< HEAD
            - request_timeout (Union[float, Tuple[float, float]], optional): the number of
                seconds the transport should wait for the server response.
                Can also be passed as a tuple (connect_timeout, read_timeout).
=======
>>>>>>> prefect clone

        Returns:
            - str: the name of the destination blob

        Raises:
            - ValueError: if `source_bucket`, `source_blob`, `dest_bucket`, or `dest_blob`
                are missing or point at the same object.

        """
        if None in [source_bucket, source_blob, dest_bucket, dest_blob]:
            raise ValueError("Missing source or destination")
        elif (source_bucket, source_blob) == (dest_bucket, dest_blob):
            raise ValueError("Source and destination are identical.")

        # create client
        client = get_storage_client(project=project, credentials=credentials)

        # get source bucket and blob
        source_bucket_obj = client.get_bucket(source_bucket)
        source_blob_obj = source_bucket_obj.blob(source_blob)
        # get dest bucket
        dest_bucket_obj = client.get_bucket(dest_bucket)
        # copy from source blob to dest bucket
        source_bucket_obj.copy_blob(
<<<<<<< HEAD
            blob=source_blob_obj,
            destination_bucket=dest_bucket_obj,
            new_name=dest_blob,
            timeout=request_timeout,
        )

        return dest_blob


class GCSBlobExists(GCSBaseTask):
    """
    Task template for checking a Google Cloud Storage bucket for a given object

    Args:
        - bucket_name (str, optional): the bucket to check
        - blob (str, optional): object for which to search within the bucket
        - project (str, optional): default Google Cloud project to work within.
            If not provided, will be inferred from your Google Cloud credentials
        - wait_seconds(int, optional): retry until file is found or until wait_seconds,
            whichever is first.  Defaults to 0
        - request_timeout (Union[float, Tuple[float, float]], optional): default number of
            seconds the transport should wait for the server response.
            Can also be passed as a tuple (connect_timeout, read_timeout).
        - fail_if_not_found (bool, optional):  Will raise Fail signal on task if
            blob is not found.  Defaults to True
        - **kwargs (dict, optional): additional keyword arguments to pass to the
            Task constructor

    Note that the design of this task allows you to initialize a _template_ with default
    settings.  Each inidividual occurence of the task in a Flow can overwrite any of these
    default settings for custom use (for example, if you want to pull different credentials for
    a given Task, or specify the Blob name at runtime).
    """

    def __init__(
        self,
        bucket_name: str = None,
        blob: str = None,
        project: str = None,
        wait_seconds: int = 0,
        fail_if_not_found: bool = True,
        request_timeout: Union[float, Tuple[float, float]] = 60,
        **kwargs,
    ):
        self.bucket_name = bucket_name
        self.blob = blob
        self.project = project
        self.wait_seconds = wait_seconds
        self.request_timeout = request_timeout
        self.fail_if_not_found = fail_if_not_found

        super().__init__(project=project, request_timeout=request_timeout, **kwargs)

    @defaults_from_attrs(
        "bucket_name",
        "blob",
        "project",
        "request_timeout",
        "wait_seconds",
        "fail_if_not_found",
    )
    def run(
        self,
        bucket_name: str = None,
        blob: str = None,
        project: str = None,
        wait_seconds: int = 0,
        fail_if_not_found: bool = True,
        credentials: dict = None,
        request_timeout: Union[float, Tuple[float, float]] = 60,
    ) -> str:
        """
        Run method for this Task. Invoked by _calling_ this Task after initialization
        within a Flow context.

        Note that some arguments are required for the task to run, and must be
        provided _either_ at initialization _or_ as arguments.

        Args:
            - bucket_name (str, optional): the bucket to check
            - blob (str, optional): object for which to search within the bucket
            - project (str, optional): default Google Cloud project to work within.
                If not provided, will be inferred from your Google Cloud credentials
            - wait_seconds(int, optional): retry until file is found or until wait_seconds,
                whichever is first.  Defaults to 0
            - fail_if_not_found (bool, optional):  Will raise Fail signal on task if
                blob is not found.  Defaults to True
            - credentials (dict, optional): a JSON document containing Google Cloud credentials.
                You should provide these at runtime with an upstream Secret task.  If not
                provided, Prefect will first check `context` for `GCP_CREDENTIALS` and lastly
                will use default Google client logic.
            - request_timeout (Union[float, Tuple[float, float]], optional): the number of
                seconds the transport should wait for the server response.
                Can also be passed as a tuple (connect_timeout, read_timeout).

        Returns:
            - bool: the object exists

        Raises:
            - ValueError: if `bucket_name` or `blob` are missing
            - FAIL: if object not found and fail_if_not_found is True

        """
        if None in [bucket_name, blob]:
            raise ValueError("Missing bucket_name or blob")

        # create client
        client = get_storage_client(project=project, credentials=credentials)

        bucket = client.bucket(bucket_name)
        blob_exists = None

        wait, n = 0, 1
        while wait <= wait_seconds and not blob_exists:
            sleep(n)
            wait += n
            n *= 2
            blob_exists = storage.Blob(bucket=bucket, name=blob).exists(client)
        if fail_if_not_found and not blob_exists:
            raise FAIL(message="Blob not found")
        return blob_exists
=======
            blob=source_blob_obj, destination_bucket=dest_bucket_obj, new_name=dest_blob
        )

        return dest_blob
>>>>>>> prefect clone
