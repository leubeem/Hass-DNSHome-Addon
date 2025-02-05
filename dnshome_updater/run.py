#!/usr/bin/env python3
import os
import time
import requests
import json
import logging
import socket
import netifaces
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DNSHomeUpdater:
    def __init__(self):
        self.config = self._load_config()
        self.domain = self.config['domain']
        self.username = self.config['username']
        self.password = self.config['password']
        self.update_interval = self.config['update_interval']
        self.update_url = "https://www.dnshome.de/dyndns.php"
        self.last_ipv4 = None
        self.last_ipv6 = None

    def _load_config(self):
        """Load the add-on configuration."""
        with open('/data/options.json') as config_file:
            return json.load(config_file)

    def get_ipv4_from_interface(self):
        """Get IPv4 address from network interface."""
        try:
            interfaces = netifaces.interfaces()

            for interface in interfaces:
                if interface.startswith('lo'):
                    continue

                addrs = netifaces.ifaddresses(interface)

                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if not (ip.startswith('10.') or
                                ip.startswith('172.16.') or
                                ip.startswith('192.168.')):
                            logger.debug(f"Found public IPv4 {ip} on interface {interface}")
                            return ip
            return None
        except Exception as e:
            logger.error(f"Error getting IPv4 from interfaces: {e}")
            return None

    def get_ipv6_from_interface(self):
        """Get IPv6 address from network interface."""
        try:
            interfaces = netifaces.interfaces()

            for interface in interfaces:
                if interface.startswith('lo'):
                    # Make log entry for loopback interface
                    logger.debug(f"Skipping loopback interface {interface}")
                    continue

                addrs = netifaces.ifaddresses(interface)

                if netifaces.AF_INET6 in addrs:
                    for addr in addrs[netifaces.AF_INET6]:
                        ip = addr['addr'].split('%')[0]  # Remove scope id if present
                        # Skip link-local addresses
                        if not (ip.startswith('fe80:') or ip.startswith('::1')):
                            logger.debug(f"Found public IPv6 {ip} on interface {interface}")
                            return ip
                # If no global IPv6 address found, make error log
                else:
                    logger.error(f"No global IPv6 address found on interface {interface}")
            return None
        except Exception as e:
            logger.error(f"Error getting IPv6 from interfaces: {e}")
            return None

    def get_ips_from_internet(self):
        """Fallback method: Get current public IPv4 and IPv6 addresses from internet services."""
        ipv4 = None
        ipv6 = None

        try:
            # Get IPv4
            response = requests.get('https://api.ipify.org?format=json')
            ipv4 = response.json()['ip']
        except Exception as e:
            logger.error(f"Error getting IPv4 from internet service: {e}")

        try:
            # Get IPv6
            response = requests.get('https://api6.ipify.org?format=json')
            ipv6 = response.json()['ip']
        except Exception as e:
            logger.error(f"Error getting IPv6 from internet service: {e}")

        return ipv4, ipv6

    def get_current_ips(self):
        """Try multiple methods to get both IPv4 and IPv6 addresses."""
        # Try local methods first
        ipv4 = self.get_ipv4_from_interface()
        ipv6 = self.get_ipv6_from_interface()

        # If either address is missing, try internet services
        if not ipv4 or not ipv6:
            fallback_ipv4, fallback_ipv6 = self.get_ips_from_internet()
            ipv4 = ipv4 or fallback_ipv4
            ipv6 = ipv6 or fallback_ipv6

        return ipv4, ipv6

    def update_dns(self, ipv4, ipv6):
        """Update DNSHome DDNS record with both IPv4 and IPv6."""
        try:
            # Basic authentication through URL parameters
            params = {
                'ip': ipv4 if ipv4 else '',
                'ip6': ipv6 if ipv6 else '',
                'username': self.username,
                'password': self.password,
            }

            response = requests.get(self.update_url, params=params)

            if response.status_code == 200 and "good" in response.text.lower():
                logger.info(f"{datetime.now()} - Successfully updated DNS records for {self.domain}")
                logger.info(f"IPv4: {ipv4}, IPv6: {ipv6}")
                self.last_ipv4 = ipv4
                self.last_ipv6 = ipv6
                return True
            else:
                logger.error(f"{datetime.now()} - Failed to update DNS records: {response.text}")
                return False

        except Exception as e:
            logger.error(f"{datetime.now()} - Error updating DNS records: {e}")
            return False

    def run(self):
        """Main loop to periodically update DNS."""
        logger.info(f"Starting DNSHome updater for domain {self.domain}")
        logger.info(f"Update interval set to {self.update_interval} seconds ({self.update_interval / 3600} hours)")

        while True:
            current_ipv4, current_ipv6 = self.get_current_ips()

            if ((current_ipv4 and current_ipv4 != self.last_ipv4) or
                    (current_ipv6 and current_ipv6 != self.last_ipv6)):
                self.update_dns(current_ipv4, current_ipv6)
            else:
                logger.debug(f"{datetime.now()} - No IP changes detected")

            time.sleep(self.update_interval)


if __name__ == "__main__":
    updater = DNSHomeUpdater()
    updater.run()