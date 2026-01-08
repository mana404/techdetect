import requests, sys, json, os
from colorama import Fore, Style, init

init(autoreset=True)

SIGNATURES_FILE = "signatures.json"
RESULTS_FILE = "results.json"

# ================== DEFAULT SIGNATURES ==================
DEFAULT_SIGNATURES = {
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

# ================== JSON HANDLING ==================
def load_signatures():
    if not os.path.exists(SIGNATURES_FILE):
        with open(SIGNATURES_FILE, "w") as f:
            json.dump(DEFAULT_SIGNATURES, f, indent=4)
        print(Fore.YELLOW + "[i] signatures.json not found. Created default signatures.")
        return DEFAULT_SIGNATURES
    with open(SIGNATURES_FILE, "r") as f:
        return json.load(f)

def save_signatures(signatures):
    with open(SIGNATURES_FILE, "w") as f:
        json.dump(signatures, f, indent=4)

def save_results(results):
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=4)
    print(Fore.CYAN + f"[i] Results saved to {RESULTS_FILE}")

SIGNATURES = load_signatures()

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
    if category not in SIGNATURES:
        SIGNATURES[category] = {}
    SIGNATURES[category][tech_name] = patterns
    save_signatures(SIGNATURES)
    print(Fore.GREEN + f"[✔] Signature updated → {category}: {tech_name}")

# ================== SCAN FUNCTION ==================
def scan_url(url):
    result = {"url": url, "headers": {}, "technologies": []}
    print(Fore.CYAN + f"[+] Scanning: {url}")

    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "TechDetect"})
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[-] Unreachable: {e}")
        result["error"] = str(e)
        return result

    # Header detection
    for h in ["server", "x-powered-by"]:
        if h in r.headers:
            result["headers"][h] = r.headers[h]

    html = r.text.lower()

    # Detect technologies
    for category, techs in SIGNATURES.items():
        for tech, patterns in techs.items():
            if any(p.lower() in html for p in patterns):
                result["technologies"].append({"category": category, "name": tech})

    # Print to console
    if result["headers"]:
        for h, v in result["headers"].items():
            print(Fore.GREEN + f"    {h}: {v}")
    if result["technologies"]:
        for t in result["technologies"]:
            print(Fore.YELLOW + f"    {t['category']}: {t['name']}")
    else:
        print(Fore.RED + "    No technologies detected.")

    return result

# ================== MAIN ==================
def main():
    banner()

    # ---------- UPDATE MODE ----------
    if "--update" in sys.argv:
        try:
            idx = sys.argv.index("--update")
            category = sys.argv[idx + 1]
            tech = sys.argv[idx + 2]
            patterns = sys.argv[idx + 3].split(",")
            update_signatures(category, tech, patterns)
            print(Fore.CYAN + "[i] Update complete. Ab scan command chalao.")
            return
        except Exception as e:
            print(Fore.RED + "Usage:")
            print(" python techdetect.py --update <Category> <TechName> <pattern1,pattern2>")
            print(Fore.RED + f"Error: {e}")
            return

    # ---------- SCAN MODE ----------
    urls = []
    if "-u" in sys.argv:
        urls.append(sys.argv[sys.argv.index("-u") + 1])
    elif "-f" in sys.argv:
        file_path = sys.argv[sys.argv.index("-f") + 1]
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                urls = [line.strip() for line in f if line.strip()]
        else:
            print(Fore.RED + f"File not found: {file_path}")
            return
    else:
        print(Fore.YELLOW + "Usage:")
        print(" python techdetect.py -u https://example.com")
        print(" python techdetect.py -f urls.txt   (file containing multiple URLs)")
        print(" python techdetect.py --update CMS Shopify cdn.shopify.com,shopify")
        return

    all_results = []
    for url in urls:
        res = scan_url(url)
        all_results.append(res)

    save_results(all_results)

# ================== RUN ==================
if __name__ == "__main__":
    main()
