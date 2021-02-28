#!/usr/bin/env bash

# Renew the certificate
certbot renew --force-renewal --tls-sni-01-port=8888

# Concatenate new cert files, with less output (avoiding the use tee and its output to stdout)
bash -c "cat /etc/letsencrypt/live/hacktheplanet.mywire.org/fullchain.pem /etc/letsencrypt/live/hacktheplanet.mywire.org/privkey.pem > /etc/ssl/hckthplnt/hckthplnt.pem"

# Reload  HAProxy
systemctl reload haproxy
