# Instalação com Snap

> https://snapcraft.io/mosquitto

# Instalação do broker no linux (ubuntu/debian)

```
    sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
    sudo apt-get update
    sudo apt install mosquitto mosquitto-clients
```

# Instalação do broker no linux (centos 7)

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

# Instalação do broker no windows

> https://mosquitto.org/download/

# Requisitos

    Python ver >= 3.10
    MongoDB
    Poetry
    `pip install poetry`

# ENVIRONMENT (.env)

    É necessário criar o arquivo .env no dir raiz.

    ```
    USERNAME=<username>
    PASSWORD=<password>
    PORT=<port>
    BROKER=<broker ip address/domain>
    ```

# COMO USAR

1. Instalação de dependência:
   `poetry install`

2. Garantir que o broker esteja em execução.
3. Criar o arquivo .env com os dados adequados.
4. Executar um subscriber
   ex: `poetry run python3 subscriber.py`
5. Executar um publisher
   ex: `poetry run python3 publisher.py`
