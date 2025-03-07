#!/bin/bash

# Script untuk konfigurasi tambahan di lingkungan CI/CD
# Dipanggil dari GitHub Actions workflow

echo "=== Setup Lingkungan CI/CD ==="

# Pastikan direktori untuk screenshot ada
mkdir -p ss_login
mkdir -p ss_register

# Periksa dependensi Python
echo "=== Memeriksa dependensi Python ==="
pip freeze

# Periksa Chrome dan ChromeDriver
echo "=== Memeriksa versi Chrome ==="
google-chrome --version

echo "=== Memeriksa versi ChromeDriver ==="
if [ -f "chromedriver-linux64/chromedriver" ]; then
    chromedriver-linux64/chromedriver --version
else
    echo "ChromeDriver tidak ditemukan di chromedriver-linux64/"
fi

# Update BASE_URL di file pengujian
echo "=== Update BASE_URL ==="
find . -name "test_*.py" -type f -exec grep -l "BASE_URL" {} \; | xargs -I{} echo "File: {}"

# Memastikan file PHP tersedia
echo "=== Memeriksa file PHP ==="
ls -la *.php

# Selesai
echo "=== Setup CI/CD selesai ===" 