## RSI s.1

---
### Docker
```bash
docker build -t rsi .
docker run -d rsi
```

### Create .env
```
SYMBOLS_FILE_PATH=/root/rsi.s1/data/symbols_v2.txt
```

### Logs

```bash
systemctl status systemd-journald
```

Edit `sudo nano /etc/systemd/journald.conf`

```
[Journal]
Storage=persistent
```
Restart
```bash
sudo systemctl restart systemd-journald
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
Environment="SYMBOLS_FILE_PATH=/root/rsi.s1/data/symbols_v2.txt"
ExecStart=/root/rsi.s1/.venv/bin/python3 /root/rsi.s1/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Run
```bash
sudo systemctl start rsi.service
sudo systemctl enable rsi.service
```

### Status
```bash
sudo systemctl status rsi.service
```

### Restart
```bash
sudo systemctl restart rsi.service
```

### Logs

```bash
journalctl -u rsi.service
```