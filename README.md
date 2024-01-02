## RSI s.1

---
### Docker
```bash
docker build -t rsi .
docker run -d rsi
```

### Service

Create service in `/etc/systemd/system/`

```bash
sudo nano /etc/systemd/system/rsi.service
```

#### rsi.service
```
[Unit]
Description=Py script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/rsi/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Run
```bash
sudo systemctl start rsi.service
sudo systemctl enable rsi.service
```

### Logs

```bash
journalctl -u rsi.service
```