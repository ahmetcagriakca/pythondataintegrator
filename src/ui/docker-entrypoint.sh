#!/bin/sh -eu
echo "starting docker entrypoint" >&1
/var/cache/nginx/generate_config_js.sh >/usr/share/nginx/html/env-config.js
nginx -g "daemon off;"
echo "nginx started" >&1