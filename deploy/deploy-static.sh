#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:?Set REMOTE_HOST to the deployment host.}"
REMOTE_USER="${REMOTE_USER:?Set REMOTE_USER to the deployment user.}"
REMOTE_PATH="${REMOTE_PATH:-/opt/portchecker.io}"
WEB_CONTAINER="${WEB_CONTAINER:-web}"

SSH=(ssh "$REMOTE_USER@$REMOTE_HOST")
SCP=(scp)

if [[ -n "${SSHPASS:-}" ]]; then
    SSH=(sshpass -p "$SSHPASS" ssh "$REMOTE_USER@$REMOTE_HOST")
    SCP=(sshpass -p "$SSHPASS" scp)
fi

tmp_archive="$(mktemp -t controlloporte-assets.XXXXXX.tar)"
trap 'rm -f "$tmp_archive"' EXIT

COPYFILE_DISABLE=1 tar \
    --format ustar \
    --exclude '._*' \
    --exclude '.DS_Store' \
    -C frontend/web/src/assets \
    -cf "$tmp_archive" .

"${SSH[@]}" "mkdir -p '$REMOTE_PATH/frontend/web/src/assets'"
"${SCP[@]}" "$tmp_archive" "$REMOTE_USER@$REMOTE_HOST:/tmp/controlloporte-assets.tar"
"${SSH[@]}" "find '$REMOTE_PATH/frontend/web/src/assets' \( -name '._*' -o -name '.DS_Store' \) -delete && tar -C '$REMOTE_PATH/frontend/web/src/assets' -xf /tmp/controlloporte-assets.tar && rm -f /tmp/controlloporte-assets.tar"
"${SSH[@]}" "docker cp '$REMOTE_PATH/frontend/web/src/assets/.' '$WEB_CONTAINER:/usr/share/nginx/html/'"
"${SSH[@]}" "docker exec '$WEB_CONTAINER' find /usr/share/nginx/html \( -name '._*' -o -name '.DS_Store' \) -delete"
"${SSH[@]}" "docker exec '$WEB_CONTAINER' nginx -s reload"
