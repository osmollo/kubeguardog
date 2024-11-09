import os
import os.path

from log import logger
from socket import gaierror
from urllib3.exceptions import NameResolutionError, MaxRetryError
from kubernetes import client, config
from common import KUBECONFIG_PATH
from datetime import datetime, timezone


def check_kubeconfig() -> None:
    if not os.path.exists(path=KUBECONFIG_PATH):
        logger.error(f'{KUBECONFIG_PATH} must be a kubeconfig file')
        exit(code=2)
    logger.debug(f"The file '{KUBECONFIG_PATH}' exists")


def get_pods():
    config.load_kube_config(config_file=KUBECONFIG_PATH)

    kubectl = client.CoreV1Api()
    print("Listing pods with their IPs:")
    if 'NAMESPACE' in os.environ:
        ret = kubectl.list_namespaced_pod(namespace=os.environ.get('NAMESPACE'),
                                          watch=False,
                                          pretty=True)
    else:
        ret = kubectl.list_pod_for_all_namespaces(watch=False, pretty=True)
    for i in ret.items:
        # Obtener la edad del Pod
        restart_count = i.status.container_statuses[0].restart_count
        if restart_count > 0:
            logger.error(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}\t{i.status.phase}\t{restart_count}")
        # else:
        #     logger.info(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}\t{i.status.phase}\t{restart_count}")


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
