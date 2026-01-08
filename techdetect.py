import requests, sys, json
from bs4 import BeautifulSoup

results = []

def banner():
    print("""
████████╗███████╗ ██████╗██╗  ██╗██████╗ ███████╗████████╗
╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔══██╗██╔════╝╚══██╔══╝
   ██║   █████╗  ██║     ███████║██║  ██║█████╗     ██║
   ██║   ██╔══╝  ██║     ██╔══██║██║  ██║██╔══╝     ██║
   ██║   ███████╗╚██████╗██║  ██║██████╔╝███████╗   ██║
   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝
        Technology Detection Tool
    """)

def scan_url(url):
    data = {"url": url, "headers": {}, "technologies": []}

    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "TechDetect"})
    except:
        data["error"] = "Unreachable"
        results.append(data)
        return

    for h in ["server", "x-powered-by"]:
        if h in r.headers:
            data["headers"][h] = r.headers[h]

    html = r.text.lower()
    soup = BeautifulSoup(html, "html.parser")

    with open("signatures.json") as f:
        sigs = json.load(f)

    for category, techs in sigs.items():
        for tech, patterns in techs.items():
            for p in patterns:
                if p in html:
                    data["technologies"].append(f"{category}: {tech}")
                    break

    for s in soup.find_all("script"):
        src = s.get("src")
        if src and "cloudflare" in src.lower():
            data["technologies"].append("CDN: Cloudflare")

    results.append(data)

def save_txt(file):
    with open(file, "w") as f:
        for r in results:
            f.write(f"\nURL: {r['url']}\n")
            if "error" in r:
                f.write("  ERROR: Unreachable\n")
                continue
            for k,v in r["headers"].items():
                f.write(f"  {k}: {v}\n")
            for t in r["technologies"]:
                f.write(f"  {t}\n")

def save_json(file):
    with open(file, "w") as f:
        json.dump(results, f, indent=4)

def main():
    banner()

    if "-l" not in sys.argv:
        print("Usage: python techdetect.py -l urls.txt [-o out.txt] [-j out.json]")
        return

    urls = open(sys.argv[sys.argv.index("-l")+1]).read().splitlines()
    for u in urls:
        scan_url(u.strip())

    if "-o" in sys.argv:
        save_txt(sys.argv[sys.argv.index("-o")+1])

    if "-j" in sys.argv:
        save_json(sys.argv[sys.argv.index("-j")+1])

    print("\n[+] Scan completed successfully ✔")

if __name__ == "__main__":
    main()
