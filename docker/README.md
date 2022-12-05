**Note:** Run all commands from base repo dir

Both configurations - in Kubernetes & in Docker Compose use PostgreSQL as a DB for Prefect.

## Run Fastflows with Prefect server on Kube cluster

### Build Fastflows Docker Image

```console

    docker build . -f ./docker/Dockerfile -t geobeyond/fastflows:latest

```

### Run Fastflows on Kube cluster

Steps to run:

1. **(For local env only)** Install minikube (will be used to create & manage local cluster): https://minikube.sigs.k8s.io/docs/start/

2. Install kubectl if you don't have it - https://kubernetes.io/docs/tasks/tools/

3. **(For local env only)** Create kubernetes cluster:

```console

    # for postgresql data & flows
    mkdir data

    minikube start

    # Important!!!
    # On MacOS to make Ingress work you should run minikube with hyperkit:

    minikube start --driver=hyperkit --mount --mount-string flows:/app/flows

```

4. **(For local env only)**

Enable Ingress & host resolving (full explanation here)

```console

    minikube addons enable ingress

```

Get minikube cluster ip

```console

    minikube ip

```

Add domains to /etc/hosts linked to minikube cluster ip.

Add this to /etc/hosts file:

```console

    your-mini-kube-ip fastflows.geo
    your-mini-kube-ip prefect.geo

    # for example (where 192.168.64.2 - minikube ip):
    # 192.168.64.2 fastflows.geo
    # 192.168.64.2 prefect.geo

```

5. Apply Kube manifests to the cluster

```console

    kubectl apply -f docker/kube-infra

```

5. Check pods statuses & wait until all pods will not be in status "Running"

```console

    kubectl get pods

```

Now you can access service by links:

http://fastflows.geo/ & http://prefect.geo/

### Tips

1.  **(For local env only)** If for some reason you need to delete cluster, use:

```console

    minikube delete

```

## Run Fastflows with Prefect Server in Docker-Compose

### 1. Create network to connect Prefect & minio server:

```console

    docker network create prefect-network

```

Note: if you use MacOS, you will need to add minio internal host 'nginx' to /etc/hosts file.

Like:

`nginx 127.0.0.1`

Address to connect Minio should be the same for command line (when you create deployment & apply) & for prefect agent (when it runs flow).

### 2. Up & Run minio cluster

```console

    docker-compose -f docker/minio.yaml up

```

To check that minio up & running go to http://127.0.0.1:9001/login

Default login & password for minio admin panel is 'minioadmin' & 'minioadmin'.

### 3. Create user to connect to minio from Prefect

Do it with UI http://127.0.0.1:9001/.

You should get "key" & "secret", something like this: "0xoznLEXV3JHiOKx" & "MmG3vfemCe5mpcxP66a1XvPnsIoXTlWs"

Set up them in `FASTFLOWS__PREFECT__STORAGE__SETTINGS__KEY` and `FASTFLOWS__PREFECT__STORAGE__SETTINGS__SECRET` in docker-compose.yml file

### 4. Up & Run Prefect & Fastflows in docker-compose

```console

    docker-compose --env-file docker/.env -f ./docker/docker-compose.yml up  --build

```

To enter Prefect UI:

```console
    # if you will try to use 0.0.0.0 you will not see any data because of CORS issues
    http://localhost:4200/flows

```

### Up & Run minio cluster

### In docker-compose

```console

    docker-compose -f docker/minio.yaml

```

To check that minio up & running go to http://127.0.0.1:9001/login

Default login & password for minio admin panel is 'minioadmin' & 'minioadmin'.

### Minio Prefect Block Configuration

```console
# bucket path with protocol
Basepath - s3://test-bucket

# settings for connection
Settings
    {
        "key": "0xoznLEXV3JHiOKx",
        "secret": "MmG3vfemCe5mpcxP66a1XvPnsIoXTlWs",
        "client_kwargs": {
            "endpoint_url": "http://nginx:9000"
        }
    }

```
