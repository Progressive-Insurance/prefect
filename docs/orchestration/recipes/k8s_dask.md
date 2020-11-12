<<<<<<< HEAD
# Static Dask Cluster on Kubernetes

This recipe is for a flow deployed to Kubernetes using a shared static
[Dask](https://dask.org) cluster. This Dask cluster runs on the same Kubernetes
cluster that the flow runs on.

Note that for most deployments we recommend using temporary per-flow clusters,
rather than a single long-running Dask cluster (although there are use cases
for both). See the [Dask
Executor](/orchestration/flow_config/executors#daskexecutor) documentation for
more information.

[[toc]]

## Kubernetes Manifests

Below we provide an example [Kubernetes
Manifest](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)
for deploying a static Dask cluster on Kubernetes. It starts a cluster with 2
workers, with the scheduler listening at `tcp://dask-scheduler:8786`.

For a production deployment you may be interested in using something like the
[Dask Helm Chart](https://docs.dask.org/en/latest/setup/kubernetes-helm.html#helm-install-dask-for-a-single-user)
instead - the manifests below are only provided as an example.
=======
# Dask Cluster on Kubernetes <Badge text="Cloud"/>

This recipe is for a flow deployed to Kubernetes using a static Dask cluster. This Dask cluster lives on the same Kubernetes cluster that the flow runs on.

[[toc]]

### Dask YAML

`dask_scheduler.yaml` is the deployment that runs the Dask scheduler.
>>>>>>> prefect clone

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dask-scheduler
  labels:
    app: dask-scheduler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dask-scheduler
  template:
    metadata:
      labels:
        app: dask-scheduler
    spec:
      containers:
        - name: dask-scheduler
          image: prefecthq/prefect:latest
          args:
            - dask-scheduler
            - --port
            - "8786"
<<<<<<< HEAD
          ports:
            - containerPort: 8786
---
apiVersion: v1
kind: Service
metadata:
  name: dask-scheduler
spec:
  selector:
    app: dask-scheduler
  ports:
    - port: 8786
      targetPort: 8786
---
=======
          env:
            - name: DASK_DISTRIBUTED__SCHEDULER__WORK_STEALING
              value: "False"
          ports:
            - containerPort: 8786
          resources: {}
```

`dask_worker.yaml` is the deployment that runs the Dask workers. Notice that setting `replicas: 2` means that there will be two workers in this Dask cluster.

```yaml
>>>>>>> prefect clone
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dask-worker
  labels:
    app: dask-worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dask-worker
  template:
    metadata:
      labels:
        app: dask-worker
    spec:
      containers:
<<<<<<< HEAD
        - name: dask-worker
          image: prefecthq/prefect:latest
=======
        - image: prefecthq/prefect:latest
>>>>>>> prefect clone
          args:
            [
              dask-worker,
              dask-scheduler:8786,
              --no-bokeh,
              --nthreads,
<<<<<<< HEAD
              "4"
            ]
```

:::warning Required dependencies
When running Dask on Kubernetes you must ensure your image contains the
dependencies your flow needs to execute, either by using the flow's Docker
storage as the image for Dask or by building a custom image with all the
required dependencies. The manifest above uses the `prefecthq/prefect:latest`
image for both the Dask scheduler & worker pods, since our flow has no external
dependencies beyond Prefect.
:::

## Flow Source

Here we create a flow configured with:

- A [KubernetesRun](/orchestration/flow_config/run_configs.md#kubernetesrun)
  run config, specifying that it should be run by a Kubernetes Agent.
- A [DaskExecutor](/orchestration/flow_config/executors.md#daskexecutor)
  configured to connect to the static Dask cluster created above.
- A [Docker](/orchestration/flow_config/storage.md#docker) storage, specifying
  that the flow source should be built and stored in a new Docker image.

```python
from prefect import task, Flow
from prefect.executors import DaskExecutor
from prefect.run_configs import KubernetesRun
from prefect.storage import Docker
=======
              "1",
              --nprocs,
              "2",
            ]
          name: dask-worker
          env:
            - name: DASK_DISTRIBUTED__SCHEDULER__BLOCKED_HANDLERS
              value: "['feed', 'run_function']"
            - name: DASK_DISTRIBUTED__SCHEDULER__WORK_STEALING
              value: "False"
          resources: {}
```

`dask_service.yaml` is the service that makes the Dask scheduler accessible over `dask-scheduler:8786`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: dask-scheduler
spec:
  selector:
    app: dask-scheduler
  ports:
    - port: 8786
      targetPort: 8786
```

:::warning Dependencies
One thing to note in this recipe is the fact that the Dask scheduler and worker pods use the base `prefecthq/prefect:latest` image; this is because our flow has no external dependencies beyond Prefect. When running Dask on Kubernetes you should ensure your image contains the dependencies your flow needs to execute, either by using the flow's Docker storage as the image for Dask or by building a custom image with all the required dependencies.
:::

### Flow Source

`dask_flow.py` is a flow which uses the
[LocalEnvironment](/orchestration/execution/local_environment.html) with a
[DaskExecutor](/api/latest/engine/executors.html#daskexecutor) to execute a
flow on a static Dask cluster. The Dask scheduler address is the one that was
assigned from `dask_service.yaml`.

```python
from prefect import task, Flow
from prefect.engine.executors import DaskExecutor
from prefect.environments import LocalEnvironment
from prefect.environments.storage import Docker
>>>>>>> prefect clone


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


<<<<<<< HEAD
with Flow("Static Dask Cluster Example") as flow:
    value = get_value()
    output_value(value)

flow.run_config = KubernetesRun()
flow.executor = DaskExecutor("tcp://dask-scheduler:8786")
flow.storage = Docker(registry_url="gcr.io/dev/", image_name="dask-k8s-flow", image_tag="0.1.0")
=======
flow = Flow(
    "Static Dask Cluster Example",
    environment=LocalEnvironment(
        executor=DaskExecutor("tcp://dask-scheduler:8786"),
    ),
    storage=Docker(
        registry_url="gcr.io/dev/", image_name="dask-k8s-flow", image_tag="0.1.0"
    ),
)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)
>>>>>>> prefect clone
```
