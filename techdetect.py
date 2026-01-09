import requests, json, os, sys
from colorama import Fore, Style, init
import urllib3

init(autoreset=True)
urllib3.disable_warnings()

SIG_FILE = "signatures.json"

# ================= DEFAULT SIGNATURES =================
DEFAULT_SIG = {
    "CMS": {
        "Shopify": ["cdn.shopify.com", "shopify"],
        "WordPress": ["wp-content", "wp-includes"]
    },
    "CDN": {
        "Cloudflare": ["cloudflare", "cf-ray"]
    },
    "JavaScript": {
        "React": ["react"],
        "Vue": ["vue"]
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
    print(Fore.CYAN + " Author    : Gobinda")
    print(Fore.CYAN + " Instagram : @_g_o_b_i_n_d_a__200\n")

# ================= LOAD / SAVE =================
def load_signatures():
    if not os.path.exists(SIG_FILE):
        with open(SIG_FILE, "w") as f:
            json.dump(DEFAULT_SIG, f, indent=4)
        print(Fore.YELLOW + "[i] signatures.json created")
        return DEFAULT_SIG

    with open(SIG_FILE) as f:
        return json.load(f)

def save_signatures(data):
    with open(SIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

SIG = load_signatures()

# ================= UPDATE MODE =================
def update_mode():
    print(Fore.CYAN + "[UPDATE MODE]")
    cat = input("Category: ")
    tech = input("Tech name: ")
    pats = input("Patterns (comma): ").lower().split(",")

    if cat not in SIG:
        SIG[cat] = {}

    SIG[cat][tech] = [p.strip() for p in pats]
    save_signatures(SIG)

    print(Fore.GREEN + "[✔] signatures.json UPDATED")

# ================= SCAN =================
def scan(url):
    print(Fore.CYAN + f"\n[+] Scanning: {url}")
    found = []

    try:
        r = requests.get(url, timeout=10, verify=False,
                         headers={"User-Agent": "TechDetect"})
    except Exception as e:
        print(Fore.RED + "[-] Failed:", e)
        return found

    data = (
        r.text.lower()
        + " ".join(f"{k}:{v}".lower() for k, v in r.headers.items())
        + " ".join(c.name.lower() for c in r.cookies)
    )

    for cat, techs in SIG.items():
        for tech, patterns in techs.items():
            for p in patterns:
                if p in data:
                    print(Fore.GREEN + f"    ✔ {cat}: {tech}")
                    found.append({"category": cat, "tech": tech})
                    break

    if not found:
        print(Fore.YELLOW + "    [!] Nothing detected")

    return found

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
        f = sys.argv[sys.argv.index("-f") + 1]
        urls = [u.strip() for u in open(f) if u.strip()]

    else:
        print("Usage:")
        print(" python techdetect.py -u https://example.com -o -json")
        print(" python techdetect.py -f urls.txt -o -json")
        print(" python techdetect.py --update")
        return

    all_results = []

    for u in urls:
        techs = scan(u)
        all_results.append({"url": u, "tech": techs})

    if "-o" in sys.argv:
        with open("results.txt", "w") as f:
            for r in all_results:
                f.write(r["url"] + "\n")
                for t in r["tech"]:
                    f.write(f"  {t['category']}: {t['tech']}\n")
                f.write("\n")
        print(Fore.GREEN + "[✔] results.txt saved")

    if "-json" in sys.argv:
        with open("results.json", "w") as f:
            json.dump(all_results, f, indent=4)
        print(Fore.GREEN + "[✔] results.json saved")

if __name__ == "__main__":
    main()
