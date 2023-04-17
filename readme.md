# Instalação do Eclipse Mosquitto Brocker

## Instalação com Snap

> https://snapcraft.io/mosquitto

## Instalação do broker no linux (ubuntu/debian)

```
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt install mosquitto mosquitto-clients
```

## Instalação do broker no linux (centos 7)

```
yum -y install epel-release
yum -y install mosquitto
sed -i
pid_file: /var/run/mosquitto.pid
conf_file: /etc/mosquitto/mosquitto.conf
systemctl start mosquitto
systemctl enable mosquitto
firewall-cmd --permanent --add-port=1883/tcp
firewall-cmd --reload
```

## Instalação do broker no windows

> https://mosquitto.org/download/

## Teste

```
mosquitto_sub -h "localhost" -t "topic" -v
mosquitto_pub -h "localhost" -t "topic" -m "message"
```

# Configuração do Mosquitto

Adição de usuário e senha

```
mosquitto_passwd -c /etc/mosquitto/passwordfile nome_usuario
```

Arquivo mosquitto.conf

```
listener 1883
protocol mqtt
socket_domain ipv4
allow_anonymous false
password_file /etc/mosquitto/passwordfile
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
include_dir /etc/mosquitto/conf.d
connection_messages true
log_timestamp true
log_type error
log_type warning
```

# Requisitos

[Python ver >= 3.10](https://www.python.org/downloads/release/python-31010/)

[MongoDB](https://www.mongodb.com/try/download/community)

[Poetry](https://python-poetry.org/)

`pip install poetry`

# ENVIRONMENT (.env)

É necessário criar o arquivo .env no dir raiz.

```
USERNAME=<username>
PASSWORD=<password>
PORT=<port>
BROKER=<broker ip address/domain>
MONGO_HOST=<ip mongodb*>
MONGO_PORT=<porta mongodb*>
```

# COMO USAR

1. Instalação de dependência: `poetry install`
2. Garantir que o broker esteja em execução.
3. Criar o arquivo .env com os dados adequados.
4. Executar um subscriber, ex.: `poetry run python3 subscriber.py`
5. Executar um publisher, ex.: `poetry run python3 publisher.py`
