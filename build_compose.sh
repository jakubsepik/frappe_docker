docker compose -p frappe -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml -f overrides/compose.https.yaml config > compose.my-custom.yaml
