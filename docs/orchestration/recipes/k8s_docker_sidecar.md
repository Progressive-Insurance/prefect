<<<<<<< HEAD
# Docker Sidecar on Kubernetes

This recipe is for a Flow deployed to Kubernetes, making use of a Docker
sidecar container to pull an image and run a container. This is an adaptation
of the [Docker Pipeline](../../core/examples/imperative_docker.md) example
where the `prefecthq/prefect:latest` image is pulled and a container is started
using that image to run another Flow inside that container.

The flow is run in a [Kubernetes
Job](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/)
using a custom job template. The job has two containers:

- The first will be filled in by the Kubernetes Agent to run the flow
- The second exposes a Docker daemon on `tcp://localhost:2375`

It uses a
[KubernetesRun](/orchestration/flow_config/run_configs.md#kubernetesrun) run
config to specify the custom job template. The Kubernetes Agent will use this
template when starting the flow run, instead of the default template set on the
agent.

The flow itself is composed of [Docker Tasks](/core/task_library/docker.html)
from Prefect's task library. It pulls an image, starts a container, then waits
for it to finish before pulling the container's logs.

```python
from prefect import Flow
from prefect.storage import Docker
from prefect.run_configs import KubernetesRun
from prefect.tasks.docker import (
    PullImage,
    CreateContainer,
    StartContainer,
    GetContainerLogs,
    WaitOnContainer,
)
from prefect.triggers import always_run


# The custom job spec to use for this flow run.
# This contains two containers:
# - The first will be filled in by the Kubernetes Agent to run the flow
# - The second exposes a Docker daemon on `tcp://localhost:2375`
job_template = """
=======
# Docker Sidecar on Kubernetes <Badge text="Cloud"/>

This recipe is for a Flow deployed to Kubernetes, making use of a Docker sidecar container to pull an image and run a container. This is an adaptation of the [Docker Pipeline](../../core/examples/imperative_docker.html) example where the `prefecthq/prefect:latest` image is pulled and a container is started using that image to run another Flow inside that container.

[[toc]]

### Job Spec YAML

`job_spec.yaml` is going to be the custom [Job](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/) YAML that will be passed into the Flow's [Kubernetes Job Environment](/orchestration/execution/k8s_job_environment.html). We have two containers for this Job: The Kubernetes Job Environment will use the first container to run the Flow; the second container will have an accessible Docker daemon over `tcp://localhost:2375`.

```yaml
>>>>>>> prefect clone
apiVersion: batch/v1
kind: Job
metadata:
  name: prefect-docker-job
<<<<<<< HEAD
spec:
  template:
=======
  labels:
    identifier: ''
spec:
  template:
    metadata:
      labels:
        identifier: ''
>>>>>>> prefect clone
    spec:
      restartPolicy: Never
      containers:
        - name: flow-container
<<<<<<< HEAD
=======
          image: ''
          command: []
          args: []
>>>>>>> prefect clone
          env:
            - name: DOCKER_HOST
              value: tcp://localhost:2375
        - name: dind-daemon
          image: docker:stable-dind
          env:
            - name: DOCKER_TLS_CERTDIR
              value: ""
          resources:
            requests:
              cpu: 20m
              memory: 512Mi
          securityContext:
            privileged: true
          volumeMounts:
            - name: docker-graph-store
              mountPath: /var/lib/docker
      volumes:
        - name: docker-graph-store
          emptyDir: {}
<<<<<<< HEAD
"""

# Initialize the tasks from the task library with all constant parameters
# Note that we pass the host of the Docker daemon to each task
image = PullImage(
    docker_server_url="tcp://localhost:2375",
    repository="prefecthq/prefect",
    tag="latest",
)
create_container = CreateContainer(
=======
```

### Flow Source

`k8s_docker.py` is a Flow which uses the Kubernetes Job Environment to create a custom Job that has access to the Docker sidecar in order to use the [Docker Tasks](/core/task_library/docker.html) found in the [Prefect Task Library](/core/task_library/).

```python
from prefect import Flow
from prefect.environments import KubernetesJobEnvironment
from prefect.environments.storage import Docker
from prefect.tasks.docker import (
    PullImage,
    CreateContainer,
    StartContainer,
    GetContainerLogs,
    WaitOnContainer,
)
from prefect.triggers import always_run


# Pass the host of the Docker daemon to each task
image = PullImage(
    docker_server_url="tcp://localhost:2375",
    repository="prefecthq/prefect",
    tag="latest",)
container = CreateContainer(
>>>>>>> prefect clone
    docker_server_url="tcp://localhost:2375",
    image_name="prefecthq/prefect:latest",
    command='''python -c "from prefect import Flow; f = Flow('empty'); f.run()"''',
)
<<<<<<< HEAD
start_container = StartContainer(docker_server_url="tcp://localhost:2375")
wait_on_container = WaitOnContainer(docker_server_url="tcp://localhost:2375")
# We pass `trigger=always_run` here so the logs will always be retrieved, even
# if upstream tasks fail
get_logs = GetContainerLogs(
    docker_server_url="tcp://localhost:2375", trigger=always_run
)

with Flow("Docker sidecar example") as flow:
    # Create and start the docker container
    container_id = create_container(image)
    started = start_container(container_id=container_id)
    # Once the docker container has started, wait until it's completed and get the status
    status_code = wait_on_container(container_id=container_id, upstream_tasks=[started])
    # Once the status code has been retrieved, retrieve the logs
    logs = get_logs(container_id=container_id, upstream_tasks=[status_code])

# Configure the flow to use the custom job template
flow.run_config = KubernetesRun(job_template=job_template)
flow.storage = Docker(
    registry_url="gcr.io/dev/", image_name="docker-on-k8s-flow", image_tag="0.1.0"
)
=======
start = StartContainer(docker_server_url="tcp://localhost:2375",)
logs = GetContainerLogs(docker_server_url="tcp://localhost:2375", trigger=always_run)
status_code = WaitOnContainer(docker_server_url="tcp://localhost:2375",)

flow = Flow(
    "Run a Prefect Flow in Docker",
    environment=KubernetesJobEnvironment(job_spec_file="job_spec.yaml"),
    storage=Docker(
        registry_url="gcr.io/dev/", image_name="docker-on-k8s-flow", image_tag="0.1.0"
    ),
)

# set task dependencies using imperative API
container.set_upstream(image, flow=flow)
start.set_upstream(container, flow=flow, key="container_id")
logs.set_upstream(container, flow=flow, key="container_id")
status_code.set_upstream(container, flow=flow, key="container_id")

status_code.set_upstream(start, flow=flow)
logs.set_upstream(status_code, flow=flow)
>>>>>>> prefect clone
```
