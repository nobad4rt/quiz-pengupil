# CI/CD Pipeline untuk Pengujian Otomatis Quiz-Pengupil

## Tentang

Repositori ini telah dikonfigurasi dengan GitHub Actions untuk menjalankan pengujian otomatis pada modul Login dan Register secara otomatis setiap kali ada push ke branch `main` atau `master`, atau ketika ada pull request.

## Alur Kerja

Pipeline CI/CD melakukan langkah-langkah berikut:

1. Menyiapkan lingkungan Ubuntu dengan layanan MySQL
2. Menginstal dan mengkonfigurasi PHP 7.4
3. Mengimpor skema database atau membuat tabel sederhana jika skema tidak ditemukan
4. Menjalankan server PHP pada port 8000
5. Menyiapkan Python dan menginstal dependensi dari `requirements.txt`
6. Menginstal Google Chrome dan ChromeDriver yang sesuai
7. Memodifikasi skrip pengujian agar bekerja dengan URL server lokal
8. Menjalankan semua tes menggunakan `run_all_tests.py`
9. Menghasilkan laporan HTML untuk hasil pengujian
10. Mengunggah hasil pengujian (laporan HTML dan tangkapan layar) sebagai artifact

## Manfaat

1. **Pengujian Otomatis**: Tidak perlu menjalankan pengujian secara manual
2. **Konsistensi**: Lingkungan pengujian selalu sama
3. **Deteksi Dini Bug**: Masalah terdeteksi lebih cepat sebelum diintegrasikan ke kode utama
4. **Dokumentasi**: Hasil pengujian tersimpan sebagai artifact di GitHub

## Cara Menggunakan

### Menjalankan Workflow Secara Manual

1. Buka tab "Actions" di repositori GitHub
2. Pilih workflow "Test Automation"
3. Klik tombol "Run workflow"
4. Pilih branch yang ingin diuji dan klik "Run workflow"

### Melihat Hasil Pengujian

1. Buka tab "Actions" di repositori GitHub
2. Pilih workflow run yang telah selesai
3. Scroll ke bawah dan klik "Artifacts"
4. Unduh "test-results" untuk melihat laporan HTML dan tangkapan layar

## Kustomisasi

Jika Anda ingin menyesuaikan konfigurasi pipeline:

1. Edit file `.github/workflows/test-automation.yml`
2. Commit dan push perubahan ke repositori

Untuk mengubah versi PHP, Python, atau konfigurasi database, Anda dapat menyesuaikan parameter di bagian yang sesuai dalam file workflow. 