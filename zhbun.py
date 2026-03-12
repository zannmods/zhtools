#!/usr/bin/env python3
"""
Advanced Bug Bounty Automation Framework (PRO VERSION 5.0)
Workflow: Subfinder -> HTTPX -> Katana (Crawling) -> Nuclei & Dalfox

Pembaruan v5.0:
- Penambahan mode STEALTH / ANTI-WAF
- Random User-Agent otomatis
- Delay & limitasi traffic cerdas untuk mencegah blokir WAF
"""

import os
import sys
import subprocess
import argparse
import time
import shutil
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║       BUG BOUNTY AUTOMATION SCANNER - ULTRA PRO v5.0         ║
    ║  Workflow: Enum -> Probe -> Crawl -> Vuln Scan -> XSS Hunt   ║
    ╚══════════════════════════════════════════════════════════════╝
    {Colors.ENDC}"""
    print(banner)

def ask_yes_no(question, default="y"):
    """Menampilkan prompt interaktif Yes/No kepada pengguna."""
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "y":
        prompt = " [Y/n] "
    elif default == "n":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer")

    while True:
        sys.stdout.write(f"{Colors.BOLD}{Colors.CYAN}[?]{Colors.ENDC} {question}{prompt}")
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Silakan jawab dengan 'y' atau 'n'.\n")

def check_dependencies(selected_tools):
    """Memeriksa apakah tools yang dipilih ada di PATH tanpa menginstalnya."""
    missing = []
    print(f"{Colors.BLUE}[*] Memeriksa dependensi tools yang akan digunakan...{Colors.ENDC}")
    
    for tool in selected_tools:
        if shutil.which(tool) is None:
            missing.append(tool)
        else:
            print(f"{Colors.GREEN}  [+] {tool} {Colors.ENDC}terdeteksi.")
    
    if missing:
        print(f"\n{Colors.FAIL}[!] EROR: Tools berikut tidak ditemukan di PATH: {', '.join(missing)}{Colors.ENDC}")
        print(f"{Colors.WARNING}Silakan install tools yang kurang. Skrip ini tidak akan menimpa/menginstal otomatis demi keamanan environment Anda.{Colors.ENDC}")
        sys.exit(1)
    print("")

def run_command(command, description):
    """Menjalankan perintah shell secara realtime."""
    print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.WARNING}>> Memulai: {description}{Colors.ENDC}")
    print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.ENDC}")
    
    try:
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        for line in process.stdout:
            print(line.strip())
            
        process.wait()
        
        if process.returncode == 0:
            print(f"{Colors.GREEN}\n[✓] Selesai: {description}{Colors.ENDC}\n")
            return True
        else:
            print(f"{Colors.FAIL}\n[✗] Gagal/Peringatan pada: {description} (Exit Code: {process.returncode}){Colors.ENDC}")
            print(f"{Colors.WARNING}Catatan: Beberapa tool mengembalikan exit code non-0 jika menemukan error kecil. Proses tetap dilanjutkan.{Colors.ENDC}\n")
            return True # Tetap kembalikan True agar pipeline tidak berhenti total
            
    except Exception as e:
        print(f"{Colors.FAIL}[!] Exception sistem saat menjalankan {description}: {str(e)}{Colors.ENDC}\n")
        return False

def filter_parameters(katana_out, params_out):
    """Menyaring URL berparameter dengan cerdas (Abaikan file statis)."""
    print(f"{Colors.BLUE}[*] Menyaring URL dengan parameter untuk Dalfox...{Colors.ENDC}")
    count = 0
    # Ekstensi yang biasanya tidak rentan terhadap XSS meskipun berparameter
    ignored_exts = ('.jpg', '.jpeg', '.png', '.gif', '.css', '.svg', '.woff', '.woff2', '.ttf', '.eot', '.ico', '.pdf')
    
    try:
        with open(katana_out, 'r') as infile, open(params_out, 'w') as outfile:
            for line in infile:
                url = line.strip()
                if '?' in url and '=' in url:
                    # Ambil path URL tanpa parameter untuk pengecekan ekstensi
                    base_path = url.split('?')[0].lower()
                    if not base_path.endswith(ignored_exts):
                        outfile.write(url + '\n')
                        count += 1
                        
        print(f"{Colors.GREEN}  [+] Ditemukan {count} URL berparameter yang valid.{Colors.ENDC}\n")
        return count > 0
    except FileNotFoundError:
        print(f"{Colors.FAIL}[!] File output Katana tidak ditemukan.{Colors.ENDC}")
        return False

def check_file_has_data(filepath):
    """Memeriksa apakah file ada dan tidak kosong."""
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def main():
    parser = argparse.ArgumentParser(description="Pro Bug Bounty Automation Framework v4 Interaktif")
    parser.add_argument("-t", "--target", help="Target domain atau URL utama (contoh: target.com)", required=True)
    parser.add_argument("-o", "--output", help="Nama awalan folder output", default="scans")
    parser.add_argument("--blind", help="URL XSS Hunter / Interactsh untuk Blind XSS Dalfox", default="")
    args = parser.parse_args()

    target = args.target.replace("https://", "").replace("http://", "").strip("/")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"{args.output}_{target}_{timestamp}"

    print_banner()
    
    # --- SESI INTERAKTIF WIZARD ---
    print(f"{Colors.HEADER}=== KONFIGURASI WORKFLOW INTERAKTIF ==={Colors.ENDC}")
    use_subfinder = ask_yes_no(f"Gunakan {Colors.BOLD}Subfinder{Colors.ENDC} untuk mencari subdomain? (Pilih 'n' jika ingin fokus 1 web)")
    use_httpx = ask_yes_no(f"Gunakan {Colors.BOLD}HTTPX{Colors.ENDC} untuk filter host yang aktif?")
    use_katana = ask_yes_no(f"Gunakan {Colors.BOLD}Katana{Colors.ENDC} untuk crawling endpoint & parameter?")
    use_nuclei = ask_yes_no(f"Gunakan {Colors.BOLD}Nuclei{Colors.ENDC} untuk full vulnerability scanning?")
    
    use_dalfox = False
    if use_katana:
        use_dalfox = ask_yes_no(f"Gunakan {Colors.BOLD}Dalfox{Colors.ENDC} untuk scan XSS di endpoint hasil Katana?")
    else:
        print(f"{Colors.WARNING}[!] Katana dinonaktifkan. Dalfox akan dilewati karena butuh data parameter endpoint.{Colors.ENDC}")

    deep_scan = ask_yes_no(f"Aktifkan mode {Colors.BOLD}DEEP SCAN{Colors.ENDC} (Lebih lambat, threads lebih agresif & mendalam)?", default="n")
    stealth_mode = ask_yes_no(f"Aktifkan mode {Colors.BOLD}STEALTH / ANTI-WAF{Colors.ENDC} (Lambat, Random UA, mencegah blokir Cloudflare/dll)?", default="y")
    print(f"{Colors.HEADER}======================================={Colors.ENDC}\n")

    # Kumpulkan tools yang divalidasi
    selected_tools = []
    if use_subfinder: selected_tools.append('subfinder')
    if use_httpx: selected_tools.append('httpx')
    if use_katana: selected_tools.append('katana')
    if use_nuclei: selected_tools.append('nuclei')
    if use_dalfox: selected_tools.append('dalfox')

    if not selected_tools:
        print(f"{Colors.FAIL}[!] Anda tidak memilih tool apa pun. Keluar...{Colors.ENDC}")
        sys.exit(0)

    check_dependencies(selected_tools)

    os.makedirs(output_dir, exist_ok=True)
    print(f"{Colors.BLUE}[*] Workspace target dibuat di: {Colors.BOLD}{output_dir}{Colors.ENDC}\n")

    # Definisi Paths
    subs_file = os.path.join(output_dir, "1_subdomains.txt")
    live_file = os.path.join(output_dir, "2_live_hosts.txt")
    katana_out = os.path.join(output_dir, "3_crawled_urls.txt")
    params_out = os.path.join(output_dir, "4_vulnerable_params.txt")
    nuclei_out = os.path.join(output_dir, "5_nuclei_findings.txt")
    dalfox_out = os.path.join(output_dir, "6_dalfox_xss.txt")

    start_time = time.time()

    # TAHAP 1: Subfinder
    if use_subfinder:
        cmd_subfinder = f"subfinder -d {target} -all -silent -t 100 -o {subs_file}"
        run_command(cmd_subfinder, f"Subdomain Enumeration ({target})")
        if not check_file_has_data(subs_file):
            print(f"{Colors.FAIL}[!] Gagal menemukan subdomain. Menghentikan proses.{Colors.ENDC}")
            sys.exit(1)
    else:
        print(f"{Colors.BLUE}[*] Melewati Subfinder. Target difokuskan HANYA ke: {args.target}{Colors.ENDC}\n")
        with open(subs_file, 'w') as f:
            f.write(args.target + '\n')

    # TAHAP 2: HTTPX
    current_target_file = subs_file
    if use_httpx:
        if stealth_mode:
            cmd_httpx = f"httpx -l {current_target_file} -silent -threads 10 -rl 20 -random-agent -o {live_file}"
        else:
            cmd_httpx = f"httpx -l {current_target_file} -silent -threads 200 -rl 200 -o {live_file}"
            
        run_command(cmd_httpx, "Validasi Live Hosts (HTTPX)")
        if not check_file_has_data(live_file):
            print(f"{Colors.FAIL}[!] Tidak ada target yang merespon HTTP/HTTPS. Menghentikan proses.{Colors.ENDC}")
            sys.exit(1)
        current_target_file = live_file
    else:
        print(f"{Colors.BLUE}[*] Melewati HTTPX. Menganggap target input sudah aktif (Live).{Colors.ENDC}\n")
        shutil.copy(current_target_file, live_file)
        current_target_file = live_file

    # TAHAP 3: Katana
    if use_katana:
        depth = 5 if deep_scan else 3
        timeout = 20 if deep_scan else 10
        if stealth_mode:
            cmd_katana = f"katana -list {current_target_file} -silent -jc -kf all -d {depth} -c 5 -p 5 -rl 20 -random-agent -ct {timeout} -o {katana_out}"
        else:
            cmd_katana = f"katana -list {current_target_file} -silent -jc -kf all -d {depth} -c 50 -p 50 -ct {timeout} -o {katana_out}"
            
        run_command(cmd_katana, f"Deep Crawling & Endpoint Discovery (Kedalaman: {depth})")

    # TAHAP 4: Nuclei
    if use_nuclei:
        severities = "critical,high,medium,low" if deep_scan else "critical,high,medium"
        if stealth_mode:
            cmd_nuclei = f"nuclei -l {current_target_file} -c 10 -bs 10 -rl 20 -random-agent -severity {severities} -o {nuclei_out}"
        else:
            cmd_nuclei = f"nuclei -l {current_target_file} -c 100 -bs 100 -severity {severities} -o {nuclei_out}"
            
        run_command(cmd_nuclei, f"Vulnerability Scanning ({severities.upper()})")

    # TAHAP 5: Dalfox
    if use_dalfox:
        if check_file_has_data(katana_out):
            has_params = filter_parameters(katana_out, params_out)
            if has_params:
                dalfox_blind = f"-b {args.blind}" if args.blind else ""
                dalfox_deep = "--deep-domxss" if deep_scan else ""
                
                if stealth_mode:
                    cmd_dalfox = f"dalfox file {params_out} {dalfox_blind} {dalfox_deep} --worker 10 --delay 2 -o {dalfox_out}"
                else:
                    cmd_dalfox = f"dalfox file {params_out} {dalfox_blind} {dalfox_deep} --worker 150 -o {dalfox_out}"
                    
                run_command(cmd_dalfox, "Advanced XSS Hunting (Dalfox)")
            else:
                print(f"{Colors.WARNING}[!] Tidak ada URL parameter valid ditemukan dari hasil Katana. Melewati Dalfox.{Colors.ENDC}")
        else:
             print(f"{Colors.WARNING}[!] Hasil crawling Katana kosong. Melewati Dalfox.{Colors.ENDC}")

    # Kalkulasi Waktu
    end_time = time.time()
    duration = round((end_time - start_time) / 60, 2)

    # Ringkasan Eksekusi Dinamis
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}║  [+] PEMINDAIAN TARGET SELESAI ({duration} menit)                ║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    if use_subfinder: print(f" {Colors.BLUE}➔ Subdomains ditemukan : {subs_file}{Colors.ENDC}")
    if use_httpx:     print(f" {Colors.BLUE}➔ Live Hosts divalidasi: {live_file}{Colors.ENDC}")
    if use_katana:    print(f" {Colors.BLUE}➔ URL Endpoint di-crawl: {katana_out}{Colors.ENDC}")
    if use_dalfox:    print(f" {Colors.BLUE}➔ Parameter disaring   : {params_out}{Colors.ENDC}")
    if use_nuclei:    print(f" {Colors.FAIL}➔ Temuan Nuclei        : {nuclei_out}{Colors.ENDC}")
    if use_dalfox:    print(f" {Colors.FAIL}➔ Temuan XSS (Dalfox)  : {dalfox_out}{Colors.ENDC}")
    print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.FAIL}[!] Pemindaian dibatalkan paksa oleh pengguna (Ctrl+C). Keluar dengan aman...{Colors.ENDC}")
        sys.exit(1)
