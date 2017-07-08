.. title: Kubernetes: Working with Images in Private Repos on Docker Hub
.. slug: kubernetes-working-with-images-in-private-repos-on-docker-hub
.. date: 2016-05-19 12:02:55 UTC+10:00
.. tags: kubernetes, docker, docker hub, devops, draft
.. category: coding
.. link: 
.. description: 
.. type: text

..  code:: console

    $ kubectl create -f web-example
    persistentvolumeclaim "tinydb-pv-claim" created
    deployment "web-example" created
    service "web-example" created
    persistentvolume "aws-pv-001" created

..  code:: console

    $ kubectl get pods
    NAME                           READY     STATUS         RESTARTS   AGE
    web-example-2455310000-032qp   1/2       ErrImagePull   0          3m

..  code:: console

    $ kubectl get events
    FIRSTSEEN   LASTSEEN   COUNT     NAME                           KIND      SUBOBJECT                            TYPE      REASON             SOURCE                                                    MESSAGE
    8m          6m         11        web-example-2455310000-032qp   Pod                                            Warning   FailedScheduling   {default-scheduler }                                      PersistentVolumeClaim is not bound: "tinydb-pv-claim"
    6m          6m         1         web-example-2455310000-032qp   Pod                                            Normal    Scheduled          {default-scheduler }                                      Successfully assigned web-example-2455310000-032qp to ip-10-0-0-183.ap-southeast-2.compute.internal
    6m          6m         1         web-example-2455310000-032qp   Pod       spec.containers{web-example-nginx}   Normal    Pulling            {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   pulling image "terriajs/web-example-nginx"
    5m          5m         1         web-example-2455310000-032qp   Pod       spec.containers{web-example-nginx}   Normal    Pulled             {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   Successfully pulled image "terriajs/web-example-nginx"
    5m          5m         1         web-example-2455310000-032qp   Pod       spec.containers{web-example-nginx}   Normal    Created            {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   Created container with docker id 0069b654869f
    5m          5m         1         web-example-2455310000-032qp   Pod       spec.containers{web-example-nginx}   Normal    Started            {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   Started container with docker id 0069b654869f
    5m          2m         5         web-example-2455310000-032qp   Pod       spec.containers{web-example-flask}   Normal    Pulling            {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   pulling image "terriajs/web-example-flask"
    5m          2m         5         web-example-2455310000-032qp   Pod       spec.containers{web-example-flask}   Warning   Failed             {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   Failed to pull image "terriajs/web-example-flask": Error: image terriajs/web-example-flask not found
    5m          2m         5         web-example-2455310000-032qp   Pod                                            Warning   FailedSync         {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   Error syncing pod, skipping: failed to "StartContainer" for "web-example-flask" with ErrImagePull: "Error: image terriajs/web-example-flask not found"

    5m        9s        23        web-example-2455310000-032qp   Pod       spec.containers{web-example-flask}   Normal    BackOff      {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   Back-off pulling image "terriajs/web-example-flask"
    5m        9s        23        web-example-2455310000-032qp   Pod                                            Warning   FailedSync   {kubelet ip-10-0-0-183.ap-southeast-2.compute.internal}   Error syncing pod, skipping: failed to "StartContainer" for "web-example-flask" with ImagePullBackOff: "Back-off pulling image \"terriajs/web-example-flask\""

    8m        8m        1         web-example-2455310000-fngpt   Pod          spec.containers{web-example-nginx}   Normal    Killing                {kubelet ip-10-0-0-184.ap-southeast-2.compute.internal}   Killing container with docker id 8b5e7cf9b505: Need to kill pod.
    8m        8m        1         web-example-2455310000-fngpt   Pod          spec.containers{web-example-flask}   Normal    Killing                {kubelet ip-10-0-0-184.ap-southeast-2.compute.internal}   Killing container with docker id 2f8dcbb94508: Need to kill pod.
    8m        8m        1         web-example-2455310000         ReplicaSet                                        Normal    SuccessfulDelete       {replicaset-controller }                                  Deleted pod: web-example-2455310000-fngpt
    8m        8m        1         web-example-2455310000         ReplicaSet                                        Normal    SuccessfulCreate       {replicaset-controller }                                  Created pod: web-example-2455310000-032qp
    8m        8m        1         web-example                    Deployment                                        Normal    ScalingReplicaSet      {deployment-controller }                                  Scaled up replica set web-example-2455310000 to 1
    8m        8m        1         web-example                    Service                                           Normal    DeletedLoadBalancer    {service-controller }                                     Deleted load balancer
    8m        8m        2         web-example                    Service                                           Normal    CreatingLoadBalancer   {service-controller }                                     Creating load balancer
    8m        8m        2         web-example                    Service                                           Normal    CreatedLoadBalancer    {service-controller }                                     Created load balancer

..  code:: console

    $ kubectl delete -f web-example
    persistentvolumeclaim "tinydb-pv-claim" deleted
    deployment "web-example" deleted
    service "web-example" deleted
    persistentvolume "aws-pv-001" deleted

..  code:: console

    $ kubectl create secret docker-registry --help
    Create a new secret for use with Docker registries.

    Dockercfg secrets are used to authenticate against Docker registries.

    When using the Docker command line to push images, you can authenticate to a given registry by running
      'docker login DOCKER_REGISTRY_SERVER --username=DOCKER_USER --password=DOCKER_PASSWORD --email=DOCKER_EMAIL'.
    That produces a ~/.dockercfg file that is used by subsequent 'docker push' and 'docker pull' commands to
    authenticate to the registry.

    When creating applications, you may have a Docker registry that requires authentication.  In order for the
    nodes to pull images on your behalf, they have to have the credentials.  You can provide this information
    by creating a dockercfg secret and attaching it to your service account.

    Usage:
      kubectl create secret docker-registry NAME --docker-username=user --docker-password=password --docker-email=email [--docker-server=string] [--from-literal=key1=value1] [--dry-run] [flags]

    Examples:
      # If you don't already have a .dockercfg file, you can create a dockercfg secret directly by using:
      $ kubectl create secret docker-registry my-secret --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL

..  code:: console

    $ kubectl create secret docker-registry docker-hub --docker-username=REDACTED \
    >                                                  --docker-password=REDACTED \
    >                                                  --docker-email=REDACTED \
    >                                                  --docker-server="https://index.docker.io/v1/" \
    >                                                  --dry-run --output=yaml
    apiVersion: v1
    data:
      .dockercfg: REDACTED
    kind: Secret
    metadata:
      creationTimestamp: null
      name: docker-hub
    type: kubernetes.io/dockercfg

..  code:: console

    $ kubectl create secret docker-registry docker-hub --docker-username=REDACTED \
    >                                                  --docker-password=REDACTED \
    >                                                  --docker-email=REDACTED \
    >                                                  --docker-server="https://index.docker.io/v1/" \
    secret "docker-hub" created

..  code:: console

    $ kubectl get secrets
    NAME                  TYPE                                  DATA      AGE
    default-token-24hxr   kubernetes.io/service-account-token   3         1d
    docker-hub            kubernetes.io/dockercfg               1         1m

..  code:: console

    $ kubectl describe secrets docker-hub
    Name:       docker-hub
    Namespace:  default
    Labels:     <none>
    Annotations:    <none>

    Type:   kubernetes.io/dockercfg

    Data
    ====
    .dockercfg: 135 bytes

..  code:: console

    $ kubectl create -f web-example
    persistentvolumeclaim "tinydb-pv-claim" created
    deployment "web-example" created
    service "web-example" created
    persistentvolume "aws-pv-001" created

..  code:: 

    $ kubectl get pods
    NAME                           READY     STATUS    RESTARTS   AGE
    web-example-2673741533-ydbrw   2/2       Running   0          1h

- https://docs.docker.com/docker-hub/repos/#private-repositories
- http://kubernetes.io/docs/user-guide/kubectl/kubectl_create_secret_docker-registry/
- http://kubernetes.io/docs/user-guide/images/#creating-a-secret-with-a-docker-config
