# Konfigurasi CI/CD

Folder ini berisi file konfigurasi tambahan untuk mendukung proses CI/CD di GitHub Actions.

## File Konfigurasi

- `setup-ci.sh`: Script bash untuk penyiapan lingkungan CI/CD tambahan

## Petunjuk Penggunaan

1. File-file di folder ini tidak perlu dijalankan secara manual
2. GitHub Actions akan otomatis menggunakan file-file ini saat workflow berjalan

## Memodifikasi CI/CD

Jika Anda perlu memodifikasi konfigurasi CI/CD:

1. Edit file `.github/workflows/test-automation.yml` untuk mengubah alur kerja utama
2. Edit script di folder ini untuk mengubah langkah-langkah persiapan

## Lingkungan CI/CD

Pipeline CI/CD berjalan dalam lingkungan Ubuntu dengan:

- PHP 7.4
- MySQL 5.7
- Python 3.9
- Chrome browser terbaru
- ChromeDriver yang kompatibel

## Dependensi

Dependensi Python yang dibutuhkan didefinisikan di `requirements.txt` di folder utama.

## Output

Output dari CI/CD workflow:

1. Log pengujian lengkap
2. Laporan hasil pengujian dalam format HTML
3. Screenshot otomatis selama pengujian
4. Status lulus/gagal yang terintegrasi dengan GitHub 