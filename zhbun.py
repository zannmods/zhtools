#!/usr/bin/env python3
"""
Advanced Bug Bounty Automation Framework (PRO VERSION)
Workflow: Subfinder -> HTTPX -> Katana (Crawling) -> Nuclei & Dalfox

Mewajibkan tools terinstal:
- subfinder (go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest)
- httpx     (go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest)
- katana    (go install github.com/projectdiscovery/katana/cmd/katana@latest)
- nuclei    (go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest)
- dalfox    (go install github.com/hahwul/dalfox/v2@latest)
"""

import os
import sys
import subprocess
import argparse
import time
import shutil
from datetime import datetime

# Definisi Warna untuk output Terminal yang lebih tajam
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║          BUG BOUNTY AUTOMATION SCANNER - PRO v2.0            ║
    ║  Workflow: Enum -> Probe -> Crawl -> Vuln Scan -> XSS Hunt   ║
    ╚══════════════════════════════════════════════════════════════╝
    {Colors.ENDC}"""
    print(banner)

def check_dependencies():
    """Memeriksa dengan akurat apakah tools yang dibutuhkan ada di PATH."""
    tools = ['subfinder', 'httpx', 'katana', 'nuclei', 'dalfox']
    missing = []
    print(f"{Colors.BLUE}[*] Memeriksa dependensi tools inti...{Colors.ENDC}")
    
    for tool in tools:
        if shutil.which(tool) is None:
            missing.append(tool)
        else:
            print(f"{Colors.GREEN}  [+] {tool} {Colors.ENDC}terdeteksi.")
    
    if missing:
        print(f"\n{Colors.FAIL}[!] EROR: Tools berikut tidak ditemukan di PATH: {', '.join(missing)}{Colors.ENDC}")
        print(f"{Colors.WARNING}Silakan install tools yang kurang menggunakan 'go install' dan pastikan folder ~/go/bin masuk ke PATH.{Colors.ENDC}")
        sys.exit(1)
    print("")

def run_command(command, description):
    """Menjalankan perintah shell secara realtime dan menangkap return code."""
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
        
        # Cetak output secara realtime
        for line in process.stdout:
            print(line.strip())
            
        process.wait()
        
        if process.returncode == 0:
            print(f"{Colors.GREEN}\n[✓] Selesai: {description}{Colors.ENDC}\n")
            return True
        else:
            print(f"{Colors.FAIL}\n[✗] Gagal/Error pada: {description} (Exit Code: {process.returncode}){Colors.ENDC}\n")
            return False
            
    except Exception as e:
        print(f"{Colors.FAIL}[!] Exception sistem saat menjalankan {description}: {str(e)}{Colors.ENDC}\n")
        return False

def filter_parameters(katana_out, params_out):
    """Menyaring URL hasil crawling yang hanya memiliki parameter (mengandung ? dan =)"""
    print(f"{Colors.BLUE}[*] Menyaring URL dengan parameter untuk Dalfox...{Colors.ENDC}")
    count = 0
    try:
        with open(katana_out, 'r') as infile, open(params_out, 'w') as outfile:
            for line in infile:
                url = line.strip()
                if '?' in url and '=' in url:
                    outfile.write(url + '\n')
                    count += 1
        print(f"{Colors.GREEN}  [+] Ditemukan {count} URL berparameter.{Colors.ENDC}\n")
        return count > 0
    except FileNotFoundError:
        print(f"{Colors.FAIL}[!] File output Katana tidak ditemukan untuk disaring.{Colors.ENDC}")
        return False

def check_file_has_data(filepath):
    """Memeriksa apakah file ada dan tidak kosong."""
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def main():
    parser = argparse.ArgumentParser(description="Pro Bug Bounty Automation Framework")
    parser.add_argument("-d", "--domain", help="Target domain utama (contoh: target.com)", required=True)
    parser.add_argument("-o", "--output", help="Nama awalan folder output", default="scans")
    parser.add_argument("--blind", help="URL XSS Hunter / Interactsh untuk Blind XSS Dalfox", default="")
    args = parser.parse_args()

    domain = args.domain
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"{args.output}_{domain}_{timestamp}"

    print_banner()
    check_dependencies()

    # Membuat direktori hasil
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

    # TAHAP 1: Subfinder (Pencarian Subdomain dengan flag -all untuk hasil maksimal)
    cmd_subfinder = f"subfinder -d {domain} -all -silent -o {subs_file}"
    run_command(cmd_subfinder, f"Subdomain Enumeration ({domain})")

    if not check_file_has_data(subs_file):
        print(f"{Colors.FAIL}[!] Gagal menemukan subdomain. Target mungkin terlalu kecil atau salah. Menghentikan proses.{Colors.ENDC}")
        sys.exit(1)

    # TAHAP 2: HTTPX (Mencari Host yang Aktif dengan multi-threading)
    cmd_httpx = f"httpx -l {subs_file} -silent -threads 100 -o {live_file}"
    run_command(cmd_httpx, "Validasi Live Hosts (HTTPX)")

    if not check_file_has_data(live_file):
        print(f"{Colors.FAIL}[!] Tidak ada subdomain yang merespon HTTP/HTTPS. Menghentikan proses.{Colors.ENDC}")
        sys.exit(1)

    # TAHAP 3: Katana (Crawling Endpoint Lanjutan)
    # -jc (javascript parsing), -kf all (known files)
    cmd_katana = f"katana -list {live_file} -silent -jc -kf all -depth 3 -o {katana_out}"
    run_command(cmd_katana, "Deep Crawling & Endpoint Discovery (Katana)")

    # TAHAP 4: Nuclei (Pemindaian Kerentanan Skala Penuh)
    # Scan langsung ke live hosts, batasi ke tingkat risiko medium hingga critical
    cmd_nuclei = f"nuclei -l {live_file} -c 50 -severity critical,high,medium -o {nuclei_out}"
    run_command(cmd_nuclei, "Vulnerability Scanning (Nuclei)")

    # TAHAP 5: Dalfox (Spesifik mencari XSS pada URL berparameter)
    if check_file_has_data(katana_out):
        has_params = filter_parameters(katana_out, params_out)
        
        if has_params:
            dalfox_blind_flag = f"-b {args.blind}" if args.blind else ""
            cmd_dalfox = f"dalfox file {params_out} {dalfox_blind_flag} -o {dalfox_out}"
            run_command(cmd_dalfox, "Advanced XSS Hunting (Dalfox)")
        else:
            print(f"{Colors.WARNING}[!] Tidak ada URL dengan parameter yang ditemukan. Melewati Dalfox XSS Scan.{Colors.ENDC}")
    else:
         print(f"{Colors.WARNING}[!] Hasil crawling Katana kosong. Melewati Dalfox XSS Scan.{Colors.ENDC}")

    # Kalkulasi Waktu
    end_time = time.time()
    duration = round((end_time - start_time) / 60, 2)

    # Ringkasan Eksekusi
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}║  [+] PEMINDAIAN TARGET SELESAI ({duration} menit)                ║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}")
    print(f" {Colors.BLUE}➔ Subdomains ditemukan : {subs_file}{Colors.ENDC}")
    print(f" {Colors.BLUE}➔ Live Hosts divalidasi: {live_file}{Colors.ENDC}")
    print(f" {Colors.BLUE}➔ URL Endpoint di-crawl: {katana_out}{Colors.ENDC}")
    print(f" {Colors.BLUE}➔ Parameter disaring   : {params_out}{Colors.ENDC}")
    print(f" {Colors.FAIL}➔ Temuan Nuclei        : {nuclei_out}{Colors.ENDC}")
    print(f" {Colors.FAIL}➔ Temuan XSS (Dalfox)  : {dalfox_out}{Colors.ENDC}")
    print(f"{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.FAIL}[!] Pemindaian dibatalkan paksa oleh pengguna (Ctrl+C). Keluar dengan aman...{Colors.ENDC}")
        sys.exit(1)
