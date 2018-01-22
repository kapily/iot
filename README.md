
How to set this up on Raspberry Pi:

Install rtl_433 by following instruction here:
https://github.com/merbanan/rtl_433

Hardware:
I bought these devices from Amazon
AcuRite 06002M Wireless Temperature and Humidity Sensor (same as 592TX)
https://www.amazon.com/gp/product/B00T0K8NXC/

RTL-SDR Blog R820T2 RTL2832U 1PPM TCXO SMA Software Defined Radio with 2x Telescopic Antennas
https://www.amazon.com/gp/product/B011HVUEME





```
sudo vi /lib/systemd/system/temperature.service
sudo systemctl enable temperature
```

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

