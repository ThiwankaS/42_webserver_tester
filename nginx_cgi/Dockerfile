FROM nginx:latest

# Install CGI wrapper, spawn-fcgi, and Python
RUN apt-get update && apt-get install -y \
    fcgiwrap \
    spawn-fcgi \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]