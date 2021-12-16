# log_analyser.py

import re
import sys
from os import path

"""
This is a sample of the log format 

IP_ADDRESS - - [01/Jan/2021:00:00:01 +0000] "GET/site-url?ref=http%3A%2F%2Fwww.somesite.co.uk%2 Fav%2Topic%2F 
HTTP/1.1" 200 32 "https://www.somesite.co.uk/topics/favorite/" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1;
Trident/4.0; InfoPath.1; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648;
.NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)" 2718 "94zv630" 
"OK" "C=1 BC=0 BF=0 CU=0 CC=0" "-" "topics_favorite (22.848) " "1672251521" "main""https://www.somesite.co.uk/topics/favorite/"
"""


def usage():
    """
    Prints the script usage information and exits with exit code 1. 
    """
    print("""

      USAGE: python3 log_analyser.py <log_file_path>

    """)
    exit(1)


def is_file(file_path) -> bool:
    """
    Validates that the input string is a valid file and not a directory. 
    :param file_path: The validated path to the file.
    :return: True if valid, False otherwise.
    """
    if path.exists(file_path) and path.isfile(file_path):
        return True
    return False


def milli_to_micro(milli):
    """
    Utility function to convert milliseconds to microseconds. 
    :param milli: The milliseconds to convert.
    :return: The milliseconds to converted to microseconds. 
    """
    return milli * 1000


def parse_file(file_path):
    """
    Parses the file in reverse order, filters the response time 
    as per the custom format and finally prints the results.
    :param file_path: 
    :return:
    """
    count = 0
    total = 0
    t100ms = 0
    t500ms = 0
    t1s = 0
    pattern = re.compile(r'.*\)\" (?P<response_time>.*?) ')
    try:
        for line in reversed(open(file_path).readlines()):
            count += 1
            if count > 100000:
                break
            matches = re.findall(pattern, line)
            response = int(matches[0])
            total += response
            # Response times in microseconds
            # Greater that 1 second
            if response > milli_to_micro(1000):
                t1s += 1
                continue
            # Greater than 500 milliseconds (ms)
            if response > milli_to_micro(500):
                t500ms += 1
                continue
            # Greater than 100 milliseconds (ms)
            if response > milli_to_micro(100):
                t100ms += 1
            if count == 10000:
                break
        avg = total / count
        print(f"""
        Total lines read:         {count}
        Average response time (microseconds): {avg}
        Total requests slower than 100ms:  {t100ms} 
        Total requests slower than 500ms:  {t500ms}
        Total requests slower that 1s:   {t1s}
        """)
    except FileNotFoundError as err:
        print('File not found')
        print(err)
        # raise err
    except IOError as err:
        print("Error reading/writing to file")
        print(err)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    log_file_path = sys.argv[1]
    if is_file(log_file_path):
        parse_file(log_file_path)
    else:
        usage()
