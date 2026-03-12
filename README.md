# 🕷️ zhtools: Bug Bounty Automation Scanner (Pro)
> **Author:** [ZannMods](https://github.com/zannmods)  
> **Version:** 1.0.0 (Pro Edition)

`zhtools` adalah framework otomatisasi reconnaissance dan pemindaian kerentanan tingkat lanjut yang dirancang khusus untuk **Bug Bounty Hunters**. Alat ini mengintegrasikan tool standar industri ke dalam satu alur kerja (workflow) yang mulus.

---

## 🚀 Alur Kerja (Workflow)
Skrip ini mengotomatiskan proses dari nol hingga pelaporan:
1.  **Subdomain Discovery** 🔍 (subfinder) - Mencari aset yang tersembunyi.
2.  **Live Host Validation** ✅ (httpx) - Memastikan target aktif dan responsif.
3.  **Deep Crawling** 🕸️ (katana) - Mengambil seluruh endpoint dan URL sensitif.
4.  **Vulnerability Scanning** 🛡️ (nuclei) - Pemindaian massal template CVE & Misconfig.
5.  **XSS Analysis** ⚡ (dalfox) - Pengujian Reflected & Blind XSS secara mendalam.

---

## 🛠️ Prasyarat (Prerequisites)
Pastikan sistem Anda (Linux/macOS) sudah terpasang:
* **Go** (Golang) versi terbaru.
* **Python 3.x**
* Akses Internet yang stabil.

---

## 📥 Instalasi
Cukup jalankan perintah berikut untuk menyiapkan lingkungan kerja Anda:

```bash
# Clone repository
git clone [https://github.com/zannmods/zhtools.git](https://github.com/zannmods/zhtools.git)
cd zhtools

# Berikan izin eksekusi pada installer
chmod +x install.sh

# Jalankan instalasi otomatis
./install.sh
