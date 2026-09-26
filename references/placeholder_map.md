# Peta Placeholder — Template_UTS_UNIROW.docx

Template ini adalah salinan persis dari contoh resmi UTS FKIP UNIROW
(`1790394422477_UAS_Angkt_2022_seminar.docx`), dengan seluruh sel isian yang
tadinya kosong / berisi contoh, diganti token `{{...}}` agar bisa dicari &
diganti secara aman lewat `scripts/fill_uts.py`.

## Struktur dokumen

1. **Kop surat** (tetap, jangan diubah): logo UNIROW (grouped image, anchored),
   "UJIAN TENGAH SEMESTER", "TAHUN AKADEMIK 2025/2026", nama kampus, alamat,
   telp/fax, website, email.
2. **Baris fakultas** (tetap): "FAKULTAS KEGURUAN DAN ILMU PENDIDIKAN" —
   sesuai konfirmasi pengguna, skill ini **selalu** memakai FKIP dan tidak
   menyediakan opsi mengganti fakultas lain.
3. **Tabel info** (2 kolom kiri-kanan × 4 baris):

   | Token | Label kolom kiri | Token | Label kolom kanan |
   |---|---|---|---|
   | `{{PRODI}}` | Prodi | `{{DOSEN}}` | Dosen |
   | `{{MATA_KULIAH}}` | Mata kuliah | `{{WAKTU}}` | Waktu |
   | `{{ANGKT_SEMESTER}}` | Angkt/Semester | `{{HARI}}` | Hari |
   | `{{SIFAT}}` | Sifat | `{{TANGGAL}}` | Tanggal |

   `{{WAKTU}}` defaultnya diisi `"90 menit"` oleh script jika field `waktu`
   tidak diberikan di data JSON (sesuai nilai asli di contoh).
4. **Instruksi** (tetap): *"Jawablah pertanyaan dibawah ini dengan benar"*
   (italic, underline, bold).
5. **`{{DAFTAR_SOAL}}`** — satu paragraf marker tunggal yang digantikan
   `scripts/fill_uts.py` dengan seluruh paragraf soal (esai bernomor, atau
   PG bernomor + opsi berlabel a./b./c./...). Lihat docstring
   `fill_uts.py` untuk format data JSON lengkap.
6. **Penutup** (tetap): "SELAMAT MENGERJAKAN" (bold, center).

## Label baku yang TIDAK boleh diubah

`FAKULTAS KEGURUAN DAN ILMU PENDIDIKAN`, label kolom (`Prodi`, `Dosen`,
`Mata kuliah`, `Waktu`, `Angkt/Semester`, `Hari`, `Sifat`, `Tanggal`),
kalimat instruksi, dan "SELAMAT MENGERJAKAN".

## Detail teknis

| Parameter | Nilai |
|---|---|
| Ukuran kertas | A4 — 11906×16838 DXA |
| Margin | top 1133, kanan/kiri/bawah 1440 DXA |
| Font | Times New Roman, 12pt (sz=24) untuk isi, 16pt (sz=32) untuk "UJIAN TENGAH SEMESTER" & nama kampus |
| Logo | `word/media/image1.png` — logo UNIROW, anchored di kop, jangan diganti/dipindah |
| Soal esai | Numbered `1. `, `2. `, dst., hanging indent 720/360 DXA |
| Opsi PG | Berlabel `a.`, `b.`, `c.`, ... otomatis dari urutan list `opsi`, indent 1080/360 DXA |

## Keterbatasan

- Skill ini tidak menyertakan kunci jawaban/rubrik penilaian (sesuai
  keputusan pengguna) — hanya lembar soal.
- Fakultas selalu FKIP; jika suatu saat perlu mendukung fakultas lain,
  baris fakultas perlu dijadikan token baru (`{{FAKULTAS}}`) dan
  `fill_uts.py` diperbarui.
- Jika template resmi kampus berubah di kemudian hari, ulangi proses
  penandaan token pada file contoh baru (unzip → cari paraId sel kosong →
  sisipkan `<w:r>` berisi token → rezip), lalu perbarui
  `assets/Template_UTS_UNIROW.docx`.
