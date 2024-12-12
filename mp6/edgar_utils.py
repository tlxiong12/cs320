import netaddr
import re
import pandas as pd
from bisect import bisect
from bs4 import BeautifulSoup

ips = pd.read_csv("ip2location.csv")
    
def lookup_region(ip):
    cleanip = re.sub(r'[^0-9.]', '0', ip) 
    ip_to_int = int(netaddr.IPAddress(cleanip))
    idx = bisect(ips['low'], ip_to_int) - 1 
    return ips.iloc[idx]['region']


class Filing:
    def __init__(self, html):
        self.dates = None  
        self.sic = None  
        self.addresses = None 

        dates = re.findall(r"\b(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b", html)
        self.dates = ["-".join(date) for date in dates]

        sics = re.findall(r"SIC=(\d+)", html)
        self.sic = int(sics[0]) if sics else None  

        addresses = []
        for addr_html in re.findall(r'<div class="mailer">(.*?)</div>', html, re.DOTALL):
            address = re.sub(r'^(Mailing Address|Business Address)\s*', '', addr_html)
            address = re.sub(r'<.*?>', '', address)
            cleaned_address = address.strip()
            if cleaned_address:
                addresses.append(cleaned_address)
        self.addresses = addresses
        
    def state(self):
        for address in self.addresses:
            cleaned_address = " ".join(address.split())
            match = re.search(r'\b([A-Z]{2})\s\d{5}\b', cleaned_address)
            if match:
                return match.group(1)
        return None


