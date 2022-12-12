## Run FastFlow server

FastFlows is a FastAPI server & command line tool to communicate with Prefect 2.0 as a Workflow manager to deploy, run,
track flows and more.

To start work with FastFlows you should define at least 2 environment variables:

```console

    # Prefect API Server address
    PREFECT__URI=http://localhost:4200

    # Path to folder with flows
    FLOWS_HOME=flows

```

If you want to define variables with env prefix, for example, like `LOCAL__PREFECT__URI` or `DEV__PREFECT__URI` you
can use environment variable `ENV_NAME`.

If Fastflows will see `ENV_NAME` variable in environment - it will search for variables with prefix defined in
this `ENV_NAME`, for example:

if `ENV_NAME = 'LOCAL__'`

Fastflows will read variables like `LOCAL__PREFECT__URI` and `LOCAL__FLOWS_HOME`,

if `ENV_NAME = 'DEV__'`, then fastflows will expect variables like `DEV__PREFECT__URI` and `DEV__FLOWS_HOME`

### How to run FastFlows with Prefect cluster

#### with Kubernetes

- [Kube instructions](docker/README.md)
- [Kubernetes configuration](docker/kube-infra/)

#### with Docker-Compose

- [Docker-Compose readme](docker/README.md)
- [Docker-compose YAML](docker/docker-compose.yml)

### Run cli

```console

    fastflows --help

```

### Flows Deployment

#### Auto deployment

Deployment of Flows can be done by FastFlows automatically: if there is a new flow or changes in `FLOWS_HOME`
directory - FastFlows creates a new deployment. To disable auto deployment set env variable to `false`

```console

    AUTO_DEPLOYMENT = false

```
