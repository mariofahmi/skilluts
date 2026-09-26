#!/usr/bin/env python3
"""
fill_uts.py — Mengisi template Soal UTS UNIROW (assets/Template_UTS_UNIROW.docx)
dengan data mata kuliah dan daftar soal, menghasilkan file .docx siap pakai.

Pemakaian:
    py fill_uts.py OUTPUT.docx --data data.json
    py fill_uts.py OUTPUT.docx --data data.json --template /path/to/Template_UTS_UNIROW.docx

Format data.json:
{
  "prodi": "Pendidikan Pancasila dan Kewarganegaraan",
  "dosen": "Dr. Mario Fahmi, M.Pd.",
  "mata_kuliah": "Telaah Kurikulum PPKn",
  "angkt_semester": "2023/6",
  "hari": "Senin",
  "tanggal": "10 November 2026",
  "sifat": "Tutup Buku",
  "waktu": "90 menit",                 // opsional, default "90 menit"
  "soal": [
    {"tipe": "esai", "teks": "Jelaskan landasan filosofis dan yuridis pengembangan Kurikulum OBE 2026 di perguruan tinggi!"},
    {"tipe": "pg", "teks": "Manakah komponen utama dalam penyusunan RPS berbasis OBE?",
     "opsi": ["CPL, CPMK, Sub-CPMK", "Hanya Silabus", "Buku Ajar Tunggal", "Rencana Mingguan Tanpa Asesmen"]}
  ]
}

Field "tipe" boleh "esai" (default jika tidak ditulis) atau "pg" (pilihan ganda,
opsi diberi label a., b., c., ... otomatis).
"""
import argparse
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

RPR_NORMAL = (
    '<w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" '
    'w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/>'
    '<w:szCs w:val="24"/></w:rPr>'
)

FIELD_TOKENS = {
    "prodi": "{{PRODI}}",
    "dosen": "{{DOSEN}}",
    "mata_kuliah": "{{MATA_KULIAH}}",
    "angkt_semester": "{{ANGKT_SEMESTER}}",
    "hari": "{{HARI}}",
    "sifat": "{{SIFAT}}",
    "tanggal": "{{TANGGAL}}",
    "waktu": "{{WAKTU}}",
}

REQUIRED_FIELDS = [
    "prodi", "dosen", "mata_kuliah", "angkt_semester", "hari", "sifat", "tanggal",
]


def xml_escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_question_paragraphs(soal_list):
    """Bangun rangkaian <w:p> untuk daftar soal, menggantikan {{DAFTAR_SOAL}}."""
    paras = []
    for i, item in enumerate(soal_list, start=1):
        tipe = item.get("tipe", "esai").strip().lower()
        teks = xml_escape(item.get("teks", "").strip())

        # Paragraf nomor + teks soal (hanging indent ala nomor urut)
        p = (
            '<w:p><w:pPr><w:spacing w:before="60" w:after="30" w:line="260" w:lineRule="auto"/>'
            '<w:ind w:left="720" w:hanging="360"/>'
            f'{RPR_NORMAL}</w:pPr>'
            f'<w:r>{RPR_NORMAL}<w:t xml:space="preserve">{i}. {teks}</w:t></w:r></w:p>'
        )
        paras.append(p)

        if tipe == "pg":
            opsi = item.get("opsi", [])
            huruf = "abcdefgh"
            for j, opt_text in enumerate(opsi):
                opt_escaped = xml_escape(str(opt_text).strip())
                label = huruf[j] if j < len(huruf) else str(j + 1)
                op = (
                    '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:left="1080" w:hanging="360"/>'
                    f'{RPR_NORMAL}</w:pPr>'
                    f'<w:r>{RPR_NORMAL}<w:t xml:space="preserve">{label}. {opt_escaped}</w:t></w:r></w:p>'
                )
                paras.append(op)
    return "".join(paras)


def fill_template(template_path: Path, data: dict, output_path: Path):
    with tempfile.TemporaryDirectory() as temp_dir_str:
        work_dir = Path(temp_dir_str)
        # 1. Unpack template menggunakan pure Python zipfile (lintas OS: Windows, Mac, Linux)
        with zipfile.ZipFile(template_path, "r") as zin:
            zin.extractall(work_dir)

        doc_xml_path = work_dir / "word" / "document.xml"
        if not doc_xml_path.exists():
            raise FileNotFoundError(f"document.xml tidak ditemukan di dalam {template_path}")
        xml = doc_xml_path.read_text(encoding="utf-8")

        # 2. Isi field header
        data.setdefault("waktu", "90 menit")
        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            raise ValueError(f"Field wajib belum diisi: {', '.join(missing)}")

        for field, token in FIELD_TOKENS.items():
            value = xml_escape(str(data.get(field, "")))
            if token not in xml:
                raise ValueError(f"Token {token} tidak ditemukan di template — template mungkin rusak/berubah")
            xml = xml.replace(token, value, 1)

        # 3. Isi daftar soal
        soal_list = data.get("soal", [])
        if not soal_list:
            raise ValueError("Field 'soal' kosong — minimal satu soal diperlukan")
        question_xml = build_question_paragraphs(soal_list)
        if "{{DAFTAR_SOAL}}" not in xml:
            raise ValueError("Token {{DAFTAR_SOAL}} tidak ditemukan di template")
        
        # Ganti seluruh paragraf marker (bukan hanya teksnya) dengan paragraf-paragraf soal
        marker_pattern = re.compile(r'<w:p[^>]*>(?:(?!<w:p[ >]).)*?\{\{DAFTAR_SOAL\}\}.*?</w:p>', re.DOTALL)
        xml, n = marker_pattern.subn(question_xml, xml, count=1)
        if n == 0:
            raise ValueError("Gagal mengganti paragraf marker {{DAFTAR_SOAL}}")

        doc_xml_path.write_text(xml, encoding="utf-8")

        # 4. Kemas ulang jadi .docx via zipfile (preserves all styles, images, and anchors)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists():
            output_path.unlink()
        
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for file_path in work_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(work_dir)
                    zout.write(file_path, arcname)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("output", help="Path file .docx hasil akhir")
    ap.add_argument("--data", required=True, help="Path file JSON berisi data mata kuliah & soal")
    ap.add_argument(
        "--template",
        default=str(Path(__file__).resolve().parent.parent / "assets" / "Template_UTS_UNIROW.docx"),
        help="Path template dasar (default: assets/Template_UTS_UNIROW.docx di dalam skill ini)",
    )
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    template_path = Path(args.template)
    if not template_path.exists():
        sys.exit(f"Template tidak ditemukan: {template_path}")

    output_path = Path(args.output)
    fill_template(template_path, data, output_path)
    print(f"Selesai: {output_path}")


if __name__ == "__main__":
    main()
