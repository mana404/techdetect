import requests, sys, json
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

# ================== GLOBAL DATA ==================
results = []

SIGNATURES = {
    "CMS": {
        "WordPress": ["wp-content", "wp-includes"],
        "Drupal": ["sites/default"],
        "Joomla": ["com_content"]
    },
    "Framework": {
        "Laravel": ["laravel_session"],
        "Django": ["csrftoken"]
    },
    "JavaScript": {
        "jQuery": ["jquery"],
        "React": ["react"],
        "Vue": ["vue"]
    }
}

# ================== BANNER ==================
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
    print(Fore.CYAN + " Author    : Gobinda")
    print(Fore.CYAN + " Instagram : @_g_o_b_i_n_d_a__200\n")

# ================== UPDATE FUNCTION ==================
def update_signatures(category, tech_name, patterns):
    global SIGNATURES

    if category not in SIGNATURES:
        SIGNATURES[category] = {}

    SIGNATURES[category][tech_name] = patterns
    print(Fore.GREEN + f"[✔] Signature updated → {category}: {tech_name}")

# ================== SCAN FUNCTION ==================
def scan_url(url):
    print(Fore.CYAN + f"[+] Scanning: {url}")
    data = {"url": url, "headers": {}, "technologies": []}

    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "TechDetect"})
    except:
        print(Fore.RED + "[-] Unreachable")
        return

    # Header detection
    for h in ["server", "x-powered-by"]:
        if h in r.headers:
            print(Fore.GREEN + f"    {h}: {r.headers[h]}")

    html = r.text.lower()

    for category, techs in SIGNATURES.items():
        for tech, patterns in techs.items():
            for p in patterns:
                if p in html:
                    print(Fore.YELLOW + f"    {category}: {tech}")
                    break

# ================== MAIN ==================
def main():
    banner()

    # ---------- UPDATE MODE ----------
    if "--update" in sys.argv:
        try:
            category = sys.argv[sys.argv.index("--update") + 1]
            tech = sys.argv[sys.argv.index("--update") + 2]
            patterns = sys.argv[sys.argv.index("--update") + 3].split(",")

            update_signatures(category, tech, patterns)
            print(Fore.CYAN + "[i] Update complete. Ab scan command chalao.")
            return
        except:
            print(Fore.RED + "Usage:")
            print(" python techdetect.py --update <Category> <TechName> <pattern1,pattern2>")
            return

    # ---------- SCAN MODE ----------
    if "-u" in sys.argv:
        url = sys.argv[sys.argv.index("-u") + 1]
        scan_url(url)
    else:
        print(Fore.YELLOW + "Usage:")
        print(" python techdetect.py -u https://example.com")
        print(" python techdetect.py --update CMS Shopify cdn.shopify.com,shopify")

# ================== RUN ==================
if __name__ == "__main__":
    main()
