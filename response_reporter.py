# requests_reporter.py
# note this requires the requests module
# pip (or pip3) install requests

import sys
from time import sleep, time
import requests

max_response = 0
tot_response = 0


def usage():
    """
    Prints the script usage information and exits with exit code 1. 
    """
    print("""

    USAGE: python3 response_reporter.py <url> [count]

    url:   required url to make the request (GET)
    count: optional number of requests to make

    """)
    exit(1)


def performance(fn):
    """
    Decorator function to capture and print the response times. 
    :param fn: function to pass to the decorator.
    """
    def wrapper(*args, **kwargs):
        t1 = time()
        status = fn(*args, **kwargs)
        t2 = time()
        response_time = t2 - t1
        global tot_response
        global max_response
        tot_response += response_time
        if response_time > max_response:
            max_response = response_time
        print(f'Response Time: {max_response} seconds, Status {status}.')

    return wrapper


@performance
def make_request(url) -> int:
    """
    Simple decorated request function to make the request and return the response. 
    :param 
    url: The URL to request via GET.
    :return: The response code.
    """
    res = requests.get(url)
    return res.status_code


def get_int(str_in) -> int:
    """
    Utility method to convert string to integer and to fail with usage if invalid type provided. 
    :param str_in: The string to convert to an integer.
    :return: The integer value for the given string.
    """
    try:
        int_out = int(str_in)
        return int_out
    except ValueError:
        print('Count must be an integer')
        usage()


def run_test(req_url, request_count=100):
    """
    Loop method to run the requests n amount of times and to print the results.
    :param req_url: The URL to make the requests with.
    :param request_count: The number of requests to make with a default value of 100 if None
    passed. 
    """
    print(f"Requesting URL: {req_url} {request_count} times...")
    for i in range(count):
        make_request(req_url)
        sleep(1)
    print(f"""

    Maximum Response Time     {max_response} seconds.
    Average Response Time     {tot_response / request_count} seconds.
    """)


if __name__ == '__main__':
    count = None
    if len(sys.argv) < 2:
        usage()
    request_url = sys.argv[1]
    if len(sys.argv) == 3:
        count = get_int(sys.argv[2])
    run_test(request_url, count)
