"""
All utility functions (previously static methods) for IP Lookup Utility.py
"""

from webbrowser import open as w_open
import tkinter.messagebox as messagebox
import ipaddress
import requests
import json


def is_valid_ip_address(address: str, ip_type: int) -> bool:
    try:
        if ip_type == 1:
            ipaddress.IPv4Address(address)
        elif ip_type == 2:
            ipaddress.IPv6Address(address)
        return True
    except ipaddress.AddressValueError:
        return False


def get_ip_info(ip: str) -> dict:
    response = requests.get("http://ip-api.com/json/" + ip).json()
    return response


def internet() -> bool:
    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        messagebox.showerror("Error", "You are not connected to the internet.")
        return False


def show_help():
    w_open("https://en.wikipedia.org/wiki/IP_address")


def format_json(json_data: dict) -> str:
    formatted_info = ""
    for key, value in json_data.items():
        formatted_info += f"{key}: {value}\n"
    return formatted_info
