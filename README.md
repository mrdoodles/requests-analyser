# requests-analyser

Use poetry or pip to install the requirements.
Recommend the use of poetry shell, virtualenv or anaconda.

Tested with python 3.9, should be compatible with 3.6 and perhaps earlier.

## log_analyser

Parses a log file in a proprietary format and reports response times

    USAGE: python3 log_analyser.py <log_file_path>

## response_reporter

Samples requests from a URL and summarises the response time (default 100 smples)

USAGE: python3 response_reporter.py <url> [count]

    url:   required url to make the request (GET)
    count: optional number of requests to make
