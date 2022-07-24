**Note:** Run all commands from base repo dir

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
