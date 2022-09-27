apk add jq
cat /data/acme.json | jq -r '.letsencrypt | .Certificates[] | .certificate' | base64 -d > /certs/cert.crt
cat /data/acme.json | jq -r '.letsencrypt | .Certificates[] | .key' | base64 -d > /certs/key.key