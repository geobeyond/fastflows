
export CLUSTER_NAME=fastflows-cluster
export KUBECONFIG=.k3d/kubeconfig-${CLUSTER_NAME}.yaml

## create cluster and install minio and prefect
kubes: cluster kubes-prefect

## create k3s cluster
cluster:
	k3d cluster create ${CLUSTER_NAME} --registry-create ${CLUSTER_NAME}-registry:0.0.0.0:5550 \
		-v "data:/data" -p 4200:80@loadbalancer -p 9090:9090@loadbalancer -p 9000:9000@loadbalancer -p 9001:9001@loadbalancer \
		--k3s-arg '--kube-apiserver-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kube-scheduler-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kubelet-arg=feature-gates=EphemeralContainers=true@agent:*' \
		--wait
	@echo "Probing until traefik CRDs are created (~60 secs)..." && export KUBECONFIG=$$(k3d kubeconfig write ${CLUSTER_NAME}) && \
		while : ; do kubectl get crd ingressroutes.traefik.containo.us > /dev/null && break; sleep 10; done
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write ${CLUSTER_NAME})"

## install prefect api and agent into kubes cluster
kubes-prefect:
	kubectl apply -f docker/kube-infra/postgres.yaml
	kubectl wait pod --for=condition=ready --timeout=120s -lapp=postgres
	kubectl apply -f docker/kube-infra/prefect.yaml
	kubectl apply -f docker/kube-infra/fastflows.yaml
    kubectl apply -f docker/kube-infra/ingress.yaml
	kubectl apply -f docker/kube-infra/prefect-queue.yaml
	kubectl wait pod --for=condition=ready --timeout=120s -lapp=orion

## show kube logs for orion
kube-logs-orion:
	kubectl logs -lapp=orion --all-containers

## show kube logs for orion
kube-logs-fastflows:
	kubectl logs -lapp=fastflows --all-containers
