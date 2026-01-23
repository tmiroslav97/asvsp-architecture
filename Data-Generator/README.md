# Data-Generator App

## Running

### On Linux
1. Find your main network interface using `ifconfig`
1. Run `docker build`
1. Update `docker-compose.yml`
1. Run using `docker compose`

### On Windows
On Windows, there is no such thing as 'host' docker network, and you cannot sniff host traffic from within a container. Hence, it is advised for you to run the app natively on Windows:
1. Run `pip install -r requirements.txt`
1. Find your main network interface using `ipconfig`
1. Update `sniffer_app.py` with the identified interface
1. Run `python sniffer_app.py`
