# 42 Webserver Tester

A lightweight benchmarking and validation tool designed to test request handling, HTTP responses, and CGI logic for the **42 Webserv** project.

## Overview

This tester compares your C++ Webserver implementation against a reference **Nginx** environment. By running both side-by-side, you can ensure your server handles headers, body sizes, and CGI scripts according to industry standards.

---

## Prerequisites

* **Docker & Docker Compose**
* **Python 3.8+**
* **C++ Webserver** (Your project)

---

## Setup Instructions

### 1. Python Environment
It is recommended to use a virtual environment to keep your global dependencies clean.

```bash
# Navigate to the tester directory
cd python_tester

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Nginx CGI Reference Server

The Nginx container acts as the "Gold Standard" for your tests.

1. **Prepare Assets:**
* Place your test website files inside `nginx_cgi/www/`.
* Place your CGI scripts inside `nginx_cgi/cgi-bin/`.
* Update `nginx.conf` to match your server's expected limits (e.g., `client_max_body_size`, `proxy_read_timeout`).


2. **Set Permissions:**
```bash
chmod +x nginx_cgi/cgi-bin/*
chmod +x nginx_cgi/entrypoint.sh

```

3. **Launch the Reference Server:**
```bash
cd nginx_cgi
docker compose up --build -d

```

*The reference server will be accessible at `http://localhost:9092`.*

### 3. Configure Your C++ Webserver

Ensure your C++ webserver is compiled and running.

* **Default Target:** `http://127.0.0.1:8081`
* **Note:** If your server uses a different port, update the configuration constants at the top of `python_tester/webserv_test.py`.

---

## Running Tests

Run the main execution script from the project root:

```bash
python3 python_tester/webserv_test.py

```

### Analyzing Results

* **Success:** All green? Your server is behaving as expected.
* **Failure:** Check the generated `test_results/` directory. For every failed test, a trace file is created detailing the discrepancy between your server and Nginx.
* **Hot Reloading:** If you modify your CGI scripts or Nginx config, restart the container:
```bash
docker compose down && docker compose up --build -d

```

---

## Technical Tips

> [!TIP]
> **Consistency is Key:** Ensure that the `MAX_BODY_SIZE` and `REQUEST_TIMEOUT` values in your `nginx.conf` are identical to those in your C++ config file. This prevents "false positive" failures caused by different server constraints.

**Enjoy, Happy Coding!**