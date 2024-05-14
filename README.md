# IP Lookup Application

This program enables users to perform IP address lookups and retrieve information about IP addresses or websites. It offers options to choose between IPv4 and IPv6 addresses, select user-friendly or full format for the results, and perform lookups for IP addresses and website URLs. Additionally, it features caching of lookup results and the option to save logs.

For more information about IP addresses, please refer to the [IP Address Wikipedia page](https://en.wikipedia.org/wiki/IP_address).

## Features
- Perform IP address lookups for both IPv4 and IPv6 addresses.
- Retrieve information about a website's IP address.
- Display IP information in either a user-friendly or full format.
- Capability to check the user's own IP address.
- Option to view help documentation about IP addresses.

#### As of v2.2.2:
- **Caching:** Lookup results are cached to improve performance.
- **Log Saving:** Option to save logs.

## PIP Dependencies (To install, open cmd and type `pip install <package-name>`)
- `public_ip`: Library to retrieve the user's public IP address. [GitHub Link](https://github.com/vterron/public-ip)
- `requests`: HTTP library for making requests. [GitHub Link](https://github.com/psf/requests)

## Usage
![Screenshot of application](README_Images/GUI_Image.png)
1. Select the IP type (IPv4 or IPv6).
2. Enter the IP address or website URL.
3. Choose the desired format for the results.
4. Click on the corresponding button:
    - **Lookup IP**: Perform IP lookup based on the selected IP type and entered IP address.
    - **Website IP Lookup**: Perform IP lookup for a given website URL.
    - **Own IP Lookup**: Check your own IP address.
    - **IP Format Help**: View help documentation about IP addresses.

## API Usage
This application relies on the [ip-api.com](http://ip-api.com) API to retrieve information about IP addresses. Please note the following:
- **API Limitations:** The usage of the API may be subject to rate limits or other restrictions imposed by ip-api.com. Please refer to their documentation for more details.
- **Internet Connection:** An active internet connection is required for the application to access the API and retrieve IP information.

## Executable Version

An executable version of the application, created with PyInstaller, is available for users who prefer not to run the Python script directly. You can download the zip file from the following link:

[Download IP Lookup Application (Executable)](exe_version/)

After downloading, extract the zip file's contents and run the executable file to use the application.

## PyInstaller
For more information about PyInstaller, please visit the [PyInstaller GitHub repository](https://github.com/pyinstaller/pyinstaller).

# License

