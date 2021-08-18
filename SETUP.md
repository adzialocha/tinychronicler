# Setup Raspberry Pi 4

## Preparation

1. Install a fresh version of *Debian with Raspberry Pi Deskop* on your Raspberry Pi first: https://www.raspberrypi.org/software/
2. Connect your Raspberry Pi to a screen, keyboard and mouse
3. Boot from your new installation

## 1. Enable SSH server

Follow steps under https://www.raspberrypi.org/documentation/computers/remote-access.html#enabling-the-server

## 2. Install Python

1. Install *pyenv* first by running:

    ```bash
    curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
    ```

2. Add the following lines to your `.profile` file:

    ```env
    export PATH="~/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```

3. Install Python version 3.8

    ```bash
    # Install required Python version and make it the default
    pyenv install 3.8.11
    pyenv global 3.8.11
    ```

## 3. Install Tiny Chronicler

Open a new terminal and run the following commands:

```bash
# Install dependencies for pillow
sudo apt-get install libjpeg-dev

# Install dependencies required to install llvmlite
sudo apt-get install llvm-9

# Install dependencies required to build scipy
sudo apt-get install gfortran libopenblas-dev liblapack-dev libatlas3-base libgfortran5

# Install Pure Data
sudo apt-get install puredata

# Clone tinychronicler repository
git clone https://github.com/adzialocha/tinychronicler
cd tinychronicler

# Install all dependencies, this might take a long time ..
LLVM_CONFIG=llvm-config-9 poetry install
```

## 4. Install HiFi Berry

Related link: https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/

Remove the driver for the onboard sound from `/boot/config.txt` if it exists. Remove the line:

```
dtparam=audio=on
```

## 5. Start Tiny Chronicler when Pi boots

Run `crontab -e` and add the following line:

```
@reboot sleep 10; /home/pi/tinychronicler/scripts/start.sh
```

## 6. Setup WiFi Access Point and local domain

1. Install required services

    ```bash
    sudo apt-get install hostapd dnsmasq
    ```

2. Configure DNS and DHCP server in `/etc/dnsmasq.conf`

    Related link: https://thinkingeek.com/2020/06/06/local-domain-and-dhcp-with-dnsmasq/

    ```env
    # If you want dnsmasq to listen for DHCP and DNS requests only on
    # specified interfaces (and the loopback) give the name of the
    # interface (eg eth0) here.
    interface=wlan0
    # If you want dnsmasq to provide only DNS service on an interface,
    # configure it as shown above, and then use the following line to
    # disable DHCP and TFTP on it.
    no-dhcp-interface=eth0
    # DNS servers
    server=8.8.8.8
    server=8.8.4.4
    # Option domain-needed is to make sure we don\u2019t forward to DNS servers plain
    # names without a domain separator.
    domain-needed
    # Don't read /etc/resolv.conf or any other file to get the forwarding files.
    no-resolv
    # Uncomment this to enable the integrated DHCP server, you need to supply the
    # range of addresses available for lease and optionally a lease time. If you
    # have more than one network, you will need to repeat this for each network on
    # which you want to supply DHCP service.
    dhcp-range=192.168.123.10,192.168.123.99,255.255.255.0,24h
    # Override the default route supplied by dnsmasq, which assumes the router is
    # the same machine as the one running dnsmasq.
    dhcp-option=option:dns-server,192.168.123.123
    # It does the following things.
    # 1) Allows DHCP hosts to have fully qualified domain names, as long as the
    #    domain part matches this setting.
    # 2) Sets the "domain" DHCP option thereby potentially setting the domain of
    #    all systems configured by DHCP
    # 3) Provides the domain part for "expand-hosts"
    domain=local
    # Add local-only domains here, queries in these domains are answered from
    # /etc/hosts or DHCP only.
    local=/local/
    ```

3. Add local domain in `/etc/hosts`

    ```env
    192.168.123.123 tinychronicler.local tinychronicler
    ```

4. Setup WiFi Access Point in `/etc/hostapd/hostapd.conf`

    Read https://www.elektronik-kompendium.de/sites/raspberry-pi/2002171.htm

    ```env
    interface=wlan0

    hw_mode=g
    channel=7
    wmm_enabled=0
    country_code=DE
    macaddr_acl=0
    ieee80211n=1
    ieee80211d=1
    ignore_broadcast_ssid=0

    auth_algs=1
    wpa=2
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP
    ssid=tinychronicler
    wpa_passphrase=tinychronicler
    ```

5. Set `hostapd` setting to default in `/etc/default/hostapd`

    ```env
    RUN_DAEMON=yes
    DAEMON_CONF="/etc/hostapd/hostapd.conf"
    ```

6. Give Pi a static IP address in `/etc/dhcpcd.conf`

    ```env
    interface wlan0
    static ip_address=192.168.123.123/24
    nohook wpa_supplicant
    ```

7. Configure services

    ```bash
    sudo systemctl unmask hostapd
    sudo systemctl start hostapd
    sudo systemctl enable hostapd
    sudo systemctl enable dnsmasq
    ```

## 7. Reboot!

```bash
sudo reboot now
```

---

## Good to know

```bash
# Kill tmux session running tinychronicler
tmux kill-session -t tc

# Start session again
/home/pi/tinychronicler/scripts/start.sh

# Inspect current session (for example via ssh)
tmux a -t tc
```
