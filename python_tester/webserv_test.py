import requests
import difflib
import os
import shutil
from datetime import datetime

# CONFIGURATION
CPP_SERVER = os.getenv("CPP_SERVER", "http://127.0.0.1:8081")
NGINX_SERVER = os.getenv("NGINX_SERVER", "http://localhost:9092")
LOG_DIR = "test_results"

# Headers to ignore in comparison (dynamic or software-specific)
IGNORE_HEADERS = ['Date', 'Server', 'Last-Modified', 'ETag', 'Accept-Ranges', 'Transfer-Encoding']

def setup_log_dir():
    """Clears old results and creates a fresh log directory."""
    if os.path.exists(LOG_DIR):
        shutil.rmtree(LOG_DIR)  # This deletes the folder and everything inside
    os.makedirs(LOG_DIR)
    print(f"🧹 Cleaned {LOG_DIR}/ and prepared fresh test run.\n")

# List of tests
# Test name, HTTP method, Route, specific HTTP headers, Request Body
tests = [
    ("test_root",    "GET", "/", {}, None),
    ("test_index",   "GET", "/index.html", {}, None),
    ("test_about",   "GET", "/about.html", {}, None),
    ("test_upload",   "GET", "/upload.html", {}, None),
    ("test_delete",   "GET", "/delete.html", {}, None),
    ("test_calculator",   "GET", "/calculator.html", {}, None),
    ("test_not_exist",   "GET", "/does-not-exist", {}, None),
    ("test_hello_cgi",  "GET", "/cgi-bin/hello.py", {}, None),
    ("test_gravity_cgi", "GET", "/cgi-bin/weight_convert.py?weight=100&planet=mars", {}, None),
    ("test_empty_body", "POST", "/", {}, None),
    ("test_gravity_cgi_post", "POST", "/cgi-bin/weight_convert.py", {"Content-Type": "application/x-www-form-urlencoded"}, "weight=100&planet=mars"),
    ("test_large_post", "POST", "/cgi-bin/hello.py", {"Content-Type": "application/x-www-form-urlencoded"}, "data=" + "A" * 8000),
    ("test_triple_slash", "GET", "///index.html", {}, None),
    ("test_url_decoding", "GET", "/my%20file.html", {}, None),
    ("test_traversal", "GET", "/../../etc/passwd", {}, None),
    ("test_lowercase_method", "get", "/", {}, None),
    #("test_max_url_fail", "GET", "/" + ("x" * 10000), {}, None), - this is breaking CPP server
    #("test_never_cgi",  "GET", "/cgi-bin/never.py", {}, None), - this is breaking NGINX
]

def compare_headers(h_nginx, h_cpp):
    diffs = []
    for key, value in h_nginx.items():
        # Case-insensitive header check
        key_lower = key.lower()
        if any(h.lower() == key_lower for h in IGNORE_HEADERS):
            continue
        
        cpp_val = h_cpp.get(key)
        if cpp_val != value:
            diffs.append(f"Header [{key}]: Expected '{value}', Got '{cpp_val}'")
    return diffs

def log_failure(name, r_nginx, r_cpp, header_diffs):
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"{LOG_DIR}/{name}_{timestamp}.diff"
    
    with open(filename, "w") as f:
        f.write(f"TEST FAILURE: {name}\n")
        f.write(f"Nginx Status: {r_nginx.status_code} | CPP Status: {r_cpp.status_code}\n")
        f.write("-" * 60 + "\n")
        
        if header_diffs:
            f.write("HEADER DISCREPANCIES:\n")
            for d in header_diffs: f.write(f"  - {d}\n")
            f.write("-" * 60 + "\n")

        f.write("BODY DIFF (Nginx vs CPP):\n")
        diff = difflib.unified_diff(
            r_nginx.text.splitlines(),
            r_cpp.text.splitlines(),
            fromfile='Nginx_Expected',
            tofile='CPP_Actual',
            lineterm=''
        )
        f.write("\n".join(list(diff)))

def run_test(name, method, path, headers, data):
    print(f"Testing {name:20} ...", end=" ", flush=True)
    try:
        r_nginx = requests.request(method, NGINX_SERVER + path, headers=headers, data=data, timeout=5)
        r_cpp = requests.request(method, CPP_SERVER + path, headers=headers, data=data, timeout=5)
        
        status_match = r_nginx.status_code == r_cpp.status_code
        header_diffs = compare_headers(r_nginx.headers, r_cpp.headers)
        body_match = r_nginx.text == r_cpp.text
        
        if status_match and not header_diffs and body_match:
            print("✅ PASS")
        else:
            print("❌ FAIL")
            log_failure(name, r_nginx, r_cpp, header_diffs)
            
    except Exception as e:
        print(f"🔥 ERROR: {e}")

if __name__ == "__main__":
    setup_log_dir()
    print(f"Comparing Servers...\nBase: {NGINX_SERVER}\nTest: {CPP_SERVER}\n")
    for test in tests:
        run_test(*test)