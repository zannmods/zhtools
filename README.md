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
git clone https://github.com/zannmods/zhtools.git
cd zhtools

# Berikan izin eksekusi pada installer
chmod +x install.sh

# Jalankan instalasi otomatis
./install.sh
```
## 🎯 Cara Penggunaan
cara penggunaan tools nya

```bash
#command standar
python3 zhbun.py -d target.com
```
```bash
python3 zhbun.py -d target.com --blind username.xss.ht
```

## ⚠️ Disclaimer
**PENTING:** Alat ini dibuat untuk tujuan pendidikan dan program Bug Bounty yang sah. Penggunaan alat ini pada target tanpa izin tertulis adalah ilegal. Penulis **ZannMods** tidak bertanggung jawab atas segala penyalahgunaan atau kerusakan yang disebabkan oleh alat ini.
