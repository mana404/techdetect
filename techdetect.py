import requests
import sys
import json
import os
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

# 1. LIST OF FILES (Files ke naam yahan define hain)
SIGNATURES_FILE = "signatures.json"
RESULTS_FILE = "results.json"

DEFAULT_SIGNATURES = {
    "CMS": {"WordPress": ["wp-content"], "Drupal": ["sites/default"]},
    "Framework": {"Laravel": ["laravel_session"]},
    "Server": {"Nginx": ["nginx"], "Apache": ["apache"]}
}

# 2. BANNER AUR AAPKA NAAM (Yahan hai)
def banner():
    print(Fore.RED + Style.BRIGHT + r"""
 ████████╗███████╗ ██████╗██╗  ██╗██████╗ ███████╗████████╗
 ╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔══██╗██╔════╝╚══██╔══╝
    ██║   █████╗  ██║     ███████║██║  ██║█████╗     ██║   
    ██║   ██╔══╝  ██║     ██╔══██║██║  ██║██╔══╝     ██║   
    ██║   ███████╗╚██████╗██║  ██║██████╔╝███████╗   ██║   
    ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   
""")
    print(Fore.YELLOW + " Technology Detection Tool")
    print(Fore.CYAN + " Author    : Gobinda") # <--- Aapka Naam
    print(Fore.CYAN + " Instagram : @_g_o_b_i_n_d_a__200\n")

def load_signatures():
    if not os.path.exists(SIGNATURES_FILE):
        with open(SIGNATURES_FILE, "w") as f:
            json.dump(DEFAULT_SIGNATURES, f, indent=4)
        return DEFAULT_SIGNATURES
    with open(SIGNATURES_FILE, "r") as f:
        return json.load(f)

SIGNATURES = load_signatures()

def scan_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    result = {"url": url, "technologies": []}
    try:
        r = requests.get(url, timeout=5, headers={"User-Agent": "TechDetect"}, verify=False)
        html = r.text.lower()
        for category, techs in SIGNATURES.items():
            for tech, patterns in techs.items():
                if any(p.lower() in html for p in patterns):
                    result["technologies"].append({"category": category, "name": tech})
        
        # Console Output
        if result["technologies"]:
            print(Fore.GREEN + f"[✔] {url} -> " + ", ".join([t['name'] for t in result["technologies"]]))
        else:
            print(Fore.WHITE + f"[-] {url} -> No Tech Found")
        return result
    except:
        print(Fore.RED + f"[!] {url} -> Unreachable")
        return {"url": url, "error": "Unreachable"}

def main():
    banner() # Banner yahan call ho raha hai
    
    # 3. SCAN & OUTPUT SAVING (Yahan save ho raha hai)
    if "-f" in sys.argv:
        file_path = sys.argv[sys.argv.index("-f") + 1]
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                urls = [line.strip() for line in f if line.strip()]
            
            print(Fore.YELLOW + f"[*] Scanning {len(urls)} sites...\n")
            with ThreadPoolExecutor(max_workers=10) as executor:
                all_results = list(executor.map(scan_url, urls))
            
            # OUTPUT SAVING LOGIC
            with open(RESULTS_FILE, "w") as f:
                json.dump(all_results, f, indent=4)
            print(Fore.MAGENTA + f"\n[i] Results saved in: {RESULTS_FILE}") # <--- File Save message
        else:
            print(Fore.RED + "Error: Input file not found!")
    elif "-u" in sys.argv:
        url = sys.argv[sys.argv.index("-u") + 1]
        scan_url(url)
    else:
        print("Usage: python tool.py -u <url> OR -f <list.txt>")

if __name__ == "__main__":
    main()