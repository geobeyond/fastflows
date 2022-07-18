Run all commands from base source dir

### Build Fastflows Docker Image

```console

    docker build . -f ./docker/Dockerfile -t geobeyond/fastflows:latest

```

### Run Fastflows on Kube cluster

Steps to run:

1. Create dir '/etc/data/postgresql' it will be used to store persistent PostgreSQL data

2. **(For local env only)** Install k3d.io (will be used as K8s local solution): https://k3d.io/v5.4.4/#installation

3. Install kubectl if you don't have it - https://kubernetes.io/docs/tasks/tools/

4. Create k3d cluster with an image registry, minio (for remote storage), the prefect agent and api:

```console

    make kubes

```

P.S: If you will see error like 'Error from server (NotFound): customresourcedefinitions.apiextensions.k8s.io "ingressroutes.traefik.containo.us" not found' it is okay - just wait.

4. (**For local run only**) Import fastflows image

To get possible run Fastflows in k3d locally you need to import image in cluster (by default k3d cannot find images from local env)

```console

    k3d images import fastflows -c fastflows-cluster

```

### Tips

1.  **(For local env only)** If for some reason you need to delete cluster, use:

```console

    k3d cluster delete fastflows

```

2. If you need to connect to PostgreSQL DB from localhose, first find host with

```console

    kubectl get svc

```

when use with information to connect wtih PgAdmin or psql

3. If you cannot access from you local terminal Kube cluster & if you run command, for example: `kubectl get svc` see the error like:
   'The connection to the server localhost:8080 was refused - did you specify the right host or port?'

Then in your terminal that you use define path to cluster config like this:

```console

    export CLUSTER_NAME=fastflows-cluster
    export KUBECONFIG=.k3d/kubeconfig-${CLUSTER_NAME}.yaml

```

4. To check pods status:

```console

    kubectl get pods

```
