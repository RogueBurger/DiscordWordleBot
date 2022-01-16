# Discord Wordle Bot

## Quick Start

Follow these steps to run a stateless instance of the Discord Wordle Bot.

### Install

```
$ pip install -r requirements.txt
```

### Configure

Copy `config.yaml.example` to `config.yaml` and fill in your Discord bot token.

### Run

```
$ python Main.py
```

## Advanced

### Persistence

If you would like the state of active games to persist across restarts, you can point the bot to an existing redis server or else use the included `docker` configuration to provision one locally.

If you already have a redis server running, just add its host and port to your chosen configuration file. For this example, assume the existing redis server is available at `redis.local:6379`:

```
# config.yaml

redis:
    enabled: true
    host: "redis.local"
    port: 6379
```

```.env
# .env

WORDLEBOT_REDIS__ENABLED="true"
WORDLEBOT_REDIS__HOST="redis.local"
WORDLEBOT_REDIS__PORT="6379"
```

### Docker

To use the included `docker` configuration, install `docker` and `docker-compose` and run:

```
$ docker-compose up -d --build
```

## Development

Developed in Python 3.9