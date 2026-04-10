export APPS_JSON_BASE64=$(base64 -w 0 apps.json)
docker build \
  --build-arg=APPS_JSON_BASE64=$APPS_JSON_BASE64 \
  --tag=custom:16 \
  --file=images/layered/Containerfile .
