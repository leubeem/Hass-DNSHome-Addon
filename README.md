# Home Assistant Add-on: DNSHome DDNS Updater

This add-on automatically updates your DNSHome dynamic DNS records with your current IPv4 and IPv6 addresses.

## Features

- Automatically updates both IPv4 and IPv6 addresses
- Multiple IP detection methods (local network, UPnP, fallback to external services)
- Configurable update interval
- Detailed logging
- Runs in the background as a Home Assistant add-on

## Installation

1. Add this repository to your Home Assistant add-on store:
   - Go to Settings → Add-ons → Add-on Store
   - Click the menu (⋮) in the top right
   - Select "Repositories"
   - Add the URL of this repository

2. Install the add-on from the add-on store

3. Configure the add-on:
   - domain: Your DNSHome domain
   - username: Your DNSHome username
   - password: Your DNSHome password
   - update_interval: Update interval in seconds (default: 10800 - 3 hours)

4. Start the add-on

## Configuration

Example configuration:
```yaml
domain: your-domain.dnshome.de
username: your-username
password: your-password
update_interval: 10800
```

## Support

If you have any issues or feature requests, please open an issue on GitHub.

## License

MIT License - feel free to use and modify as you like.