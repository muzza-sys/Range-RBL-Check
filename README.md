# RBL IP Range Lookup with Discord Alerts

## Overview
A Python script that checks multiple IP ranges against popular Real-time Blackhole Lists (RBLs) to detect blacklisted IPs. If any IPs are blacklisted, the script sends a Discord webhook alert with the details.

## Features
- ✅ Check multiple IP ranges for blacklisted IPs
- 🔍 Query popular RBLs (Spamhaus, SpamCop, Barracuda, etc.)
- 🛡️ Rate-limited lookups to avoid getting blocked
- 📢 Discord webhook notifications for blacklisted IPs

## Prerequisites
- Python 3.x
- Install required Python packages:

```bash
pip install dnspython requests
```

## Usage
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/rbl-ip-range-lookup.git
   cd rbl-ip-range-lookup
   ```

2. **Configure the script:**
   - Edit `ip_ranges` in the script to specify your IP ranges.
   - Replace `'https://discord.com/api/webhooks/your_webhook_url_here'` with your Discord webhook URL.
   - Adjust `delay_seconds` for rate-limiting.

3. **Run the script:**
   ```bash
   python rbl_lookup.py
   ```

## Example Output
```
Checking range: 192.168.1.1 - 192.168.1.10
192.168.1.1 is clean.
192.168.1.2 is blacklisted in: zen.spamhaus.org, bl.spamcop.net
```

## Automate with Cron Job
Automate the script by adding it to cron:

```bash
crontab -e
```

Add this line to run the script daily at 2 AM:
```bash
0 2 * * * /usr/bin/python3 /path/to/rbl_lookup.py >> /var/log/rbl_lookup.log 2>&1
```

