## Quiz Pengujian Piranti Lunak 

Diperlukan Stub untuk menguji modul

# Modul #

- Login
- Register

# Requirement #

- PHP
- MySQL

# Installasi #

- Clone atau download repository ini ke folder htdocs di komputer
- Import file sql database yang berada pada folder db

# Test Selenium untuk Quiz-Pengupil

Repository ini berisi script Selenium untuk menguji modul login dan register dari aplikasi Quiz-Pengupil.

## Prasyarat

1. PHP 7.4 atau lebih baru
2. MySQL/MariaDB
3. Python 3.7 atau lebih baru
4. Browser Chrome atau Firefox
5. Web server lokal (Apache/XAMPP/WAMP)

## Instalasi

1. Pastikan aplikasi Quiz-Pengupil sudah diinstal dan berjalan di web server lokal
2. Instal dependensi Python:

   ```
   pip install -r requirements.txt
   ```

3. Persiapkan database untuk testing:

   ```
   php setup_test_db.php
   ```

4. Pastikan ChromeDriver tersedia di folder `chromedriver-win64`:
   - Test akan otomatis menggunakan ChromeDriver di folder `chromedriver-win64/chromedriver.exe`
   - Jika tidak tersedia, test akan mencoba menggunakan webdriver-manager (fallback)

## Struktur File

- `test_login_module.py` - Test case untuk modul login.php
- `test_register_module.py` - Test case untuk modul register.php
- `run_all_tests.py` - Script untuk menjalankan semua test sekaligus
- `setup_test_db.php` - Script persiapan database

## Test Case yang Diimplementasikan

### Modul Login (login.php)

1. **Test Case 1**: Login dengan Username dan Password Valid
   - Verifikasi redirect ke index.php
   - Verifikasi session username terisi

2. **Test Case 2**: Login dengan Username Tidak Terdaftar
   - Verifikasi pesan error "Register User Gagal !!"
   - Verifikasi session tidak terbentuk

3. **Test Case 3**: Login dengan Password Salah
   - Verifikasi login ditolak
   - Verifikasi session tidak terbentuk

4. **Test Case 4**: Field Kosong
   - Verifikasi pesan error "Data tidak boleh kosong !!"

5. **Test Case 5**: SQL Injection pada Input
   - Verifikasi login ditolak untuk input `' OR 1=1 --`

6. **Test Case 6**: Redirect Jika Sudah Login
   - Verifikasi redirect langsung ke index.php

### Modul Register (register.php)

1. **Test Case 1**: Registrasi dengan Data Valid
   - Verifikasi data tersimpan (redirect ke index.php)
   - Verifikasi session aktif

2. **Test Case 2**: Password dan Re-Password Tidak Sama
   - Verifikasi pesan error "Password tidak sama !!"

3. **Test Case 3**: Username Sudah Terdaftar
   - Verifikasi pesan error "Username sudah terdaftar !!"

4. **Test Case 4**: Field Kosong
   - Verifikasi pesan error "Data tidak boleh kosong !!"

5. **Test Case 5**: SQL Injection pada Input
   - Verifikasi SQL injection `'; DROP TABLE users; --` gagal
   - Verifikasi tabel users tetap ada

6. **Test Case 6**: Validasi Email Tidak Ada
   - Verifikasi sistem menerima email tidak valid (bug potensial)

7. **Test Case 7**: Bug pada Query INSERT
   - Verifikasi respon sistem terhadap bug variabel $nama vs $name

## Menjalankan Test

### Opsi 1: Menjalankan semua test sekaligus

```
python run_all_tests.py
```

### Opsi 2: Membuat laporan HTML

```
python run_all_tests.py --html
```

### Opsi 3: Menjalankan test terpisah

```
python test_login_module.py
python test_register_module.py
```

## Fitur Tambahan

1. **Screenshots Otomatis**: Setiap test mengambil screenshot saat persiapan dan jika terjadi error
2. **Pencarian Elemen Cerdas**: Script dapat menemukan elemen meskipun struktur HTML berubah
3. **Reuse Test Data**: User test dibuat sekali dan digunakan kembali untuk test yang berbeda
4. **Error Handling Komprehensif**: Menangkap dan melaporkan error dengan jelas

## Catatan Penting

1. Modul login.php dan register.php harus tersedia di web server lokal
2. Pastikan file `logout.php` ada untuk test yang memerlukan logout
3. Pastikan koneksi database berfungsi
4. Setiap test membuat data unik dengan timestamp untuk mencegah konflik

## Pemecahan Masalah

Jika menemui masalah dengan ChromeDriver, ikuti langkah berikut:
1. Pastikan Chrome dan ChromeDriver memiliki versi yang kompatibel
2. Gunakan ChromeDriver dengan arsitektur yang sama dengan Chrome (32-bit atau 64-bit)
3. Jika error "not a valid Win32 application", unduh ChromeDriver yang sesuai dan letakkan di folder `chromedriver-win64`