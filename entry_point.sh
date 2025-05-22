#!/bin/sh
echo "entry point stasting"
[[ -n $FEAST_PROJECT_NAME ]] && yq eval ".project = \"$FEAST_PROJECT_NAME\"" -i /app/feature_repo/feature_store.yaml
[[ -n $FEAST_REGISTRY_URL ]] && yq eval ".registry.path = \"$FEAST_REGISTRY_URL\"" -i /app/feature_repo/feature_store.yaml
[[ -n $DB_HOST ]] && yq eval ".online_store.host = \"$DB_HOST\"" -i /app/feature_repo/feature_store.yaml
[[ -n $DB_PORT ]] && yq eval ".online_store.port = \"$DB_PORT\"" -i /app/feature_repo/feature_store.yaml
[[ -n $DB_USER ]] && yq eval ".online_store.user = \"$DB_USER\"" -i /app/feature_repo/feature_store.yaml
[[ -n $DB_PASSWORD ]] && yq eval ".online_store.password = \"$DB_PASSWORD\"" -i /app/feature_repo/feature_store.yaml
[[ -n $DB_NAME ]] && yq eval ".online_store.database = \"$DB_NAME\"" -i /app/feature_repo/feature_store.yaml
cat /app/feature_repo/feature_store.yaml
echo "entry point ending"
