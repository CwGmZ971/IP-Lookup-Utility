# IP Lookup Application

This program allows users to perform IP address lookups and retrieve information about IP addresses or websites. It provides options to select between IPv4 and IPv6 addresses, choose between user-friendly or full format for the results, and performs lookups for IP addresses and website URLs.

## Version Information
- **Version**: 2.1.8
- **Last Modified**: 01/02/2024

## Features
- Perform IP address lookups for both IPv4 and IPv6 addresses.
- Retrieve information about a website's IP address.
- Display IP information in either a user-friendly or full format.
- Capability to check the user's own IP address.
- Option to view help documentation about IP addresses.

## Dependencies
- `tkinter`: Python's standard GUI (Graphical User Interface) toolkit.
- `requests`: HTTP library for making requests.
- `public_ip`: Library to retrieve the user's public IP address.
- `ipaddress`: Library for working with IP addresses.
- `socket`: Provides access to the BSD socket interface.

## Usage
1. Select the IP type (IPv4 or IPv6).
2. Enter the IP address or website URL.
3. Choose the desired format for the results.
4. Click on the corresponding button:
    - **Lookup IP**: Perform IP lookup based on the selected IP type and entered IP address.
    - **Website IP Lookup**: Perform IP lookup for a given website URL.
    - **Own IP Lookup**: Check your own IP address.
    - **IP Format Help**: View help documentation about IP addresses.

## Important Note
- This application requires an internet connection to perform IP lookups.

For more information about IP addresses, please refer to the [IP Address Wikipedia page](https://en.wikipedia.org/wiki/IP_address).
