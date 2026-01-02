
```bash
#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# ontocms-runtime — AENGA-compliant container runtime (Docker alternative)

set -e

IMAGE_NAME="ontocms/agent"
ROOTFS_DIR="/var/lib/machines/ontocms"
PROFILE="${ONTO_PROFILE:-Libra-Earth-Goat}"
PHASE="${ONTO_PHASE:-Slow}"

# 1. Проверка: нет ли запрещённых флагов (нарушение AENGA)
if echo "$*" | grep -E "(--privileged|--cap-add|--device)"; then
    echo "❌ AENGA VIOLATION: privileged mode forbidden"
    exit 1
fi

# 2. Создание rootfs (на основе минимального образа)
if [ ! -d "$ROOTFS_DIR" ]; then
    echo "📦 Initializing ontocms rootfs..."
    mkdir -p "$ROOTFS_DIR"
    # Используем podman или debootstrap — без Docker Hub
    if command -v podman >/dev/null; then
        podman pull --root "$ROOTFS_DIR" docker.io/library/debian:bookworm-slim
    else
        debootstrap --variant=minbase bookworm "$ROOTFS_DIR" http://deb.debian.org/debian/
    fi
fi

# 3. Копирование ontoCMS-бинарника (предполагается, что он уже собран)
if [ ! -f "$ROOTFS_DIR/usr/local/bin/ontocms-agent" ]; then
    cp "$(dirname "$0")/../../../target/release/ontocms-agent" "$ROOTFS_DIR/usr/local/bin/"
fi

# 4. Запись онтологического профиля в контейнер
cat > "$ROOTFS_DIR/etc/ontocms-profile" <<EOF
ONTO_PROFILE=$PROFILE
ONTO_PHASE=$PHASE
EOF

# 5. Запуск через systemd-nspawn (без привилегий)
exec systemd-nspawn \
    --directory="$ROOTFS_DIR" \
    --property=DeviceAllow=char-urandom r \
    --property=DeviceAllow=char-urandom rw \
    --capability=CAP_NET_BIND_SERVICE \
    --setenv=ONTO_PROFILE="$PROFILE" \
    --setenv=ONTO_PHASE="$PHASE" \
    /usr/local/bin/ontocms-agent
```

