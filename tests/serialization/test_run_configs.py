import pytest

<<<<<<< HEAD
from prefect.run_configs import KubernetesRun, LocalRun, DockerRun, ECSRun, UniversalRun
from prefect.serialization.run_config import RunConfigSchema, RunConfigSchemaBase


def test_serialized_run_config_sorts_labels():
    assert RunConfigSchemaBase().dump({"labels": ["b", "c", "a"]})["labels"] == [
        "a",
        "b",
        "c",
    ]


@pytest.mark.parametrize("config", [UniversalRun(), UniversalRun(labels=["a", "b"])])
def test_serialize_universal_run(config):
    msg = RunConfigSchema().dump(config)
    config2 = RunConfigSchema().load(msg)
    assert sorted(config.labels) == sorted(config2.labels)
=======
from prefect.run_configs import KubernetesRun, LocalRun, DockerRun, ECSRun
from prefect.serialization.run_config import RunConfigSchema
>>>>>>> prefect clone


@pytest.mark.parametrize(
    "config",
    [
        KubernetesRun(),
        KubernetesRun(
            job_template_path="s3://bucket/test.yaml",
            image="myimage",
            env={"test": "foo"},
            cpu_limit=2,
            cpu_request="500m",
            memory_limit="4G",
            memory_request="2G",
<<<<<<< HEAD
            service_account_name="my-account",
            image_pull_secrets=["secret-1", "secret-2"],
=======
>>>>>>> prefect clone
            labels=["a", "b"],
        ),
        KubernetesRun(
            job_template={
                "apiVersion": "batch/v1",
                "kind": "Job",
                "metadata": {"labels": {"example": "foo"}},
            }
        ),
    ],
)
def test_serialize_kubernetes_run(config):
    msg = RunConfigSchema().dump(config)
    config2 = RunConfigSchema().load(msg)
    assert sorted(config.labels) == sorted(config2.labels)
    fields = [
        "job_template",
        "job_template_path",
        "image",
        "env",
        "cpu_limit",
        "cpu_request",
        "memory_limit",
        "memory_request",
<<<<<<< HEAD
        "service_account_name",
        "image_pull_secrets",
=======
>>>>>>> prefect clone
    ]
    for field in fields:
        assert getattr(config, field) == getattr(config2, field)


@pytest.mark.parametrize(
    "config",
    [
        LocalRun(),
        LocalRun(
            env={"test": "foo"},
            working_dir="/path/to/dir",
            labels=["a", "b"],
        ),
    ],
)
def test_serialize_local_run(config):
    msg = RunConfigSchema().dump(config)
    config2 = RunConfigSchema().load(msg)
    assert sorted(config.labels) == sorted(config2.labels)
    fields = ["env", "working_dir"]
    for field in fields:
        assert getattr(config, field) == getattr(config2, field)


@pytest.mark.parametrize(
    "config",
    [
        DockerRun(),
        DockerRun(
            env={"test": "foo"},
            image="testing",
            labels=["a", "b"],
        ),
    ],
)
def test_serialize_docker_run(config):
    msg = RunConfigSchema().dump(config)
    config2 = RunConfigSchema().load(msg)
    assert sorted(config.labels) == sorted(config2.labels)
    fields = ["env", "image"]
    for field in fields:
        assert getattr(config, field) == getattr(config2, field)


@pytest.mark.parametrize(
    "config",
    [
        ECSRun(),
        ECSRun(
            task_definition_path="s3://bucket/test.yaml",
            image="myimage",
            env={"test": "foo"},
            cpu="1 vcpu",
            memory="1 GB",
            task_role_arn="my-task-role",
<<<<<<< HEAD
            execution_role_arn="execution-role",
=======
>>>>>>> prefect clone
            run_task_kwargs={"overrides": {"taskRoleArn": "example"}},
            labels=["a", "b"],
        ),
        ECSRun(
            task_definition={
                "containerDefinitions": [
                    {
                        "name": "flow",
                        "environment": [{"name": "TEST", "value": "VALUE"}],
                    }
                ]
            }
        ),
<<<<<<< HEAD
        ECSRun(task_definition_arn="my-task-definition"),
=======
>>>>>>> prefect clone
    ],
)
def test_serialize_ecs_run(config):
    msg = RunConfigSchema().dump(config)
    config2 = RunConfigSchema().load(msg)
    assert sorted(config.labels) == sorted(config2.labels)
    fields = [
        "task_definition",
        "task_definition_path",
<<<<<<< HEAD
        "task_definition_arn",
=======
>>>>>>> prefect clone
        "image",
        "env",
        "cpu",
        "memory",
        "task_role_arn",
<<<<<<< HEAD
        "execution_role_arn",
=======
>>>>>>> prefect clone
        "run_task_kwargs",
    ]
    for field in fields:
        assert getattr(config, field) == getattr(config2, field)
