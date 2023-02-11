# Instalação com Snap

    https://snapcraft.io/mosquitto

# Instalação do broker no linux (ubuntu/debian)

    sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
    sudo apt-get update
    sudo apt install mosquitto mosquitto-clients

# Instalação do broker no linux (centos 7)

    yum -y install epel-release
    yum -y install mosquitto
    sed -i
    pid_file: /var/run/mosquitto.pid
    conf_file: /etc/mosquitto/mosquitto.conf
    systemctl start mosquitto
    systemctl enable mosquitto
    firewall-cmd --permanent --add-port=1883/tcp
    firewall-cmd --reload

# Instalação do broker no windows

    https://mosquitto.org/download/
