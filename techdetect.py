import requests, sys, json, os
from colorama import Fore, Style, init
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

SIGNATURES_FILE = "signatures.json"
RESULT_JSON = "results.json"
RESULT_TXT = "results.txt"

# ================= DEFAULT SIGNATURES =================
DEFAULT_SIGNATURES = {
    "CMS": {
        "WordPress": ["wp-content", "wp-includes"],
        "Shopify": ["cdn.shopify.com", "shopify"],
        "Drupal": ["sites/default"]
    },
    "Framework": {
        "Laravel": ["laravel_session"],
        "Django": ["csrftoken"]
    },
    "JavaScript": {
        "React": ["react"],
        "Vue": ["vue"],
        "jQuery": ["jquery"]
    }
}

# ================= BANNER =================
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
    print(Fore.CYAN + " Author : Gobinda")
    print(Fore.CYAN + " Instagram : @_g_o_b_i_n_d_a__200\n")

# ================= SIGNATURE HANDLING =================
def load_signatures():
    if not os.path.exists(SIGNATURES_FILE):
        with open(SIGNATURES_FILE, "w") as f:
            json.dump(DEFAULT_SIGNATURES, f, indent=4)
        print(Fore.YELLOW + "[i] signatures.json created")
        return DEFAULT_SIGNATURES
    with open(SIGNATURES_FILE, "r") as f:
        return json.load(f)

def save_signatures(data):
    with open(SIGNATURES_FILE, "w") as f:
        json.dump(data, f, indent=4)

SIGNATURES = load_signatures()

# ================= UPDATE MODE =================
def update_mode():
    print(Fore.CYAN + "[+] Update mode")
    cat = input("Category: ")
    tech = input("Tech name: ")
    patterns = input("Patterns (comma separated): ").split(",")

    if cat not in SIGNATURES:
        SIGNATURES[cat] = {}

    SIGNATURES[cat][tech] = [p.strip().lower() for p in patterns]
    save_signatures(SIGNATURES)

    print(Fore.GREEN + "[✔] Signature updated & saved")

# ================= SCAN =================
def scan_url(url):
    result = {"url": url, "headers": {}, "technologies": []}
    print(Fore.CYAN + f"[+] Scanning: {url}")

    try:
        r = requests.get(
            url,
            timeout=10,
            verify=False,
            headers={"User-Agent": "TechDetect"}
        )
    except Exception as e:
        print(Fore.RED + "[-] Failed")
        result["error"] = str(e)
        return result

    for h in ["server", "x-powered-by"]:
        if h in r.headers:
            result["headers"][h] = r.headers[h]

    html = r.text.lower()

    for category, techs in SIGNATURES.items():
        for tech, patterns in techs.items():
            if any(p in html for p in patterns):
                result["technologies"].append({
                    "category": category,
                    "name": tech
                })
                print(Fore.YELLOW + f"    {category}: {tech}")

    return result

# ================= USAGE =================
def usage():
    print(Fore.YELLOW + "Use:")
    print(" python techdetect.py -u https://example.com -json")
    print(" python techdetect.py -f urls.txt -o")
    print(" python techdetect.py -f urls.txt -json -o")
    print(" python techdetect.py --update")

# ================= MAIN =================
def main():
    banner()

    if "--update" in sys.argv:
        update_mode()
        return

    urls = []

    if "-u" in sys.argv:
        urls.append(sys.argv[sys.argv.index("-u") + 1])

    elif "-f" in sys.argv:
        file_path = sys.argv[sys.argv.index("-f") + 1]
        if not os.path.exists(file_path):
            print(Fore.RED + "URL file not found")
            return
        urls = [u.strip() for u in open(file_path) if u.strip()]

    else:
        usage()
        return

    results = []
    for url in urls:
        results.append(scan_url(url))

    if "-json" in sys.argv:
        with open(RESULT_JSON, "w") as f:
            json.dump(results, f, indent=4)
        print(Fore.GREEN + f"[✔] Saved {RESULT_JSON}")

    if "-o" in sys.argv:
        with open(RESULT_TXT, "w") as f:
            for r in results:
                f.write(r["url"] + "\n")
                for t in r["technologies"]:
                    f.write(f"  {t['category']}: {t['name']}\n")
                f.write("\n")
        print(Fore.GREEN + f"[✔] Saved {RESULT_TXT}")

if __name__ == "__main__":
    main()
