import requests
import sys
import json
import os
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

SIGNATURES_FILE = "signatures.json"
RESULTS_FILE = "results.json"

# Mega List Jo Aapne Di Thi
DEFAULT_SIGNATURES = {
    "CMS": {
        "WordPress": ["wp-content", "wp-includes"],
        "Drupal": ["sites/default"],
        "Joomla": ["com_content"],
        "Magento": ["mage", "magento"],
        "Blogger": ["blogger"],
        "Ghost": ["ghost"]
    },
    "Framework": {
        "Laravel": ["laravel_session"],
        "Django": ["csrftoken"],
        "Flask": ["flask", "werkzeug"],
        "Spring": ["jsessionid"],
        "Express": ["express"]
    },
    "JavaScript": {
        "jQuery": ["jquery"], "React": ["react"], "Vue": ["vue"],
        "Angular": ["angular"], "Next.js": ["_next"], "Nuxt": ["_nuxt"]
    },
    "Server": {
        "Apache": ["apache"], "Nginx": ["nginx"], "LiteSpeed": ["litespeed"]
    },
    "CDN / Security": {
        "Cloudflare": ["cloudflare", "cf-ray"], "Akamai": ["akamai"], "Sucuri": ["sucuri"]
    }
}

def banner():
    print(Fore.RED + Style.BRIGHT + r"""
 ████████╗███████╗ ██████╗██╗  ██╗██████╗ ███████╗████████╗
 ╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔══██╗██╔════╝╚══██╔══╝
    ██║   █████╗  ██║     ███████║██║  ██║█████╗     ██║   
    ██║   ██╔══╝  ██║     ██╔══██║██║  ██║██╔══╝     ██║   
    ██║   ███████╗╚██████╗██║  ██║██████╔╝███████╗   ██║   
    ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   
""")
    print(Fore.YELLOW + " Technology Detection Tool | Author: Gobinda")

def load_signatures():
    if not os.path.exists(SIGNATURES_FILE):
        with open(SIGNATURES_FILE, "w") as f:
            json.dump(DEFAULT_SIGNATURES, f, indent=4)
        return DEFAULT_SIGNATURES
    with open(SIGNATURES_FILE, "r") as f:
        return json.load(f)

def save_signatures(signatures):
    with open(SIGNATURES_FILE, "w") as f:
        json.dump(signatures, f, indent=4)

def scan_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    res_data = {"url": url, "technologies": []}
    try:
        r = requests.get(url, timeout=7, headers={"User-Agent": "TechDetect"}, verify=False)
        html = r.text.lower()
        sigs = load_signatures()
        for cat, techs in sigs.items():
            for tech, patterns in techs.items():
                if any(p.lower() in html for p in patterns):
                    res_data["technologies"].append({"category": cat, "name": tech})
        
        if res_data["technologies"]:
            found = ", ".join([t['name'] for t in res_data["technologies"]])
            print(Fore.GREEN + f"[✔] {url} -> {found}")
        else:
            print(Fore.WHITE + f"[-] {url} -> No Tech Found")
        return res_data
    except:
        return {"url": url, "error": "Dead"}

def main():
    banner()
    sigs = load_signatures()

    # ================== UPDATE COMMAND LOGIC ==================
    if "--update" in sys.argv:
        try:
            # Usage: python tool.py --update CMS Shopify shopify,cdn.shopify
            cat = sys.argv[sys.argv.index("--update") + 1]
            name = sys.argv[sys.argv.index("--update") + 2]
            patterns = sys.argv[sys.argv.index("--update") + 3].split(",")
            
            if cat not in sigs: sigs[cat] = {}
            sigs[cat][name] = patterns
            save_signatures(sigs)
            print(Fore.CYAN + f"[+] Success: {name} added to {cat}!")
            return
        except:
            print(Fore.RED + "Usage: python tool.py --update <Category> <Name> <pattern1,pattern2>")
            return

    # ================== SCANNING LOGIC ==================
    urls = []
    if "-u" in sys.argv:
        urls.append(sys.argv[sys.argv.index("-u") + 1])
    elif "-f" in sys.argv:
        path = sys.argv[sys.argv.index("-f") + 1]
        if os.path.exists(path):
            with open(path, "r") as f:
                urls = [l.strip() for l in f if l.strip()]
    
    if urls:
        with ThreadPoolExecutor(max_workers=10) as exe:
            results = list(exe.map(scan_url, urls))
        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=4)
        print(Fore.MAGENTA + f"\n[!] Done! Saved to {RESULTS_FILE}")
    else:
        print("Use -u for URL or -f for file.")

if __name__ == "__main__":
    main()