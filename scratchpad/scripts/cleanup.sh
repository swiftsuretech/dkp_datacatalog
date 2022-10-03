#!/bin/zsh

clear
if [ $# -eq 0 ]
  then
    echo "Please provide a namespace when you run the script"
    exit 
fi    

NAMESPACE=$1
ROOTDIR='/home/dswhitehouse/dkp_big_data_catalog'

echo "About to clear up resources in namespace: $NAMESPACE"
# sleep 10
echo "\nDeleting App Deployments"
kubectl get appdeployment -n $NAMESPACE -l kubefed.io/managed=true -o name 2>/dev/null | while read line; do
  echo "Deleting $line"
  kubectl delete $line -n $NAMESPACE 2>/dev/null
done
echo "--done"

# Patch the ceph cluster ready for deletion
echo "\nPatching Ceph cluster and deleting artifacts"
kubectl patch cephcluster rook-ceph -n rook-ceph --type merge -p '{"spec":{"cleanupPolicy":{"confirmation":"yes-really-destroy-data"}}}' 2>/dev/null
kubectl get crd -o name 2>/dev/null | grep ceph | while read line; do
  CRD=$(echo $line | cut -d "/" -f 2)
  echo "Checking for artifacts - $line"
  THING=$(kubectl get $CRD -n rook-ceph -o name 2>/dev/null)
  if [ ${#THING}  -ge 5 ]; then 
    echo deleting $THING
    kubectl delete $THING -n rook-ceph 2>/dev/null
  else
    echo "--None Found"
  fi
done
echo "--done"

echo "\nWaiting for all Ceph objects to shut down (Apart from the controller)"
while true; do
  COUNT=$(kubectl get po -n rook-ceph -o name --field-selector=status.phase==Running 2>/dev/null | wc -l)
  RUNNING=kubectl get po -n rook-ceph -o name --field-selector=status.phase==Running 2>/dev/null
  if [ $((COUNT)) -gt 1 ]; then
    echo "There are currently $COUNT pods running:"
    echo $RUNNING
  else
    break
  fi
  sleep 10
done
echo "--done"

echo "\nDeleting remaining Ceph stuff"
kubectl patch objectbucketclaim ceph-bucket -n rook-ceph -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null
kubectl patch objectbucket obc-rook-ceph-ceph-bucket -n rook-ceph -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null
kubectl delete objectbucketclaim ceph-bucket -n rook-ceph 2>/dev/null
kubectl delete -f $ROOTDIR/deployments/rook-clusters 2>/dev/null
kubectl delete objectbucket obc-rook-ceph-ceph-bucket -n rook-ceph 2>/dev/null
echo "--done"


echo "\nDeleting cleanup pods"
for cleanup in $(kubectl get po -n rook-ceph -o name 2>/dev/null | grep cleanup); do
  kubectl delete -n rook-ceph $cleanup 2>/dev/null
done
echo "--done"
  
echo "\nDeleting Elastic Stuff"
kubectl delete -f $ROOTDIR/deployments/elastic-clusters 2>/dev/null
kubectl delete -f $ROOTDIR/deployments/elastic-mapping 2>/dev/null
echo "--done"

echo "\nDeleting Kafka Stuff"
kubectl patch kafkatopic newsitem -n $NAMESPACE -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null
kubectl patch kafkacluster kafka -n $NAMESPACE -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null
kubectl delete -f $ROOTDIR/deployments/kafka-topics 2>/dev/null
kubectl delete -f $ROOTDIR/deployments/kafka-clusters 2>/dev/null
echo "--done"

echo "\nDeleting NiFi Stuff"
kubectl patch nificluster nifi-demo -n $NAMESPACE -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null
kubectl delete nificluster nifi-demo -n $NAMESPACE 2>/dev/null
kubectl patch nifiregistryclient registry-client -n $NAMESPACE -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null
kubectl delete nifiregistryclient registry-client -n $NAMESPACE 2>/dev/null
kubectl delete -f $ROOTDIR/deployments/nifi-clusters 2>/dev/null
echo "--done"

echo "\nDeleting GitOps sources"
kubectl get gitopsrepositories -n $NAMESPACE -o name 2>/dev/null | while read line; do                                                                                                                                                       130 ↵ ──(Mon,Oct03)─┘
  echo "Deleting $line"
  kubectl delete $line -n $NAMESPACE 2>/dev/null                                                                     
done
echo "--done"

echo "\nDeleting Kommander ConfigMaps"
kubectl get federatedconfigmap -n $NAMESPACE -o name 2>/dev/null | while read line; do
  echo "Deleting $line"
  kubectl delete $line -n $NAMESPACE 2>/dev/null
done
echo "--done"

echo "\nDeleting Kommander Secrets"
kubectl get federatedsecret -n $NAMESPACE -o name 2>/dev/null | while read line; do
  echo "Deleting $line"
  kubectl delete $line -n $NAMESPACE 2>/dev/null
done
echo "--done"

echo "\nUninstalling the Catalogue"
helm delete catalog -n $NAMESPACE 2>/dev/null
echo "--done"

echo "\nDeleting the project"
kubectl delete project $NAMESPACE -n kommander 2>/dev/null
echo "--done"

echo "Updating HELM"
helm repo update
echo "--done"

