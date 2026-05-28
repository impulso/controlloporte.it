# Controllo Porte

[controlloporte.it](https://controlloporte.it) is a web tool for checking whether a TCP port is reachable from the outside on an IP address or domain name.

The project includes:

- a static frontend served by Nginx;
- a Python API backend built with Litestar;
- JSON endpoints for checking one or more TCP ports;
- support for checking the visitor's public IP address through the `me` alias;
- Italian SEO content and informational pages;
- a GDPR-conscious setup with local assets and no third-party tracking resources in the frontend;
- Docker configuration for development and production.

## Project Origin

This project is based on [dsgnr/portchecker.io](https://github.com/dsgnr/portchecker.io).

The main changes in this version include Italian localization, `controlloporte.it` branding, informational pages, privacy policy, GDPR-conscious frontend changes, updated API documentation, open-port latency support, and deployment-specific configuration.

## API Documentation

Public API documentation is available at:

- [https://controlloporte.it/docs](https://controlloporte.it/docs)
- [https://controlloporte.it/.well-known/openapi.json](https://controlloporte.it/.well-known/openapi.json)

POST example:

```bash
curl -sS \
  -H "Content-Type: application/json" \
  -d '{"host":"example.com","ports":[80,443]}' \
  https://controlloporte.it/api/query
```

JSON GET example:

```bash
curl -sS https://controlloporte.it/api/check/example.com/443
```

To check the visitor's public IP address, use `me`:

```bash
curl -sS \
  -H "Content-Type: application/json" \
  -d '{"host":"me","ports":[443]}' \
  https://controlloporte.it/api/query
```

## Local Development

### Frontend

Requires Node.js 25 or newer and Yarn classic.

```bash
cd frontend/web
yarn install
yarn dev
```

The frontend is exposed at:

```text
http://0.0.0.0:8080
```

### Backend

Requires Python 3.13 and Poetry.

```bash
cd backend/api
poetry install
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API is exposed at:

```text
http://0.0.0.0:8000
```

### Development With Docker

```bash
docker compose -f docker-compose-dev.yml up --build
```

## Production

```bash
docker compose up -d --build
```

The production configuration exposes:

- frontend on `127.0.0.1:8080`;
- API on `127.0.0.1:8000`;
- public reverse proxy through Caddy/Nginx.

### Permanent scanner bans

Nginx rejects common secret/config probes such as `/.env`, `/.git/config`, `wp-config.php`
backups, exposed logs, SQL dumps and CI files with status `403`, and writes them to:

```text
/var/log/controlloporte/nginx/security-scan.log
```

Install the included fail2ban jail on the host to ban the caller at firewall level on the
first matching request:

```bash
sudo cp deploy/fail2ban/filter.d/controlloporte-security-scan.conf /etc/fail2ban/filter.d/
sudo cp deploy/fail2ban/jail.d/controlloporte-security-scan.local /etc/fail2ban/jail.d/
sudo systemctl reload fail2ban
```

The jail is named `cp-scan` and uses `bantime = -1`, so bans are permanent until manually removed.
On the production AlmaLinux host it uses `firewallcmd-allports`, matching the active
firewalld firewall.

## Environment Variables

### Frontend

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `API_URL` | No | `http://api:8000` | Internal API service URL. |
| `DEFAULT_HOST` | No | empty | Optional host value prefilled in the form. |
| `DEFAULT_PORT` | No | `443` | Optional port value prefilled in the form. |

### API

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `ALLOW_PRIVATE` | No | `False` | Allows checks against private/special IPv4 ranges. |

## License

See [LICENSE](LICENSE).

This project keeps the license of the original project it derives from.
