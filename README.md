# zhtools
Credit ZannMods
🕷️ Bug Bounty Automation Scanner (Pro)

Alat otomatisasi reconnaissance dan pemindaian kerentanan tingkat lanjut untuk Bug Bounty Hunters. Skrip ini menggabungkan beberapa tools terbaik di industri untuk melakukan pencarian subdomain, validasi host, crawling mendalam, hingga pemindaian Vuln & XSS secara otomatis.

🚀 Alur Kerja (Workflow)

Pencarian Subdomain (subfinder)

Validasi Live Host (httpx)

Deep Crawling & Endpoint Discovery (katana)

Pemindaian Kerentanan Massal (nuclei)

Pemindaian Blind/Reflected XSS (dalfox)

🛠️ Prasyarat (Prerequisites)

Pastikan kamu menggunakan Linux/macOS dan sudah menginstal Go (golang) dan Python 3.

📥 Instalasi

Clone repository ini:

git clone https://github.com/zannmods/zhtools.git
cd zhtools


Jalankan skrip instalasi untuk mengunduh semua tools pendukung secara otomatis:

chmod +x install.sh
./install.sh


🎯 Cara Penggunaan

Jalankan skrip menggunakan Python 3 dengan parameter domain target:

python3 bounty_scanner.py -d target.com


Opsi Lanjutan (Blind XSS):
Jika kamu menggunakan XSS Hunter atau Interactsh, kamu bisa menambahkan URL blind payload kamu:

python3 bounty_scanner.py -d target.com --blind sukmadic.xss.ht


📁 Output

Semua hasil pemindaian akan disimpan secara terstruktur di dalam folder scans_target.com_[timestamp]/ dengan format yang rapi agar mudah dianalisa.

⚠️ Disclaimer

Gunakan tools ini HANYA pada target di mana kamu memiliki izin (Program Bug Bounty Resmi atau Authorized Pentesting). Pembuat tidak bertanggung jawab atas penyalahgunaan alat ini.
