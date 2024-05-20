# GUI Imports
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

# Allows multithreading
from threading import Thread

# Networking + misc libraries
from webbrowser import open as w_open
from appdirs import user_data_dir
from platform import python_version
import public_ip
import requests
import ipaddress
import atexit
import json
import time
import socket
import os


class IPLookupApp:
    def __init__(self):
        self.cache = {}
        self.ver = "2.4.1"
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
        self.save_log_var = tk.BooleanVar(value=False)

        self.style = ttk.Style()
        self.create_widgets()
        self.create_context_menu()
        self.root.bind("<Button-3>", self.show_context_menu)

        atexit.register(self.save_cache)

    def create_widgets(self):
        self.create_ip_type_frame()
        self.create_ip_entry_frame()
        self.create_website_entry_frame()
        self.create_format_frame()
        self.create_buttons_frame()

    def create_ip_type_frame(self):
        ip_type_frame = ttk.Frame(self.root)
        ip_type_frame.pack(pady=12)
        ip_type_label = ttk.Label(ip_type_frame, text="IP Type:")
        ip_type_label.pack(side=tk.LEFT)
        ipv4_radio = ttk.Radiobutton(ip_type_frame, text="IPv4", variable=self.ip_type_var, value=1)
        ipv4_radio.pack(side=tk.LEFT)
        ipv6_radio = ttk.Radiobutton(ip_type_frame, text="IPv6", variable=self.ip_type_var, value=2)
        ipv6_radio.pack(side=tk.LEFT)

    def create_ip_entry_frame(self):
        ip_entry_frame = ttk.Frame(self.root)
        ip_entry_frame.pack(pady=12)
        ip_label = ttk.Label(ip_entry_frame, text="Enter IP Address:")
        ip_label.pack(side=tk.LEFT)
        self.ip_entry = ttk.Entry(ip_entry_frame)
        self.ip_entry.pack(side=tk.LEFT)

    def create_website_entry_frame(self):
        website_entry_frame = ttk.Frame(self.root)
        website_entry_frame.pack(pady=12)
        website_label = ttk.Label(website_entry_frame, text="Enter Website URL:")
        website_label.pack(side=tk.LEFT)
        self.website_entry = ttk.Entry(website_entry_frame)
        self.website_entry.pack(side=tk.LEFT)

    def create_format_frame(self):
        format_frame = ttk.Frame(self.root)
        format_frame.pack(pady=12)
        format_label = ttk.Label(format_frame, text="Format:")
        format_label.pack(side=tk.LEFT)
        friendly_format_radio = ttk.Radiobutton(format_frame, text="User-friendly", variable=self.format_var, value=1)
        friendly_format_radio.pack(side=tk.LEFT)
        full_format_radio = ttk.Radiobutton(format_frame, text="Full", variable=self.format_var, value=2)
        full_format_radio.pack(side=tk.LEFT)
        ttk.Label(format_frame, text=" " * 18).pack(side=tk.LEFT)
        save_log_checkbutton = ttk.Checkbutton(format_frame, text="Save Log", variable=self.save_log_var, onvalue=True, offvalue=False)
        save_log_checkbutton.pack(side=tk.LEFT)

    def create_buttons_frame(self):
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=12)
        lookup_button = ttk.Button(buttons_frame, text="Lookup IP", command=self.ip_lookup)
        lookup_button.pack(side=tk.LEFT, padx=10)
        website_lookup_button = ttk.Button(buttons_frame, text="Website IP Lookup", command=self.website_ip_lookup)
        website_lookup_button.pack(side=tk.LEFT, padx=10)
        own_ip_button = ttk.Button(buttons_frame, text="Own IP Lookup", command=self.own_ip_lookup)
        own_ip_button.pack(side=tk.LEFT, padx=10)
        help_button = ttk.Button(buttons_frame, text="IP Format Help", command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=10)

    def ip_lookup(self):
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

            if ip in self.cache:
                response = self.cache[ip]
            else:
                response = self.get_ip_info(ip)
                self.cache[ip] = response

            self.display_ip_info(response)

    def website_ip_lookup(self):
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

                if ip in self.cache:
                    response = self.cache[ip]
                else:
                    response = self.get_ip_info(ip)
                    self.cache[ip] = response

                self.display_ip_info(response)
            except socket.gaierror:
                messagebox.showerror("Error", "The website you entered doesn't exist.")

    def show_please_wait_window(self):
        self.please_wait_window = tk.Toplevel(self.root)
        self.please_wait_window.title("Please Wait")
        self.please_wait_window.geometry("200x100")
        self.please_wait_window.resizable(False, False)
        if self.icon_path:
            self.please_wait_window.iconbitmap(self.icon_path)
        self.please_wait_label = ttk.Label(self.please_wait_window, text="Request sent. Please wait...")
        self.please_wait_label.pack(pady=20)

    def perform_own_ip_lookup(self):
        self.show_please_wait_window()
        try:
            ip = public_ip.get()

            if ip in self.cache:
                response = self.cache[ip]
            else:
                response = self.get_ip_info(ip)
                self.cache[ip] = response

            self.display_ip_info(response)
            self.please_wait_window.destroy()
        except (ValueError, IOError) as err:
            self.please_wait_window.destroy()
            messagebox.showerror("Error", str(err))

    def own_ip_lookup(self):
        if self.internet():
            Thread(target=self.perform_own_ip_lookup, daemon=True).start()

    @staticmethod
    def is_valid_ip_address(address: str, ip_type: int) -> bool:
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
        response = requests.get("http://ip-api.com/json/" + ip).json()
        return response

    @staticmethod
    def internet() -> bool:
        try:
            response = requests.get("https://www.google.com")
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            messagebox.showerror("Error", "You are not connected to the internet.")
            return False

    @staticmethod
    def show_help():
        w_open("https://en.wikipedia.org/wiki/IP_address")

    def display_ip_info(self, response: dict):
        if response['status'] == 'success':
            format_type = self.format_var.get()
            if format_type == 1:
                info = f"""Country: {response['country']}
                        \nRegion Name: {response['regionName']}
                        \nCity: {response['city']}
                        \nISP: {response['isp']}"""
                messagebox.showinfo(f"IP Lookup Application ({self.ver})", info)
            elif format_type == 2:
                response_copy = response.copy()
                response_copy.pop("status", None)
                formatted_info = self.format_json(response_copy)
                messagebox.showinfo(f"IP Lookup Application ({self.ver})", formatted_info)
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {response['message']}")

    def save_cache(self):
        if self.save_log_var.get() and self.cache:
            try:
                logs_dir = os.path.join(user_data_dir(appname="IP Lookup Utility"), "logs")
                if not os.path.exists(logs_dir):
                    os.makedirs(logs_dir)

                cache_log_path = os.path.join(logs_dir, "cache_log.txt")
                with open(cache_log_path, "a+") as file:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f"Cache saved at: {timestamp}\n")
                    for ip, data in self.cache.items():
                        data.pop("status", None)
                        data.pop("query", None)
                        file.write(f"IP Address: {ip}\n")
                        file.write(json.dumps(data, indent=4))
                        file.write("\n")
                    file.write("\n")
                messagebox.showinfo("Log Saved", f"Saved log to location: {cache_log_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save cache log: {str(e)}")

    @staticmethod
    def format_json(json_data: dict) -> str:
        formatted_info = ""
        for key, value in json_data.items():
            formatted_info += f"{key}: {value}\n"
        return formatted_info

    @staticmethod
    def download_update(download_url, latest_version):
        try:
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                update_zip_path = os.path.join(downloads_dir, f"IP Lookup Utility ({latest_version}).zip")
                with open(update_zip_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                messagebox.showinfo("Download Complete", f"Update downloaded at {update_zip_path}.")
            else:
                messagebox.showerror("Error", f"Failed to download the update. (Error Code: {response.status_code})")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading the update: {str(e)}")

    def check_latest_version(self):
        if self.internet():
            try:
                response = requests.get("https://api.github.com/repos/CwGmZ971/IP-Lookup-Utility/releases/latest")
                if response.status_code == 200:
                    latest_version = response.json()["tag_name"]
                    if latest_version[1:] != self.ver:
                        zipball_url = response.json().get("zipball_url")
                        result = messagebox.askyesno("Update Available",
                                                     f"New version {latest_version} is available. Do you want to download it now?")
                        if result:
                            self.download_update(zipball_url, latest_version)
                    else:
                        messagebox.showinfo("Up to Date", "You are using the latest version.")
                else:
                    messagebox.showerror("Error",
                                         f"Failed to check for updates. Please try again later. (Error Code: {response.status_code})")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_about_window(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("280x180")
        about_window.resizable(False, False)
        py_ver = python_version()
        if self.icon_path:
            about_window.iconbitmap(self.icon_path)

        about_text = (
            f"IP Lookup App:  {self.ver}\n"
            f"Python Version: {py_ver}\n"
            "This application uses ip-api.com for lookups\n"
            "Check the README.md file for details.\n"
            "Created by CwGmZ971 (Under MIT License)"
        )

        about_label = ttk.Label(about_window, text=about_text)
        about_label.pack(pady=10)

        update_button = ttk.Button(about_window, text="Check for Updates", command=self.check_latest_version)
        update_button.pack(pady=5)

        github_button = ttk.Button(about_window, text="GitHub Repository",
                                   command=lambda: w_open("https://github.com/CwGmZ971/IP-Lookup-Utility"))
        github_button.pack(pady=5)

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="About", command=self.show_about_window)

    def show_context_menu(self, event):
        # Check if the click occurred on a blank space
        if event.widget == self.root:
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()

    def run(self):
        if self.internet():
            self.root.mainloop()
        else:
            self.root.destroy()


if __name__ == "__main__":
    app = IPLookupApp()
    app.run()
