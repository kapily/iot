
How to set this up on Raspberry Pi:

Install rtl_433 by following instruction here:
https://github.com/merbanan/rtl_433


sudo vi /lib/systemd/system/temperature.service
sudo systemctl enable temperature

temperature.service:

```
[Unit]
Description=Temperature Monitor
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/Desktop/temperature.py
Restart=always

[Install]
WantedBy=multi-user.target

```

