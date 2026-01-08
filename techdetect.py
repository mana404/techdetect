def main():
    banner()

    # ====== Y ======
    if "--update" in sys.argv:
        try:
            category = sys.argv[sys.argv.index("--update") + 1]
            tech = sys.argv[sys.argv.index("--update") + 2]
            patterns = sys.argv[sys.argv.index("--update") + 3].split(",")

            update_signatures(category, tech, patterns)
            print(Fore.CYAN + "[i] Signature added. Ab scan chalao.")
            return
        except:
            print(Fore.RED + "Usage:")
            print(" python techdetect.py --update <Category> <TechName> <pattern1,pattern2>")
            return
    # ====== YK ======

    # 👇 iske baad tumhara existing -u / -l code rahega
import requests, sys, json
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

results = []

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


    def update_signatures(category, tech_name, patterns):
    global SIGNATURES

    if category not in SIGNATURES:
        SIGNATURES[category] = {}

    SIGNATURES[category][tech_name] = patterns
    print(Fore.GREEN + f"[✔] Signature updated → {category}: {tech_name}")


# ================== SCAN FUNCTION ==================
def scan_url(url):
    print(Fore.CYAN + f"\n[+] Scanning: {url}")
    data = {"url": url, "headers": {}, "technologies": []}

    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "TechDetect"})
    except:
        print(Fore.RED + "[-] Unreachable")
        data["error"] = "Unreachable"
        results.append(data)
        return

    # Header detection
    for h in ["server", "x-powered-by"]:
        if h in r.headers:
            data["headers"][h] = r.headers[h]
            print(Fore.GREEN + f"    {h}: {r.headers[h]}")

    html = r.text.lower()
    soup = BeautifulSoup(html, "html.parser")

    # Load signatures
    sigs = load_signatures()


    for category, techs in sigs.items():
        for tech, patterns in techs.items():
            for p in patterns:
                if p in html:
                    tech_line = f"{category}: {tech}"
                    print(Fore.YELLOW + f"    {tech_line}")
                    data["technologies"].append(tech_line)
                    break

    # CDN detect
    for s in soup.find_all("script"):
        src = s.get("src")
        if src and "cloudflare" in src.lower():
            print(Fore.BLUE + "    CDN: Cloudflare")
            data["technologies"].append("CDN: Cloudflare")

    results.append(data)

# ================== SAVE OUTPUT ==================
def save_txt(file):
    with open(file, "w") as f:
        for r in results:
            f.write(f"\nURL: {r['url']}\n")
            if "error" in r:
                f.write("  ERROR: Unreachable\n")
                continue
            for k, v in r["headers"].items():
                f.write(f"  {k}: {v}\n")
            for t in r["technologies"]:
                f.write(f"  {t}\n")

def save_json(file):
    with open(file, "w") as f:
        json.dump(results, f, indent=4)

# ================== MAIN ==================
def main():
    banner()

    if "-u" not in sys.argv and "-l" not in sys.argv:
        print(Fore.YELLOW + "Usage:")
        print("  Single URL : python techdetect.py -u https://example.com")
        print("  URL List   : python techdetect.py -l urls.txt")
        print("  Output     : -o out.txt  -j out.json")
        return

    if "-u" in sys.argv:
        url = sys.argv[sys.argv.index("-u") + 1]
        scan_url(url)

    if "-l" in sys.argv:
        file = sys.argv[sys.argv.index("-l") + 1]
        with open(file) as f:
            urls = [u.strip() for u in f if u.strip()]
        for url in urls:
            scan_url(url)

    if "-o" in sys.argv:
        save_txt(sys.argv[sys.argv.index("-o") + 1])

    if "-j" in sys.argv:
        save_json(sys.argv[sys.argv.index("-j") + 1])

    print(Fore.GREEN + "\n[✔] Scan completed successfully")

if __name__ == "__main__":
    main()
