import os
import os.path
import datetime

from log import logger
from common import KUBECONFIG_PATH
from telegram import send_telegram_message

from socket import gaierror
from tabulate import tabulate
from kubernetes import client, config
from urllib3.exceptions import NameResolutionError, MaxRetryError
from kubernetes.client.exceptions import ApiException


def check_kubeconfig() -> None:
    if not os.path.exists(path=KUBECONFIG_PATH):
        logger.error(f'{KUBECONFIG_PATH} must be a kubeconfig file')
        exit(code=2)
    logger.debug(f"The file '{KUBECONFIG_PATH}' exists")


def format_age(pod_age_timedelta) -> str:
    if pod_age_timedelta.days > 0:
        pod_age = f"{pod_age_timedelta.days}d"
    elif pod_age_timedelta.seconds // 3600 > 0:
        pod_age = f"{pod_age_timedelta.seconds // 3600}h"
    elif pod_age_timedelta.seconds // 60 > 0:
        pod_age = f"{pod_age_timedelta.seconds // 60}m"
    else:
        pod_age = f"{pod_age_timedelta.seconds}s"
    return pod_age


def get_pods():
    config.load_kube_config(config_file=KUBECONFIG_PATH)

    kubectl = client.CoreV1Api()
    v1 = client.CoreV1Api()
    node = v1.list_node().items[0]
    cluster_name = node.metadata.annotations.get('cluster.x-k8s.io/cluster-name')

    if 'NAMESPACE' in os.environ:
        ret = kubectl.list_namespaced_pod(namespace=os.environ.get('NAMESPACE'),
                                          watch=False,
                                          pretty=True)
    else:
        ret = kubectl.list_pod_for_all_namespaces(watch=False, pretty=True)

    restarted_pod = False
    pods = []
    headers = ['CLUSTER_NAME', 'POD NAME', 'NAMESPACE', 'IP', 'STATUS', 'RESTARTS', 'AGE']
    for i in ret.items:
        # Obtener la edad del Pod
        restart_count = i.status.container_statuses[0].restart_count
        if restart_count > 0:
            restarted_pod = True
            pod_start_time = i.status.start_time
            pod_age_timedelta = datetime.datetime.now(datetime.timezone.utc) - pod_start_time
            pods.append([cluster_name,
                         i.metadata.name,
                         i.metadata.namespace,
                         i.status.pod_ip,
                         i.status.phase,
                         restart_count,
                         format_age(pod_age_timedelta)])
    print(tabulate(tabular_data=pods,
                   headers=headers,
                   tablefmt='rounded_outline'))

    if restarted_pod and 'TELEGRAM_TOKEN' in os.environ and 'TELEGRAM_CHAT_ID' in os.environ:
        send_telegram_message(token=os.environ.get('TELEGRAM_TOKEN'),
                              chat_id=os.environ.get('TELEGRAM_CHAT_ID'),
                              text=f"K8s cluster *{cluster_name}* has restarted pods:\n\n{'\n'.join([x[1].replace('-', '\\-') for x in pods])}")


def main() -> None:
    check_kubeconfig()
    try:
        get_pods()
    except ConnectionRefusedError as e:
        logger.error(msg=f"Connection refused: {e.reason}")
        exit(code=3)
    except gaierror as e:
        logger.error(msg=f"Socket error: {e.reason}")
        exit(code=4)
    except NameResolutionError as e:
        logger.error(msg=f"Name resolution error: {e.reason}")
        exit(code=5)
    except MaxRetryError as e:
        logger.error(msg=f"Max retries exceeded: {e.reason}")
        exit(code=6)
    except ApiException as e:
        logger.error(msg=f"API Exception: {e.reason}")
        exit(code=7)


if __name__ == "__main__":
    main()
