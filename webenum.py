import requests
import re
import socket
from colorama import Fore, Style

def scrape_crtsh(domain):
     """Scrapes crt.sh for subdomains."""
     url = f"https://crt.sh/?q=%25.{domain}&output=json"
     headers = {"User-Agent": "Mozilla/5.0"}
     
     try:
          response = requests.get(url, headers=headers, timeout=10)
          if response.status_code != 200:
               print(f"{Fore.RED}[-] Failed to fetch data from crt.sh{Style.RESET_ALL}")
               return set()
          
          json_data = response.json()
          subdomains = set()
          
          for entry in json_data:
               name = entry["name_value"]
               subdomains.update(name.split("\n"))  # Some entries have multiple subdomains

          subdomains = {sub.strip() for sub in subdomains if re.match(r"^[a-zA-Z0-9.-]+$", sub)}
          return subdomains

     except requests.RequestException as e:
          print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")
          return set()

def resolve_subdomain(subdomain):
     """Attempts to resolve a subdomain to check if it's active."""
     try:
          ip = socket.gethostbyname(subdomain)
          return f"{Fore.YELLOW}[+]{Style.RESET_ALL} {Fore.GREEN}Active: {subdomain} -> {ip}{Style.RESET_ALL}"
     except socket.gaierror:
          return None  # Ignore unresolved subdomains

def main():
     domain = input("Enter target domain: ").strip()

     print(f"\n{Fore.BLUE}[~] Scraping crt.sh for subdomains...{Style.RESET_ALL}\n")
     subdomains = scrape_crtsh(domain)
     
     if subdomains:
          print(f"{Fore.YELLOW}[+] Found {len(subdomains)} subdomains. Verifying active ones...{Style.RESET_ALL}\n")
          active_subdomains = [resolve_subdomain(sub) for sub in sorted(subdomains)]
          
          # Print only active subdomains
          for result in active_subdomains:
               if result:
                    print(result)
     else:
          print(f"{Fore.RED}[-] No subdomains found.{Style.RESET_ALL}")

if __name__ == "__main__":
     main()
