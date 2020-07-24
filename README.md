# OVH Dynhost

This app is used to link dynamically google cloud virtual machine external IPs to my DNS

## Accounts

### OVH

Create a token [here](https://eu.api.ovh.com/createToken/)

With the following rights :
```
GET /*
POST /*
PUT /*
DELETE /*
```

### Google Cloud

Create a service account with rights `Compute Viewer` and get the .json credentials file.

## Create Secret

```bash
echo -n '<ovh_consumer_key>' > ovh_consumer_key
echo -n '<ovh_application_key>' > ovh_application_key
echo -n '<ovh_application_secret>' > ovh_application_secret
kubectl create secret generic ovh-tokens \
    --from-file=ovh_consumer_key \
    --from-file=ovh_application_key \
    --from-file=ovh_application_secret \
    --namespace=ovh-mgmt
kubectl create secret generic gcloud-tokens \
    --from-file=credentials.json \
    --namespace=ovh-mgmt
```
