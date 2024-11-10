import os
import os.path

from log import logger
from common import KUBECONFIG_PATH
from telegram import send_telegram_message

from socket import gaierror
from urllib3.exceptions import NameResolutionError, MaxRetryError
from kubernetes import client, config


def check_kubeconfig() -> None:
    if not os.path.exists(path=KUBECONFIG_PATH):
        logger.error(f'{KUBECONFIG_PATH} must be a kubeconfig file')
        exit(code=2)
    logger.debug(f"The file '{KUBECONFIG_PATH}' exists")


def get_pods():
    config.load_kube_config(config_file=KUBECONFIG_PATH)

    kubectl = client.CoreV1Api()
    if 'NAMESPACE' in os.environ:
        ret = kubectl.list_namespaced_pod(namespace=os.environ.get('NAMESPACE'),
                                          watch=False,
                                          pretty=True)
    else:
        ret = kubectl.list_pod_for_all_namespaces(watch=False, pretty=True)

    restarted_pod = False
    pods = []
    for i in ret.items:
        # Obtener la edad del Pod
        restart_count = i.status.container_statuses[0].restart_count
        if restart_count > 0:
            restarted_pod = True
            pods.append(i.metadata.name.replace("-", "\\-"))
            logger.error(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}\t{i.status.phase}\t{restart_count}")

    if restarted_pod:
        if 'TELEGRAM_TOKEN' in os.environ and 'TELEGRAM_CHAT_ID' in os.environ:
            v1 = client.CoreV1Api()
            node = v1.list_node().items[0]
            cluster_name = node.metadata.annotations.get('cluster.x-k8s.io/cluster-name')
            send_telegram_message(token=os.environ.get('TELEGRAM_TOKEN'),
                                  chat_id=os.environ.get('TELEGRAM_CHAT_ID'),
                                  text=f"K8s cluster *{cluster_name}* has restarted pods:\n\n{'\n'.join(pods)}")
        if 'WEBHOOK_URL' in os.environ:
            pass


def main() -> None:
    check_kubeconfig()
    try:
        get_pods()
    except ConnectionRefusedError:
        logger.error(f"Connection refused")
        exit(code=3)
    except gaierror:
        logger.error(f"Socket error")
        exit(code=4)
    except NameResolutionError:
        logger.error(f"Name resolution error")
        exit(code=5)
    except MaxRetryError:
        logger.error(f"Max retries exceeded")
        exit(code=6)


if __name__ == "__main__":
    main()
