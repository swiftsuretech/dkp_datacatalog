 <img src="../images/d2iq.png" alt="alt text" width="50"/><img src="../images/nifi.png" alt="alt text" width="50"/>

# Running a big data stack on DKP

## Full Version

### Notes

- This is the detailed version. Field engineers and experienced DKP users wishing to use the tldr version should see [this guide](./catalog-deploy-tldr-version.md).
- In order to follow along with this tutorial, it is advised that you clone this repository to your local machine.

### Pre-requisites

- A healthy DKP cluster, ver 2.0 or later.
- DKP User Interface Installed.
- Basic knowledge of Kubernetes.
- IF deploying a new cluster; suitable credentials to do so [(see here)](https://docs.d2iq.com/dkp/2.3/infrastructure-providers).
- kubectl and helm installed on your local machine.
- ***Important***: This demonstration uses ceph storage provided by Rook. Whilst our deployment will allow us to deploy a ceph cluster for the project, we need to have the controller pre-installed on the cluster. It is not appropriate to do this from a catalog application as the cleanup in particular is comples. With the operator in place, we will use the catalogue item to deploy individual ceph clusters and associated buckets and object stores later in the process. Run the following to check if the operator is already present:

    ```bash
    # Do a system wide check to see if our operator is present. If the operator pod is returned and shows healthy, we can move on.
    kubectl get po -n rook-ceph -l app=rook-ceph-operator
    ```
    If there is no ceph operator installed on the system, deploy it as follows:
    ```bash
    # Add the rook repo and install the operator
    helm repo add rook-release https://charts.rook.io/release
    helm repo update
    helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph
    # Check the status of the operator. It may take a few minutes to come up
    watch kubectl get po -n rook-ceph -l app=rook-ceph-operator
    ```
### Scope

- The aim of the project is to deploy a fully functioning big data streaming stack into DKP that incorporates ingestion, processing, object storage, a document store and a front end application for analysis.
- This is an opinionated stack that uses, wherever possible, kubernetes "operators" to manage deployments. The examples shown are provided using a basic configuration and are therefore not production ready.  Operators allow the end user to configure their deployment with broadly the same options as bare metal deployments. It is advisable to review the latest documents pertaining to each of the product APIs for a production deployment.
- DKP provides users with the facility to create their own custom catalogue applications. Further details may be found in the [DKP documentation](https://docs.d2iq.com/dkp/2.3/custom-applications). This repository serves as an advanced example of that.

### Opinionated Technologies

- Links to the relevant operators can be found as follows:  
<br />
<center>

|Product|Type|Operator|Version|Link|
|---|---|---|---|---|
|Apache NiFi|Operator|nifNiFiKopikop|0.14.1|[NiFiKop]([link](https://konpyutaika.github.io/nifikop/docs/1_concepts/1_start_here))
|Apache Kafka|Operator|koperator|0.21.2|[koperator]([Link](https://github.com/banzaicloud/koperator))|
|NiFi Registry|Helm Chart|dysnix|1.1.0|[ArtifactHub]([Link](https://artifacthub.io/packages/helm/dysnix/nifi-registry))|
|Elasticsearch with Kibana|Operator|ECK|2.4.0|[Elastic ECK]([Link](https://www.elastic.co/blog/introducing-elastic-cloud-on-kubernetes-the-elasticsearch-operator-and-beyond))|
|Rook Ceph Storage|Operator|Rook|1.10.0|[Rook]([Link](https://rook.io/docs/rook/v1.10/Getting-Started/quickstart/))|
|Streamlit|Helm Chart|Custom|0.1.0|[Streamlit]([Link](https://streamlit.io/))|

</center>
<br />
The technology stack for this deployment is as follows:
<br/><br/>

<p align="center"> <img src="../diagrams/architecture.png" alt="alt text" width="800"/></p>

### Preparing the Environment

1. Ensure you have a healthy management cluster with the DKP user interface installed. Although it is possible to run the stack on the management cluster, it is highly advisable to create a new cluster specifically for this purpose. You may either add a cluster through the User Interface or attach an existing one.

2. NiFi is a heavyweight application written in Java. As such, it requires ample physical resources to function correctly. Worker nodes on the target cluster should meet the following requirements:
<br/><br/>

<center>

||Minimum|Recommended|
|---|:--:|:--:|
|Worker Nodes|4|8|
|CPUs|8|16|
|Memory|16Gi|32Gi|

</center>

### Configure a new workspace

1. Select "Workspace" from the sidebar menu and then "Create Workspace".

<p align="center"><img src="../images/create_workspace.png" alt="Create a Workspace" width="800" /></p>

2. Select the new workspace from the top menu.

### ***Optional***: Add a dedicated cluster

1. In the new workspace, select "Clusters" from the sidebar menu and select "Add Cluster". There are several ways to add a new cluster. For further information, see the DKP documentation [here]([link](https://docs.d2iq.com/)).

## Create a new project

1. From the "Projects" menu in the sidebar, create a new project:

- Name the project appropriately and ensure that you manually set the namespace from the default to the same as the project name (see highlighted diagram).
- Select the cluster you wish to deploy to. This would normally be a dedicated cluster but you may also use the DKP Management Cluster for demonstration purposes.
<p align="center"><img src="../images/new_project.png" alt="Create a Project" width="800" /></p>

  > ⚠️ To ensure that all your artifacts are deployed to the correct namespace, it is strongly advised to set kubeconfig context to your new namespace as follows:
    ```bash
    kubectl config set-context --current --namespace=data-demo 
    ```

## Deploy the catalogue

1. Ensure that you have cloned this repository to enable deployment of the HELM charts locally. Advanced users may use the registry version of this repo from Github.
2. Ensure that you deploy the registry to the correct namespace by following the step above or, alternatively, setting your namespace as an env variable:

  ```bash
  helm install catalog charts/data-catalog
  ```
3. Open your project to the "Applications" tab. You should see that the catalogue applications are now available.
<p align="center"><img src="../images/apps_deployed.png" alt="Apps" width="800" /></p>

## Deploy our custom applications

1. We are now ready to deploy our custom applications. For the purpose of this demo, we will build out object storage in a data lake provisioned in Ceph storage by the Rook operator 