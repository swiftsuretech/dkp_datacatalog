 <img src="./images/d2iq.png" alt="alt text" width="50"/><img src="./images/nifi.png" alt="alt text" width="50"/>
 # Apache NiFi in DKP

## Scope

The scope of the project is as follows:

- Generate a HELM chart that runs Apache NiFi with scaleable clusters
- Provide NiFe registry instance for flow version control and collaborative development
- Add the NiFi software as a catalogue item, deployable from the DKP UI
- Provide simple but meaningful configuration options to the end user
- Ensure the chart is available in an air-gapped deploy scenario

## Overview

There are a small number of existing HELM charts available through bitnami and artifact hub. These are traditional HELM charts that, with some configuration, will run on the DKP platform. However, none of the exiting iterations allow for a stable NiFi cluster experience and function as a single node only. This is not suitable for a production deployment owing to the lack of resilience.

There is an active project called NiFiKop, standing for NiFi Kubernetes Operator, which seeks to address these issues and provide a true NiFi experience tailored specifically for Kubernetes.

Rather than a helm chart consisting of a Stateful Set and peripheral services, it is a bespoke controller for NiFi. It generates a number of CRDs which allow the user to generate a cluster object, as well as advanced feature such as user and access management and dataflows.

The project is available [here](https://konpyutaika.github.io/nifikop/). It is open source, under active development but still in beta.

NiFi nodes run in pods that **are not** part of a stateful set. The reasons for this are to permit us to:
- Modify the configuration of unique Nodes
- Remove specific Nodes from clusters
- Use multiple Persistent Volumes for each Node

None of which are currently possible using a Stateful Set

The controller, utilising Zookeeper, manages the cluster functions for us to offer a bare metal type NiFi cluster experience.
## Pre-Requisites


## Installation


## Configuration


## Ingress


## Uninstallation


## Further Notes