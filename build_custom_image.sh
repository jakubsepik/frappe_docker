export APPS_JSON_BASE64=$(base64 -w 0 apps.json)
docker build \
 --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
 --build-arg=FRAPPE_BRANCH=version-15 \
 --build-arg=APPS_JSON_BASE64=$APPS_JSON_BASE64 \
 --tag=custom:15 \
 --file=images/layered/Containerfile .