import time
import boto3
import requests
import threading
from datetime import datetime
from instances import *
from SecurityGroup import *
from KeyPair import *
from ELB import *


def scenario1(elb_dns, path):
    """
    Function that gets 1000 requests sequentially

    :param elb_dns: dns of the ELB
    :param path: path to specify --> /cluster1 or /cluster2
    """
    for req in range(1000):
        response = requests.get("http://" + elb_dns + path)

def scenario2(elb_dns, path):
    """
    Function that gets 500 requests, sleep 1min, then getting 1000 requests

    :param elb_dns: dns of the ELB
    :param path: path to specify --> /cluster1 or /cluster2
    """
    for req in range(500):
        response = requests.get("http://" + elb_dns + path)
    time.sleep(60)
    for req in range(1000):
        response = requests.get("http://" + elb_dns + path)


def benchmark(elb_dns):
    """
    Function that commits the benchmark

    :param elb_dns: dns of the ELB
    """
    # Cluster 1 benchmark
    now = datetime.now()
    print(str(now) + " --> Starting benchmark for cluster 1")
    thread1 = threading.Thread(target=scenario1, args=(
        elb_dns,
        "/cluster1",
    ))
    thread2 = threading.Thread(target=scenario2, args=(
        elb_dns,
        "/cluster1",
    ))

    now = datetime.now()
    print(str(now) + " --> Starting both threads for cluster 1")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    now = datetime.now()
    print(str(now) + " --> Ending benchmark for cluster 1")

    # Cluster 2 benchmark
    now = datetime.now()
    print(str(now) + " --> Starting benchmark for cluster 2")
    thread1 = threading.Thread(target=scenario1, args=(
        elb_dns,
        "/cluster2",
    ))
    thread2 = threading.Thread(target=scenario2, args=(
        elb_dns,
        "/cluster2",
    ))

    now = datetime.now()
    print(str(now) + " --> Starting both threads for cluster 2")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    now = datetime.now()
    print(str(now) + " --> Ending benchmark for cluster 2")