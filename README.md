# 42 Webserver Tester

Small tester to benchmark request handling and responses for our 42 webserver.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)

## Setup

### 1. Python Environment

It is recommended to use a virtual environment.

```bash
cd python_tester
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Nginx CGI Server (Reference)

Build and run the Nginx container which serves as the reference for tests.

```bash
cd nginx_cgi
docker compose up --build
```
This will start the Nginx server on port `9092`.

### 3. Your C++ Webserver

Ensure your C++ webserver is running. By default, the tester expects it at `http://127.0.0.1:8081`.

## Running Tests

Run the python tester script:

```bash
# From the project root or python_tester directory
python3 python_tester/webserv_test.py
```

## Configuration

You can configure the target servers using environment variables:

- `CPP_SERVER`: URL of your C++ webserver (default: `http://127.0.0.1:8081`)
- `NGINX_SERVER`: URL of the reference Nginx server (default: `http://localhost:9092`)

Example:

```bash
export CPP_SERVER="http://localhost:8080"
python3 python_tester/webserv_test.py
```
