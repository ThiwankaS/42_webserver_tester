#!/bin/sh

# Start the CGI wrapper using the Ubuntu path
# -s: socket, -u: user, -g: group
spawn-fcgi -s /var/run/fcgiwrap.socket -u www-data -g www-data /usr/sbin/fcgiwrap

# Give the socket a second to be created then open permissions
sleep 1
chmod 777 /var/run/fcgiwrap.socket

# Start Nginx
echo "Starting Nginx..."
nginx -g 'daemon off;'