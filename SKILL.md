---
name: uts-unirow
description: >
  Membuat dokumen SOAL UJIAN TENGAH SEMESTER (UTS) resmi Universitas PGRI
  Ronggolawe (UNIROW) Tuban, FKIP, sebagai file .docx sesuai template resmi
  kampus (logo UNIROW, kop surat, tabel Prodi/Dosen/Mata kuliah/Waktu/Angkt-
  Semester/Hari/Sifat/Tanggal, instruksi, penutup "SELAMAT MENGERJAKAN").
  Gunakan setiap kali pengguna minta "soal UTS", "ujian tengah semester",
  "buatkan UTS", "susun soal UTS" untuk UNIROW/Ronggolawe Tuban/FKIP — baik
  saat sudah punya soal sendiri tinggal diformat, maupun minta dibantu
  MENYUSUN soal esai/PG dari topik/RPS. Juga saat mengunggah contoh naskah
  UTS lama minta versi baru, atau merevisi naskah UTS yang sudah ada.
  WAJIB dipakai juga ketika pengguna hanya mengunggah Kontrak Kuliah, RPS,
  dan/atau draft soal lalu minta dibuatkan UTS — skill membaca sendiri
  dokumen tsb untuk mengambil Prodi/Dosen/Mata kuliah/materi dan menyusun
  soal, tanpa pengguna perlu mengetik ulang data manual.
---

# Soal UTS Universitas PGRI Ronggolawe (UNIROW) Tuban

Skill ini menghasilkan file `.docx` yang identik secara visual dengan
template resmi Soal UTS UNIROW FKIP — lengkap dengan kop surat, logo kampus,
dan tabel identitas mata kuliah — berdasarkan analisis XML mendalam terhadap
contoh asli.

**Jangan coba membangun ulang dokumen ini dari nol dengan `docx` (npm)/
docx-js.** Kop suratnya memuat logo ber-anchor (floating image) yang sulit
direplikasi dari kode dan gampang rusak. Alih-alih, gunakan
`assets/Template_UTS_UNIROW.docx` — salinan template asli dengan field yang
berubah-ubah sudah ditandai token `{{...}}` — lalu isi dengan
`scripts/fill_uts.py`. Pendekatan ini menjamin kop, logo, dan formatting
selalu identik dengan aslinya.

Peta lengkap semua token & struktur tabel: `references/placeholder_map.md`
(baca ini jika perlu memahami detail lebih dalam atau template perlu
diperbarui).

---

## Cara membuat soal UTS baru

### 1. WAJIB baca dulu dokumen yang diunggah pengguna, sebelum bertanya apa pun

Pengguna sering hanya mengunggah **Kontrak Kuliah**, **RPS**, dan/atau
**draft soal lama** dan berharap skill ini mengambil sendiri semua data
yang dibutuhkan — jangan langsung menembak pertanyaan ke pengguna kalau
datanya sebenarnya sudah ada di dokumen yang mereka unggah.

Untuk setiap file yang diunggah, gunakan skill `file-reading` (dan `docx`
untuk `.docx`) untuk membacanya (`extract-text <file>`), lalu ambil apa
yang relevan:

- **Kontrak Kuliah** biasanya memuat: nama mata kuliah, kode MK, sks,
  Prodi, semester, nama Dosen Pengampu, deskripsi/CPMK/topik mingguan,
  dan kadang komponen penilaian (bisa jadi acuan bobot/cakupan UTS).
- **RPS** (kalau sama seperti template `rps-unirow`) memuat: Prodi, Mata
  Kuliah, CPL/CPMK/Sub-CPMK, rencana 16 minggu (materi tiap minggu, biasa
  UTS mencakup minggu 1–7/8) — pakai bagian **materi minggu 1 s.d. sebelum
  UTS** sebagai cakupan/bahan acuan untuk menyusun soal, dan **Sub-CPMK**
  terkait sebagai acuan tingkat kompetensi yang diuji.
- **Draft soal lama** (docx/teks apa pun): ekstrak daftar soal apa adanya
  (dan opsi PG jika ada) untuk diformat ulang ke template — jangan mengubah
  substansi soal kecuali pengguna minta direvisi/dilengkapi.

Isi field `prodi`, `dosen`, `mata_kuliah`, dan (jika tersedia)
`angkt_semester` langsung dari dokumen-dokumen ini tanpa bertanya lagi ke
pengguna. Sebutkan singkat ke pengguna field mana yang diambil otomatis
dari dokumen mana, supaya mereka bisa mengoreksi kalau salah ambil.

### 2. Baru tanyakan ke pengguna apa yang benar-benar belum ada

Setelah dokumen dibaca, biasanya yang **tidak** tercantum di Kontrak
Kuliah/RPS (dan karena itu wajib ditanyakan, jangan mengarang) adalah:

- **Hari** dan **Tanggal** pelaksanaan ujian yang sebenarnya (jadwal UTS
  biasanya ditentukan belakangan oleh kampus, bukan bagian dari RPS/Kontrak
  Kuliah).
- **Sifat ujian** (mis. "Tutup Buku", "Buka Buku", "Take Home").
- **Waktu** pengerjaan, jika bukan default 90 menit.
- Konfirmasi **jenis soal**: esai, pilihan ganda (PG), atau campuran, dan
  berapa jumlah soal yang diinginkan — kecuali draft soal lama sudah
  menjawab ini.
- Jika Kontrak Kuliah/RPS tidak memuat Prodi/Dosen/Mata kuliah sama sekali
  (dokumen tidak lengkap atau tidak diunggah), baru tanyakan field itu.

