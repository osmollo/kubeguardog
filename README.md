# KUBEGUARDOG

- [KUBEGUARDOG](#kubeguardog)
  - [Dependencies](#dependencies)
    - [Environment variables](#environment-variables)
    - [Volumes](#volumes)
  - [How to execute](#how-to-execute)
    - [List pods of all namespaces:](#list-pods-of-all-namespaces)
    - [List pods of namespace `example-ns`:](#list-pods-of-namespace-example-ns)
    - [Send notifications to Telegram:](#send-notifications-to-telegram)
  - [Alternative motherfucking way](#alternative-motherfucking-way)

## Dependencies

### Environment variables

|**NAME**|**DESCRIPTION**|**DEFAULT VALUE**|**REQUIRED**|
|---|---|:---:|:---:|
|NAMESPACE|List pods of this namespace|`all`|NO|
|LOG_LEVEL|Logging level|`INFO`|NO|
|WEBHOOK_URL|Webhook URL for sending events||NO|
|TELEGRAM_TOKEN|Token for Telegram authentication||NO|
|TELEGRAM_CHAT_ID|ID of the Telegram user/group to send notifications||NO1

### Volumes

|**TYPE**|**CONTAINER PATH**|**DESCRIPTION**|
|---|---|---|
|file|`/kubeconfig.yaml`|Kubeconfig file|

## How to execute

### List pods of all namespaces:

```shell
docker run -ti --rm --network host \
-v ~/kubeconfig/ef1bau.yaml:/kubeconfig.yaml \
kubeguardog:latest kubeguardog.py
```

### List pods of namespace `example-ns`:

```shell
docker run -ti --rm --network host \
-v ~/kubeconfig/ef1bau.yaml:/kubeconfig.yaml \
-e NAMESPACE=example-ns \
kubeguardog:latest kubeguardog.py
```

### Send notifications to Telegram:

```shell
docker run -ti --rm --network host \
-v ~/kubeconfig/ef1bau.yaml:/kubeconfig.yaml \
-e NAMESPACE=example-ns \
-e TELEGRAM_TOKEN="<TELEGRAM_TOKEN>" \
-e TELEGRAM_CHAT_ID=<TELEGRAM_CHAT_ID" \
kubeguardog:latest kubeguardog.py
```

## Alternative motherfucking way

```shell
kubectl --kubeconfig ~/kubeconfig/file.yaml get pods | awk '$4>0'
```
