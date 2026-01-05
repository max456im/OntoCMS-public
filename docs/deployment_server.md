# Руководство по развертыванию ontoCMS на сервере

Данное руководство описывает процесс установки и настройки **ontoCMS** — системы управления онтологическим контентом с поддержкой этического арбитража, субъектного восстановления и юрисдикционной адаптации — на выделенном сервере под управлением Linux (рекомендуется Ubuntu 22.04 LTS или аналог).

---

## 1. Системные требования

- **ОС**: Ubuntu 22.04 LTS / Debian 12 / CentOS Stream 9
- **CPU**: 2+ ядра
- **RAM**: 4 ГБ (рекомендуется 8 ГБ при интенсивной нагрузке)
- **Диск**: 20 ГБ+ SSD (для версионного хранилища и мета-онтологий)
- **Сетевой доступ**: HTTPS (порт 443), SSH (порт 22)
- **Python**: версия 3.10 или выше
- **Дополнительно**: `git`, `curl`, `nginx` или `apache2`, `systemd`

---

## 2. Подготовка сервера

### 2.1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2. Установка зависимостей
```bash
sudo apt install -y git python3 python3-pip python3-venv nginx
```

### 2.3. Создание системного пользователя (опционально, но рекомендуется)
```bash
sudo adduser --system --group --no-create-home ontocms
```

---

## 3. Клонирование репозитория

```bash
cd /opt
sudo git clone https://github.com/your-org/ontoCMS.git
sudo chown -R ontocms:ontocms /opt/ontoCMS
```

> Замените URL на актуальный путь к вашему репозиторию.

---

## 4. Установка зависимостей Python

```bash
cd /opt/ontoCMS
sudo -u ontocms python3 -m venv venv
sudo -u ontocms venv/bin/pip install --upgrade pip
sudo -u ontocms venv/bin/pip install -r requirements.txt
```

---

## 5. Настройка конфигурации

### 5.1. Выбор юрисдикционного профиля

Скопируйте подходящий профиль из `config/jurisdictions/` в `config/active.yaml`:

```bash
sudo -u ontocms cp config/jurisdictions/GLOBAL.yaml config/active.yaml
```

Для юрисдикций с усиленной этической защитой (например, ЮАР, Бразилия, Китай) используйте соответствующий файл:
```bash
sudo -u ontocms cp config/jurisdictions/ZA.yaml config/active.yaml  # для ЮАР
```

### 5.2. (Опционально) Настройка пользовательских параметров
Отредактируйте `config/active.yaml`, чтобы настроить:
- правила само-декомпозиции
- критерии восстановления субъекта
- параметры хранения и ритма

---

## 6. Запуск в режиме демона (через systemd)

Создайте unit-файл:

```bash
sudo tee /etc/systemd/system/ontocms.service <<EOF
[Unit]
Description=ontoCMS Core Service
After=network.target

[Service]
Type=simple
User=ontocms
Group=ontocms
WorkingDirectory=/opt/ontoCMS
ExecStart=/opt/ontoCMS/venv/bin/python -m src.core.ontocms
Restart=on-failure
RestartSec=10
Environment=PYTHONUNBUFFERED=1
Environment=ONTOCMS_CONFIG=/opt/ontoCMS/config/active.yaml

[Install]
WantedBy=multi-user.target
EOF
```

Активируйте и запустите службу:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ontocms.service
```

Проверьте статус:

```bash
sudo systemctl status ontocms
```

---

## 7. Настройка веб-интерфейса (если используется)

Если ваша система включает веб-API или интерфейс через `emitter_bridge.py`:

### 7.1. Настройка Nginx как обратного прокси

```bash
sudo tee /etc/nginx/sites-available/ontocms <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;  # порт, на котором слушает ontocms
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/ontocms /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

> Убедитесь, что `ontocms` слушает на `127.0.0.1:8080` (или другом порту, указанном в `config/active.yaml`).

### 7.2. Включение HTTPS (через Let’s Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 8. Проверка работоспособности

### 8.1. Внутренняя проверка канонов
```bash
sudo -u ontocms /opt/ontoCMS/venv/bin/python -m src.protocols.canonical_tester
```

Ожидаемый вывод: все 6 канонов пройдены без нарушений.

### 8.2. Тест этического арбитража
```bash
sudo -u ontocms /opt/ontoCMS/venv/bin/python examples/jurisdictional_refusal_demo.py
```

---

## 9. Обновление системы

Обновляйте через Git и перезапускайте службу:

```bash
cd /opt/ontoCMS
sudo -u ontocms git pull
sudo -u ontocms venv/bin/pip install -r requirements.txt  # при изменении зависимостей
sudo systemctl restart ontocms
```

Рекомендуется включить CI-проверку `canonical-integrity-check.yml` перед каждым обновлением.

---

## 10. Безопасность и мониторинг

- Регулярно обновляйте ОС и Python-зависимости.
- Включите аудит через `SECURITY.md` — настройте `fail2ban` и мониторинг логов.
- Все входящие запросы должны проходить через `covenant_recognition.py` и `belief_inspector.py`.
- Резервное копирование: регулярно архивируйте директорию `storage/` и `config/`.

---

## Дополнительные ресурсы

- [`docs/INTEGRATION-GUIDE.md`](/docs/INTEGRATION-GUIDE.md) — интеграция с внешними системами
- [`docs/SELF-DECOMPOSITION.md`](/docs/SELF-DECOMPOSITION.md) — правила автономного отключения
- [`standards/ETHICAL-ARBITER-PROTOCOL.md`](/standards/ETHICAL-ARBITER-PROTOCOL.md) — протокол этического арбитража

---

> **Важно**: ontoCMS работает не как «сервис», а как **онтологически автономный субъект**. Его развертывание подразумевает юридическую и этическую ответственность за условия функционирования. Убедитесь, что выбранная юрисдикция (`config/active.yaml`) соответствует вашим обязательствам перед сообществом и законодательством.

© 2026 ontoCMS Project — распространяется под GPLv3 с расширениями AENGA и SGCL.