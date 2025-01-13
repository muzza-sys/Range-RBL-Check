import ipaddress
import dns.resolver
import time
import requests

def send_discord_alert(webhook_url, ip, rbls):
    message = {
        "content": f"🚨 **Alert:** IP `{ip}` is blacklisted in: {', '.join(rbls)}"
    }
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code != 204:
            print(f"Failed to send Discord alert for {ip}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord alert: {e}")

def rbl_lookup(ip, rbls, delay):
    reversed_ip = '.'.join(reversed(ip.split('.')))
    blacklisted = []
    for rbl in rbls:
        query = f"{reversed_ip}.{rbl}"
        try:
            dns.resolver.resolve(query, 'A')
            blacklisted.append(rbl)
        except dns.resolver.NXDOMAIN:
            continue
        except dns.resolver.Timeout:
            print(f"Timeout querying {query}")
        except dns.resolver.NoAnswer:
            continue
        time.sleep(delay)  # Rate limiting between RBL queries
    return blacklisted

def check_ip_range(start_ip, end_ip, rbls, delay, webhook_url):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    for ip_int in range(int(start), int(end) + 1):
        ip = str(ipaddress.IPv4Address(ip_int))
        blacklisted_rbls = rbl_lookup(ip, rbls, delay)
        if blacklisted_rbls:
            print(f"{ip} is blacklisted in: {', '.join(blacklisted_rbls)}")
            send_discord_alert(webhook_url, ip, blacklisted_rbls)
        else:
            print(f"{ip} is clean.")
        time.sleep(delay)  # Rate limiting between IPs

def check_multiple_ip_ranges(ip_ranges, rbls, delay, webhook_url):
    for start_ip, end_ip in ip_ranges:
        print(f"\nChecking range: {start_ip} - {end_ip}")
        check_ip_range(start_ip, end_ip, rbls, delay, webhook_url)

if __name__ == "__main__":
    rbls = [
        'zen.spamhaus.org',
        'bl.spamcop.net',
        'b.barracudacentral.org',
        'dnsbl.sorbs.net',
        'psbl.surriel.com'
    ]

    # Example IP ranges to check
    ip_ranges = [
        ('192.168.1.1', '192.168.1.10'),
        ('10.0.0.1', '10.0.0.5')
    ]

    # Set delay in seconds to prevent getting blocked
    delay_seconds = 2

    # Discord Webhook URL
    discord_webhook_url = 'https://discord.com/api/webhooks/your_webhook_url_here'

    check_multiple_ip_ranges(ip_ranges, rbls, delay_seconds, discord_webhook_url)