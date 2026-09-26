# Skill Soal UTS UNIROW Tuban (FKIP)

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://github.com/mariofahmi/skilluts)
[![Template](https://img.shields.io/badge/Template-UNIROW%20FKIP-red.svg)](https://unirow.ac.id)
[![Kurikulum](https://img.shields.io/badge/Kurikulum-OBE%202026-green.svg)](https://unirow.ac.id)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Skill resmi dan agen otomatisasi **Google Antigravity & Agentic AI** untuk menyusun dan menerbitkan naskah **Soal Ujian Tengah Semester (UTS)** resmi Fakultas Keguruan dan Ilmu Pendidikan (FKIP), Universitas PGRI Ronggolawe (UNIROW) Tuban berbasis kurikulum Outcome-Based Education (OBE) 2026.

---

## 🌟 Fitur Utama

1. **Preservasi 100% Format Resmi Dokumen:**
   - Mempertahankan integritas XML dokumen asli (`Template_UTS_UNIROW.docx`), termasuk **Kop Surat resmi**, **Logo ber-anchor (floating image)**, dan penataan tabel identitas mata kuliah tanpa risiko file rusak (*corrupted*).
2. **Ekstraksi Cerdas Otomatis dari Berkas RPS / Kontrak Kuliah:**
   - AI membaca langsung Program Studi, Nama Mata Kuliah, Dosen Pengembang RPS (tabel otorisasi), Angkatan/Semester, dan materi Sub-CPMK Minggu 1 s.d. 7.
3. **Penyusunan Soal Berbobot Taksonomi Bloom (C2–C6):**
   - Menghasilkan butir soal esai berkualitas akademik tinggi (Pemahaman Konseptual, Analisis Asas, Tinjauan Komparatif, Evaluasi Kasus Kontemporer, dan Solusi Aplikatif).
4. **Dukungan Soal Esai dan Pilihan Ganda (PG):**
   - Mendukung format soal esai dengan *hanging indent* nomor urut otomatis, serta pilihan ganda dengan label opsi `a., b., c., d.` yang rapi.
5. **Lintas Platform (Pure Python):**
   - Menggunakan modul standar bawaan Python (`zipfile` & `tempfile`), berjalan lancar di Windows, macOS, dan Linux tanpa ketergantungan *tool* `unzip`/`zip` CLI.

---

## 📁 Struktur Direktori

```text
skilluts/
├── .gitignore
├── LICENSE (MIT)
├── README.md                          # Dokumentasi resmi
├── SKILL.md                           # Konfigurasi skill Antigravity IDE
├── assets/
│   └── Template_UTS_UNIROW.docx       # Template master resmi UNIROW FKIP
├── references/
│   └── placeholder_map.md             # Pemetaan token XML {{...}}
└── scripts/
    └── fill_uts.py                    # Engine pengisi template lintas platform
```

---

## 🚀 Cara Penggunaan

### 1. Di Lingkungan Antigravity IDE (Slash Command)

Ketik salah satu slash command berikut pada antarmuka chat:
```text
/uts @RPS_Mata_Kuliah.docx
```
atau:
```text
/uts-unirow "Hukum Tata Negara"
```

AI akan secara otomatis membaca materi Sub-CPMK pertemuan 1–7, menyusun naskah soal, dan memproduksi file `.docx` siap cetak.

### 2. Eksekusi Melalui Python CLI

Anda juga dapat menjalankan skrip generator secara langsung melalui terminal:

```bash
# Sintaks umum
py scripts/fill_uts.py "Naskah_UTS_Hasil.docx" --data "data_ujian.json"
```

---

## 📝 Format Data Input (`data.json`)

```json
{
  "prodi": "Pendidikan Pancasila dan Kewarganegaraan",
  "dosen": "Dr. Sukisno, M.Pd.",
  "mata_kuliah": "Telaah Kurikulum PPKn",
  "angkt_semester": "2023/6",
  "hari": "Senin",
  "tanggal": "10 November 2026",
  "sifat": "Tutup Buku",
  "waktu": "90 menit",
  "soal": [
    {
      "tipe": "esai",
      "teks": "Jelaskan secara komprehensif konsep dasar, hakikat, dan 4 dimensi kurikulum!"
    },
    {
      "tipe": "pg",
      "teks": "Manakah komponen utama evaluasi dalam kurikulum berbasis Outcome-Based Education (OBE)?",
      "opsi": [
        "Rubrik Penilaian Kinerja Otentik",
        "Ujian Hafalan Teoretis Semata",
        "Presensi Kehadiran Kuliah",
        "Tinjauan Silabus Tanpa Bukti Asesmen"
      ]
    }
  ]
}
```

---

## 📦 Instalasi ke Workspace Antigravity

Untuk menginstal skill ini ke workspace lokal Anda:

```bash
git clone https://github.com/mariofahmi/skilluts.git .agents/skills/uts-unirow
```

---

## 🏛️ Lisensi & Hak Cipta
Didistribusikan di bawah lisensi [MIT License](LICENSE).  
Dikembangkan untuk Program Studi PPKn & Fakultas Keguruan dan Ilmu Pendidikan (FKIP), **Universitas PGRI Ronggolawe (UNIROW) Tuban**.
