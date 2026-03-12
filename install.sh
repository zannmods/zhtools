#!/bin/bash
# Skrip instalasi otomatis untuk dependencies Bug Bounty Scanner

echo -e "\e[94m[*] Memulai instalasi dependencies tools (Go diperlukan)...\e[0m"

# Cek apakah Go sudah terinstal
if ! command -v go &> /dev/null
then
    echo -e "\e[91m[!] Go tidak ditemukan! Silakan install golang terlebih dahulu.\e[0m"
    exit 1
fi

echo -e "\e[92m[+] Menginstal Subfinder...\e[0m"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

echo -e "\e[92m[+] Menginstal HTTPX...\e[0m"
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

echo -e "\e[92m[+] Menginstal Katana...\e[0m"
go install github.com/projectdiscovery/katana/cmd/katana@latest

echo -e "\e[92m[+] Menginstal Nuclei...\e[0m"
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

echo -e "\e[92m[+] Menginstal Dalfox...\e[0m"
go install github.com/hahwul/dalfox/v2@latest

echo -e "\e[96m[*] Memperbarui template Nuclei...\e[0m"
nuclei -update-templates

echo -e "\e[92m[✓] Instalasi Selesai! Pastikan folder ~/go/bin sudah masuk ke dalam PATH Anda.\e[0m"
echo -e "\e[93mTips: Jalankan 'export PATH=\$PATH:\$HOME/go/bin' jika tools belum terdeteksi.\e[0m"
