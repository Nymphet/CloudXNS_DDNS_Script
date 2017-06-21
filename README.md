# CloudXNS_DDNS_Script

This very simple script is used to set up CloudXNS DDNS automatically with local IPv4 & IPv6 addresses.

Since the official API doesn't support IPv6 DDNS, is was implemented with some workarounds.

There is a "ipv6_addr_starts_with" field in the configuration section, it is used to select which IPv6 address to use when multiple addresses are available. If no address is prefered, just set it to an empty string.