Fakultas **selalu FKIP** (Fakultas Keguruan dan Ilmu Pendidikan) — skill
ini tidak mendukung fakultas lain, dan tidak perlu ditanyakan. Skill ini
juga **tidak menyertakan kunci jawaban/rubrik** — hanya lembar soal murni.

### 3. Susun/ekstrak soal

Jika pengguna minta dibantu menyusun soal dari topik/RPS, susun soal yang
relevan dengan materi & Sub-CPMK yang diambil di langkah 1, jelas, dan
sesuai tingkat kesulitan UTS (jangan terlalu mudah/sulit tanpa arahan),
dalam Bahasa Indonesia formal akademik (kecuali mata kuliah berbahasa
asing, mis. Bahasa Inggris, di mana soal boleh dalam bahasa tersebut jika
pengguna memintanya). Jika pengguna mengunggah draft soal lama, gunakan
soal tersebut apa adanya (atau sesuai revisi yang diminta).

### 4. Susun data JSON

Buat file JSON (lihat format lengkap di docstring `scripts/fill_uts.py`)
berisi field berikut:

```json
{
  "prodi": "...",
  "dosen": "...",
  "mata_kuliah": "...",
  "angkt_semester": "...",
  "hari": "...",
  "tanggal": "...",
  "sifat": "...",
  "waktu": "90 menit",
  "soal": [
    {"tipe": "esai", "teks": "..."},
    {"tipe": "pg", "teks": "...", "opsi": ["...", "...", "...", "..."]}
  ]
}
```

`tipe` boleh `"esai"` (default) atau `"pg"`. Field `waktu` opsional (default
"90 menit" jika tidak diisi).

### 5. Jalankan script pengisi

```bash
cd /mnt/skills/user/uts-unirow   # atau lokasi skill ini terpasang
python3 scripts/fill_uts.py /mnt/user-data/outputs/UTS_<Nama_MK>.docx --data data.json
```

(Ganti path skill sesuai lokasi instalasi aktual — cek dulu dengan `view`
pada direktori skill jika path di atas tidak ditemukan. Path template default
sudah menunjuk ke `assets/Template_UTS_UNIROW.docx` relatif terhadap lokasi
`scripts/fill_uts.py`, tidak perlu diberikan manual kecuali template dipindah.)

### 6. Selalu verifikasi hasil secara visual sebelum diserahkan ke pengguna

```bash
python3 /mnt/skills/public/docx/scripts/office/soffice.py --headless \
  --convert-to pdf /mnt/user-data/outputs/UTS_<Nama_MK>.docx
pdftoppm -jpeg -r 120 /mnt/user-data/outputs/UTS_<Nama_MK>.pdf /tmp/preview
```

Lalu `view` gambar `/tmp/preview-1.jpg` (dan halaman berikutnya jika lebih
dari satu halaman) dan periksa:

- Kop surat, logo, dan tabel identitas tidak rusak/bergeser
- Semua field identitas terisi benar (tidak ada token `{{...}}` tersisa)
- Soal bernomor urut 1, 2, 3, ... dengan benar
- Opsi PG (jika ada) berlabel a., b., c., ... dan tidak terpotong
- "SELAMAT MENGERJAKAN" tetap muncul di akhir

Jika ada yang salah, perbaiki data JSON atau `scripts/fill_uts.py`, lalu
ulangi langkah 5–6. Jika skrip gagal karena token tidak ditemukan
("Token ... tidak ditemukan di template"), kemungkinan
`assets/Template_UTS_UNIROW.docx` rusak/berubah — jangan mencoba menambal
manual, laporkan ke pengguna.

### 7. Serahkan file

Salin/pastikan file akhir ada di `/mnt/user-data/outputs/` dengan nama jelas
(misal `UTS_Reading_Comprehension.docx`), lalu panggil `present_files`.

---

## Aturan Konten Penting (jangan dilanggar)

- **Fakultas selalu "FAKULTAS KEGURUAN DAN ILMU PENDIDIKAN"** — jangan
  diubah, sesuai keputusan eksplisit pengguna.
- **Tidak menyertakan kunci jawaban atau rubrik penilaian** dalam dokumen
  ini — jika pengguna kemudian minta kunci jawaban/rubrik, itu di luar
  cakupan skill ini; buat sebagai dokumen terpisah dan beri tahu pengguna.
- Jangan mengarang nama dosen, prodi, atau tanggal jika pengguna belum
  memberikannya — tanyakan dulu.
- Total soal disesuaikan kebutuhan pengguna; jika tidak disebutkan jumlah,
  tanyakan atau gunakan jumlah wajar untuk UTS (4–6 soal esai, atau
  campuran esai+PG secukupnya).
- Bahasa dokumen: Bahasa Indonesia formal akademik, kecuali soal memang
  untuk mata kuliah bahasa asing.

## Spesifikasi Halaman & Template (referensi cepat)

| Aspek | Nilai |
|---|---|
| Ukuran kertas | A4 (11906×16838 DXA) |
| Margin | top 1133 DXA, sisi lain 1440 DXA |
| Font | Times New Roman, 12pt body |
| Logo | `word/media/image1.png` di dalam template — logo UNIROW, jangan diganti |
| Fakultas | Selalu FKIP (tetap, tidak bisa diganti field lain) |

Detail lengkap peta token → lokasi & format soal ada di
`references/placeholder_map.md` — baca file itu jika perlu memahami atau
memperbarui template.
