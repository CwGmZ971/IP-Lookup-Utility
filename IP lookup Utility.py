"""
    VERSION 2.2.0
    LAST MODIFIED 10/03/2024
"""

# GUI Imports
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

# Allows multithreading
from threading import Thread

# Networking + misc libraries
from webbrowser import open as w_open
import public_ip
import ipaddress
import requests
import socket
import os


class IPLookupApp:
    """
    IP Lookup Application Main Class
    """
    def __init__(self):
        self.ver = "2.2.0"
        self.root = tk.Tk()
        self.root.title(f"IP Lookup Application ({self.ver})")
        self.root.geometry("450x230")
        self.root.resizable(False, False)

        self.icon_path = os.path.join(os.getcwd(), "Icon", "LOGO.ico")
        if os.path.exists(self.icon_path):
            self.root.iconbitmap(self.icon_path)
        else:
            self.icon_path = None

        self.ip_type_var = tk.IntVar(value=1)
        self.format_var = tk.IntVar(value=1)

        self.style = ttk.Style()
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the GUI elements
        :return: None
        """
        self.create_ip_type_frame()
        self.create_ip_entry_frame()
        self.create_website_entry_frame()
        self.create_format_frame()
        self.create_buttons_frame()

    def create_ip_type_frame(self):
        """
        Creates the frame for selecting IP type (IPv4 or IPv6)
        :return: None
        """
        ip_type_frame = ttk.Frame(self.root)
        ip_type_frame.pack(pady=10)
        ip_type_label = ttk.Label(ip_type_frame, text="IP Type:")
        ip_type_label.pack(side=tk.LEFT)
        ipv4_radio = ttk.Radiobutton(ip_type_frame, text="IPv4", variable=self.ip_type_var, value=1)
        ipv4_radio.pack(side=tk.LEFT)
        ipv6_radio = ttk.Radiobutton(ip_type_frame, text="IPv6", variable=self.ip_type_var, value=2)
        ipv6_radio.pack(side=tk.LEFT)

    def create_ip_entry_frame(self):
        """
        Creates the frame for entering IP address
        :return: None
        """
        ip_entry_frame = ttk.Frame(self.root)
        ip_entry_frame.pack(pady=10)
        ip_label = ttk.Label(ip_entry_frame, text="Enter IP Address:")
        ip_label.pack(side=tk.LEFT)
        self.ip_entry = ttk.Entry(ip_entry_frame)
        self.ip_entry.pack(side=tk.LEFT)

    def create_website_entry_frame(self):
        """
        Creates the frame for entering website URL
        :return: None
        """
        website_entry_frame = ttk.Frame(self.root)
        website_entry_frame.pack(pady=10)
        website_label = ttk.Label(website_entry_frame, text="Enter Website URL:")
        website_label.pack(side=tk.LEFT)
        self.website_entry = ttk.Entry(website_entry_frame)
        self.website_entry.pack(side=tk.LEFT)

    def create_format_frame(self):
        """
        Creates the frame for selecting IP format (User-friendly or Full)
        :return: None
        """
        format_frame = ttk.Frame(self.root)
        format_frame.pack(pady=10)
        format_label = ttk.Label(format_frame, text="Format:")
        format_label.pack(side=tk.LEFT)
        friendly_format_radio = ttk.Radiobutton(format_frame, text="User-friendly", variable=self.format_var, value=1)
        friendly_format_radio.pack(side=tk.LEFT)
        full_format_radio = ttk.Radiobutton(format_frame, text="Full", variable=self.format_var, value=2)
        full_format_radio.pack(side=tk.LEFT)

    def create_buttons_frame(self):
        """
        Creates the frame for buttons
        :return: None
        """
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=20)
        lookup_button = ttk.Button(buttons_frame, text="Lookup IP", command=self.ip_lookup)
        lookup_button.pack(side=tk.LEFT, padx=10)
        website_lookup_button = ttk.Button(buttons_frame, text="Website IP Lookup", command=self.website_ip_lookup)
        website_lookup_button.pack(side=tk.LEFT, padx=10)
        own_ip_button = ttk.Button(buttons_frame, text="Own IP Lookup", command=self.own_ip_lookup)
        own_ip_button.pack(side=tk.LEFT, padx=10)
        help_button = ttk.Button(buttons_frame, text="IP Format Help", command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=10)

    def ip_lookup(self):
        """
        Performs IP lookup based on the selected IP type and entered IP address
        :return: None
        """
        if self.internet():
            ip_type = self.ip_type_var.get()
            ip = self.ip_entry.get()
            self.ip_entry.delete(0, tk.END)
            if len(ip) == 0:
                messagebox.showerror("Error", "Nothing entered in IP input box")
                return
            elif ip_type == 1 and not self.is_valid_ip_address(ip, 1):
                messagebox.showerror("Error", "Invalid IPv4 address format. Please try again.")
                return
            elif ip_type == 2 and not self.is_valid_ip_address(ip, 2):
                messagebox.showerror("Error", "Invalid IPv6 address format. Please try again.")
                return

            response = self.get_ip_info(ip)
            self.display_ip_info(response)

    def website_ip_lookup(self):
        """
        Performs IP lookup for a given website URL
        :return: None
        """
        if self.internet():
            website_url = self.website_entry.get()
            self.website_entry.delete(0, tk.END)
            if len(website_url) == 0:
                messagebox.showerror("Error", "Nothing entered in website text box")
                return
            elif "." not in website_url or len(website_url) <= 3:
                messagebox.showerror("Error", "Website format is incorrect. Please try again.")
                return
            try:
                ip = socket.gethostbyname(website_url)
                response = self.get_ip_info(ip)
                self.display_ip_info(response)
            except socket.gaierror:
                messagebox.showerror("Error", "The website you entered doesn't exist.")

    def show_please_wait_window(self):
        """
        Show a 'Please Wait' window during IP lookup.
        :return: None
        """
        self.please_wait_window = tk.Toplevel(self.root)
        self.please_wait_window.title("Please Wait")
        self.please_wait_window.geometry("200x100")
        self.please_wait_window.resizable(False, False)
        if self.icon_path:
            self.please_wait_window.iconbitmap(self.icon_path)
        self.please_wait_label = ttk.Label(self.please_wait_window, text="Request sent. Please wait...")
        self.please_wait_label.pack(pady=20)

    def perform_own_ip_lookup(self):
        """
        Perform IP lookup for the user's own IP address.
        :return: None
        """
        self.show_please_wait_window()
        try:
            ip = public_ip.get()
            response = self.get_ip_info(ip)
            self.display_ip_info(response)
            self.please_wait_window.destroy()
        except (ValueError, IOError) as err:
            self.please_wait_window.destroy()
            messagebox.showerror("Error", str(err))

    def own_ip_lookup(self):
        """
        perform_own_ip_lookup executes on separate thread to keep the GUI running
        :return: None
        """
        if self.internet():
            Thread(target=self.perform_own_ip_lookup, daemon=True).start()

    @staticmethod
    def is_valid_ip_address(address: str, ip_type: int) -> bool:
        """
        Check if the given IP address is valid based on the IP type.
        :param address: IP address to check.
        :param ip_type: Type of IP address (1 for IPv4, 2 for IPv6).
        :return: True if the IP address is valid, False otherwise.
        """
        try:
            if ip_type == 1:
                ipaddress.IPv4Address(address)
            elif ip_type == 2:
                ipaddress.IPv6Address(address)
            return True
        except ipaddress.AddressValueError:
            return False

    @staticmethod
    def get_ip_info(ip: str) -> dict:
        """
        Retrieve IP information from API based on the given IP address.
        :param ip: IP address.
        :return: Dictionary containing IP information.
        """
        response = requests.get("http://ip-api.com/json/" + ip).json()
        return response

    @staticmethod
    def internet() -> bool:
        """
        Check for an active internet connection
        :return: boolean indicating whether the internet connection is active
        """
        try:
            response = requests.get("https://www.google.com")
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            messagebox.showerror("Error", "You are not connected to the internet.")
            return False

    @staticmethod
    def show_help():
        """
        Opens link to IP address Wikipedia page
        :return: None
        """
        w_open("https://en.wikipedia.org/wiki/IP_address")

    def display_ip_info(self, response: dict):
        """
        Display the IP information in a message box based on the selected format.
        :param response: Dictionary containing IP information.
        :return: None
        """
        if response['status'] == 'success':
            format_type = self.format_var.get()
            if format_type == 1:
                info = f"""Country: {response['country']}
                        \nRegion Name: {response['regionName']}
                        \nCity: {response['city']}
                        \nISP: {response['isp']}"""
                messagebox.showinfo(f"IP Lookup Application ({self.ver})", info)
            elif format_type == 2:
                response.pop('status', None)  # Remove status key/pair as it is no longer needed
                formatted_info = self.format_json(response)
                messagebox.showinfo(f"IP Lookup Application ({self.ver})", formatted_info)
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {response['message']}")

    @staticmethod
    def format_json(json_data: dict) -> str:
        """
        Formats JSON data into a human-readable string
        :param json_data: Dictionary containing IP information
        :return: Formatted JSON string
        """
        formatted_info = ""
        for key, value in json_data.items():
            formatted_info += f"{key}: {value}\n"
        return formatted_info

    def run(self):
        """
        Runs the IP Lookup application
        :return: None
        """
        if self.internet():
            self.root.mainloop()
        else:
            self.root.destroy()


if __name__ == "__main__":
    # Create an instance of the IPLookupApp class and run the application
    app = IPLookupApp()
    app.run()
