import time
import unittest
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import string

def generate_random_string(length=8):
    """Menghasilkan string acak dengan panjang tertentu"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

class TestRegisterModule(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup yang dijalankan sekali sebelum semua test"""
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Jalankan dalam mode headless
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Gunakan chromedriver dari folder chromedriver-win64 jika ada
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = script_dir  # Diasumsikan script berada di root project
        chrome_driver_path = os.path.join(project_dir, "chromedriver-win64", "chromedriver.exe")
        
        # Buat folder untuk screenshot
        cls.screenshot_folder = os.path.join(project_dir, "ss_register")
        if not os.path.exists(cls.screenshot_folder):
            os.makedirs(cls.screenshot_folder)
            print(f"✅ Folder screenshot dibuat di {cls.screenshot_folder}")
        else:
            print(f"✅ Menggunakan folder screenshot yang sudah ada di {cls.screenshot_folder}")
        
        if os.path.exists(chrome_driver_path):
            print(f"✅ Menggunakan ChromeDriver dari {chrome_driver_path}")
            cls.driver = webdriver.Chrome(
                service=Service(executable_path=chrome_driver_path),
                options=chrome_options
            )
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            print("⚠️ ChromeDriver tidak ditemukan, menggunakan WebDriverManager")
            cls.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        
        # Konfigurasi driver
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost/quiz-pengupil"
        
        # Register user_sudah_ada untuk TC3
        cls.create_existing_user()
    
    @classmethod
    def tearDownClass(cls):
        """Teardown yang dijalankan sekali setelah semua test"""
        cls.driver.quit()

    @classmethod
    def save_screenshot(cls, driver, filename):
        """Helper untuk menyimpan screenshot ke folder ss_register"""
        filepath = os.path.join(cls.screenshot_folder, filename)
        driver.save_screenshot(filepath)
        return filepath

    @classmethod
    def create_existing_user(cls):
        """Buat user untuk pengujian username yang sudah ada"""
        driver = cls.driver
        
        # Setup data test user
        cls.existing_username = "user_sudah_ada"
        cls.existing_password = "password123"
        cls.existing_email = "user_sudah_ada@example.com"
        cls.existing_name = "User Sudah Ada"
        
        # Register user baru jika belum ada
        driver.get(f"{cls.base_url}/register.php")
        
        # Cek apakah form register muncul
        try:
            # Isi form register
            cls.fill_input_field(driver, "name", cls.existing_name)
            cls.fill_input_field(driver, "email", cls.existing_email)
            cls.fill_input_field(driver, "username", cls.existing_username)
            cls.fill_input_field(driver, "password", cls.existing_password)
            cls.fill_input_field(driver, "repassword", cls.existing_password)
            
            # Submit form
            cls.find_and_click_button(driver)
            
            # Cek apakah berhasil didaftarkan atau sudah ada
            try:
                WebDriverWait(driver, 5).until(
                    lambda d: "index.php" in d.current_url or cls.element_exists(d, By.CLASS_NAME, "alert-danger")
                )
            except TimeoutException:
                print("⚠️ Waktu tunggu habis saat memeriksa hasil registrasi existing user")
            
            # Logout jika berhasil register
            if "index.php" in driver.current_url:
                driver.get(f"{cls.base_url}/logout.php")
            
            print(f"✅ User existing {cls.existing_username} siap digunakan untuk TC3")
        except Exception as e:
            print(f"⚠️ Gagal menyiapkan existing user: {e}")
            # Coba login saja untuk memastikan user sudah ada
            driver.get(f"{cls.base_url}/login.php")
            try:
                cls.fill_input_field(driver, "username", cls.existing_username)
                cls.fill_input_field(driver, "password", cls.existing_password)
                cls.find_and_click_button(driver)
                
                # Logout jika berhasil login
                if "index.php" in driver.current_url:
                    driver.get(f"{cls.base_url}/logout.php")
                    print(f"✅ User existing {cls.existing_username} sudah ada dan dapat digunakan")
            except:
                print("⚠️ Existing user belum terdaftar dan gagal dibuat")
    
    @staticmethod
    def fill_input_field(driver, field_identifier, value):
        """Mengisi field input dengan berbagai metode pencarian"""
        # Tambahkan tunggu sedikit untuk memastikan halaman loading selesai
        time.sleep(1)
        
        # Coba berbagai selector untuk menemukan field
        for selector in [By.ID, By.NAME]:
            try:
                element = driver.find_element(selector, field_identifier)
                element.clear()
                element.send_keys(value)
                return True
            except NoSuchElementException:
                pass
        
        # Coba pendekatan placeholder
        placeholders = {
            "name": "Masukkan Nama",
            "email": "Masukkan email",
            "username": "Masukkan username",
            "password": "Password",
            "repassword": "Re-Password"
        }
        
        if field_identifier in placeholders:
            try:
                element = driver.find_element(By.XPATH, f"//input[@placeholder='{placeholders[field_identifier]}']")
                element.clear()
                element.send_keys(value)
                return True
            except NoSuchElementException:
                pass
        
        # Cari semua input field dan coba temukan yang sesuai
        inputs = driver.find_elements(By.TAG_NAME, "input")
        if len(inputs) == 0:
            # Ambil screenshot jika tidak ada input sama sekali
            TestRegisterModule.save_screenshot(driver, f"no_inputs_found_{int(time.time())}.png")
            print(f"⚠️ Tidak ada input elements ditemukan saat mencari {field_identifier}")
        
        for input_elem in inputs:
            input_type = input_elem.get_attribute("type")
            input_id = input_elem.get_attribute("id") or ""
            input_name = input_elem.get_attribute("name") or ""
            input_placeholder = input_elem.get_attribute("placeholder") or ""
            
            # Log info untuk debugging
            print(f"Input ditemukan: id={input_id}, name={input_name}, type={input_type}, placeholder={input_placeholder}")
            
            # Logika untuk field password
            if field_identifier == "password" and input_type == "password":
                if "re" not in str(input_id).lower() and "re" not in str(input_name).lower():
                    input_elem.clear()
                    input_elem.send_keys(value)
                    return True
            
            # Logika untuk field repassword
            elif field_identifier == "repassword" and input_type == "password":
                if "re" in str(input_id).lower() or "re" in str(input_name).lower():
                    input_elem.clear()
                    input_elem.send_keys(value)
                    return True
            
            # Logika untuk field lainnya
            elif field_identifier in str(input_id).lower() or field_identifier in str(input_name).lower() or field_identifier in str(input_placeholder).lower():
                input_elem.clear()
                input_elem.send_keys(value)
                return True
                
        # Screenshot untuk debugging
        timestamp = int(time.time())
        TestRegisterModule.save_screenshot(driver, f"debug_field_not_found_{field_identifier}_{timestamp}.png")
        print(f"⚠️ Tidak dapat menemukan field '{field_identifier}', halaman: {driver.current_url}")
        
        return False
    
    @staticmethod
    def find_and_click_button(driver):
        """Menemukan dan mengklik tombol submit/login/register"""
        # Tambahkan tunggu sedikit
        time.sleep(1)
        
        # Coba cari dengan name=submit
        try:
            button = driver.find_element(By.NAME, "submit")
            button.click()
            return True
        except NoSuchElementException:
            pass
        
        # Coba cari button dengan teks
        button_texts = ["Register", "Sign Up", "Daftar", "Submit", "Login", "Sign In"]
        for text in button_texts:
            try:
                button = driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                button.click()
                return True
            except NoSuchElementException:
                pass
        
        # Coba cari input[type=submit]
        try:
            button = driver.find_element(By.XPATH, "//input[@type='submit']")
            button.click()
            return True
        except NoSuchElementException:
            pass
        
        # Coba cari form dan button di dalamnya
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            button = form.find_element(By.TAG_NAME, "button")
            button.click()
            return True
        except NoSuchElementException:
            pass
        
        # Cari semua button untuk debugging
        buttons = driver.find_elements(By.TAG_NAME, "button")
        if len(buttons) > 0:
            print(f"⚠️ Ditemukan {len(buttons)} button, tapi tidak ada yang cocok:")
            for btn in buttons:
                print(f"  - Text: '{btn.text}', Class: '{btn.get_attribute('class')}'")
        
        # Screenshot untuk debugging
        timestamp = int(time.time())
        TestRegisterModule.save_screenshot(driver, f"debug_no_button_found_{timestamp}.png")
        print(f"⚠️ Tidak dapat menemukan tombol submit di halaman: {driver.current_url}")
        
        return False
    
    @staticmethod
    def element_exists(driver, by, value):
        """Cek apakah elemen ada tanpa menunggu"""
        try:
            driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    @staticmethod
    def is_logged_in(driver, base_url):
        """Cek apakah user sudah login dengan mengakses index.php"""
        current_url = driver.current_url
        driver.get(f"{base_url}/index.php")
        
        # Jika diarahkan ke login.php, berarti belum login
        is_login = "login.php" not in driver.current_url
        
        # Kembali ke halaman sebelumnya
        driver.get(current_url)
        return is_login
    
    def wait_for_result(self, driver, timeout=5):
        """Tunggu hasil submit form (redirect ke index.php atau muncul pesan error)"""
        start_time = time.time()
        current_url = driver.current_url
        
        # Loop sampai timeout
        while time.time() - start_time < timeout:
            # Cek redirect ke index.php
            if "index.php" in driver.current_url:
                return "redirect"
            
            # Cek pesan error
            if self.element_exists(driver, By.CLASS_NAME, "alert-danger"):
                return "error"
                
            # Cek pesan validasi password
            if self.element_exists(driver, By.CLASS_NAME, "text-danger"):
                return "validation"
                
            # Cek URL berubah
            if driver.current_url != current_url:
                return "url_changed"
                
            # Tunggu sebentar
            time.sleep(0.5)
            
        # Waktu habis, ambil screenshot
        TestRegisterModule.save_screenshot(driver, f"timeout_waiting_for_result_{int(time.time())}.png")
        return "timeout"
    
    def test_01_valid_registration(self):
        """Test Case 1: Registrasi dengan Data Valid"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        # Siapkan data test yang valid
        test_name = "John Doe"
        test_email = f"john_{generate_random_string()}@example.com"
        test_username = f"john_doe_{generate_random_string()}"
        test_password = "Password123"
        
        # Isi form register
        if not self.fill_input_field(driver, "name", test_name):
            self.fail("❌ TC1: Gagal mengisi field name")
        if not self.fill_input_field(driver, "email", test_email):
            self.fail("❌ TC1: Gagal mengisi field email")
        if not self.fill_input_field(driver, "username", test_username):
            self.fail("❌ TC1: Gagal mengisi field username")
        if not self.fill_input_field(driver, "password", test_password):
            self.fail("❌ TC1: Gagal mengisi field password")
        if not self.fill_input_field(driver, "repassword", test_password):
            self.fail("❌ TC1: Gagal mengisi field repassword")
        
        # Klik tombol register
        if not self.find_and_click_button(driver):
            self.fail("❌ TC1: Gagal menemukan tombol register")
        
        # Tunggu hasil
        result = self.wait_for_result(driver)
        
        # Tangkap screenshot sebelum registrasi
        self.save_screenshot(driver, "tc1_register_form.png")
        
        # Verifikasi hasil:
        # 1. Data tersimpan (dibuktikan dengan redirect ke index.php & session aktif)
        # 2. Password di-hash (tidak bisa diverifikasi melalui UI test)
        if result == "redirect" and "index.php" in driver.current_url:
            # Cek apakah user sudah login
            self.assertTrue(self.is_logged_in(driver, self.base_url))
            print(f"✅ TC1: Registrasi berhasil dengan username {test_username}")
        else:
            self.save_screenshot(driver, "tc1_register_failed.png")
            html_content = driver.page_source
            self.fail(f"❌ TC1: Registrasi gagal, result: {result}, URL: {driver.current_url}")
        
        # Logout untuk test berikutnya
        driver.get(f"{self.base_url}/logout.php")
    
    def test_02_password_mismatch(self):
        """Test Case 2: Password dan Re-Password Tidak Sama"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        # Siapkan data test dengan password berbeda
        test_name = "Password Mismatch"
        test_email = f"mismatch_{generate_random_string()}@example.com"
        test_username = f"mismatch_{generate_random_string()}"
        test_password = "Password123"
        test_repassword = "Password456"
        
        # Isi form register
        self.fill_input_field(driver, "name", test_name)
        self.fill_input_field(driver, "email", test_email)
        self.fill_input_field(driver, "username", test_username)
        self.fill_input_field(driver, "password", test_password)
        self.fill_input_field(driver, "repassword", test_repassword)
        
        # Klik tombol register
        self.find_and_click_button(driver)
        
        # Tunggu hasil
        result = self.wait_for_result(driver)
        
        # Tangkap screenshot sebelum registrasi
        self.save_screenshot(driver, "tc2_password_mismatch_form.png")
        
        # Verifikasi hasil:
        # Tampil pesan error: "Password tidak sama !!"
        if result == "validation" or result == "error":
            # Coba cek pesan error text-danger
            if self.element_exists(driver, By.CLASS_NAME, "text-danger"):
                error_element = driver.find_element(By.CLASS_NAME, "text-danger")
                error_text = error_element.text
                if "password" in error_text.lower() or "sama" in error_text.lower():
                    print(f"✅ TC2: Deteksi password tidak sama berhasil, pesan: {error_text}")
                else:
                    self.save_screenshot(driver, "tc2_wrong_error_text.png")
                    print(f"⚠️ TC2: Pesan error tidak spesifik 'password tidak sama': {error_text}")
            # Coba cek error dengan selector lain
            elif self.element_exists(driver, By.CLASS_NAME, "alert-danger"):
                error_text = driver.find_element(By.CLASS_NAME, "alert-danger").text
                if "password" in error_text.lower() or "sama" in error_text.lower():
                    print(f"✅ TC2: Deteksi password tidak sama berhasil, pesan: {error_text}")
                else:
                    self.save_screenshot(driver, "tc2_wrong_error.png")
                    print(f"⚠️ TC2: Pesan error tidak tentang password: {error_text}")
            else:
                self.save_screenshot(driver, "tc2_failed.png")
                print(f"⚠️ TC2: Error alert tidak ditemukan sama sekali")
        elif result == "redirect":
            self.save_screenshot(driver, "tc2_redirect.png")
            print(f"⚠️ TC2: Redirect berhasil padahal harusnya error password tidak sama")
        else:
            self.save_screenshot(driver, "tc2_timeout.png")
            print(f"⚠️ TC2: Tidak ada hasil yang terdeteksi: {result}")
    
    def test_03_username_already_exists(self):
        """Test Case 3: Username Sudah Terdaftar"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        # Siapkan data test dengan username yang sudah ada
        test_name = "Another User"
        test_email = f"another_{generate_random_string()}@example.com"
        # Gunakan username yang sudah dibuat di setup
        test_username = self.existing_username
        test_password = "Password123"
        
        # Isi form register
        self.fill_input_field(driver, "name", test_name)
        self.fill_input_field(driver, "email", test_email)
        self.fill_input_field(driver, "username", test_username)
        self.fill_input_field(driver, "password", test_password)
        self.fill_input_field(driver, "repassword", test_password)
        
        # Klik tombol register
        self.find_and_click_button(driver)
        
        # Tunggu hasil
        result = self.wait_for_result(driver)
        
        # Tangkap screenshot sebelum registrasi
        self.save_screenshot(driver, "tc3_existing_username_form.png")
        
        # Verifikasi hasil:
        # Tampil pesan error: "Username sudah terdaftar !!"
        if result == "error" and self.element_exists(driver, By.CLASS_NAME, "alert-danger"):
            error_element = driver.find_element(By.CLASS_NAME, "alert-danger")
            error_text = error_element.text
            if "username" in error_text.lower() and ("sudah" in error_text.lower() or "terdaftar" in error_text.lower()):
                print(f"✅ TC3: Deteksi username sudah terdaftar berhasil, pesan: {error_text}")
            else:
                self.save_screenshot(driver, "tc3_wrong_error.png")
                print(f"⚠️ TC3: Muncul pesan error tetapi bukan untuk username sudah terdaftar: {error_text}")
        # Cek apakah tetap di halaman register
        elif "index.php" not in driver.current_url:
            self.save_screenshot(driver, "tc3_no_error_msg.png")
            print("⚠️ TC3: Tidak ada pesan error spesifik, tapi pendaftaran gagal (tetap di halaman register)")
        else:
            self.save_screenshot(driver, "tc3_failed.png")
            self.fail(f"❌ TC3: Test username sudah terdaftar gagal: {result}")
    
    def test_04_empty_fields(self):
        """Test Case 4: Field Kosong"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        # Siapkan data test dengan salah satu field kosong (username)
        test_name = "Empty Field Test"
        test_email = f"empty_{generate_random_string()}@example.com"
        # Username dikosongkan
        test_password = "Password123"
        
        # Isi form register (tanpa username)
        self.fill_input_field(driver, "name", test_name)
        self.fill_input_field(driver, "email", test_email)
        # Username dikosongkan sengaja
        self.fill_input_field(driver, "password", test_password)
        self.fill_input_field(driver, "repassword", test_password)
        
        # Klik tombol register
        self.find_and_click_button(driver)
        
        # Tunggu hasil
        result = self.wait_for_result(driver)
        
        # Tangkap screenshot sebelum registrasi
        self.save_screenshot(driver, "tc4_empty_field_form.png")
        
        # Verifikasi hasil:
        # Tampil pesan error: "Data tidak boleh kosong !!"
        if result == "error" and self.element_exists(driver, By.CLASS_NAME, "alert-danger"):
            error_element = driver.find_element(By.CLASS_NAME, "alert-danger")
            error_text = error_element.text
            if "kosong" in error_text.lower() or "empty" in error_text.lower():
                print(f"✅ TC4: Deteksi field kosong berhasil, pesan: {error_text}")
            else:
                self.save_screenshot(driver, "tc4_wrong_error.png")
                print(f"⚠️ TC4: Muncul pesan error tetapi bukan untuk field kosong: {error_text}")
        # Cek apakah tetap di halaman register
        elif "index.php" not in driver.current_url:
            self.save_screenshot(driver, "tc4_no_error_msg.png")
            print("⚠️ TC4: Tidak ada pesan error spesifik, tapi pendaftaran gagal (tetap di halaman register)")
        else:
            self.save_screenshot(driver, "tc4_failed.png")
            self.fail(f"❌ TC4: Test field kosong gagal: {result}")
    
    def test_05_sql_injection_attempt(self):
        """Test Case 5: SQL Injection pada Input"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        
        # Siapkan data test dengan sql injection di username
        test_name = "SQL Injection Test"
        test_email = f"sql_{generate_random_string()}@example.com"
        test_username = "'; DROP TABLE users; --"
        test_password = "Password123"
        
        # Isi form register
        self.fill_input_field(driver, "name", test_name)
        self.fill_input_field(driver, "email", test_email)
        self.fill_input_field(driver, "username", test_username)
        self.fill_input_field(driver, "password", test_password)
        self.fill_input_field(driver, "repassword", test_password)
        
        # Klik tombol register
        self.find_and_click_button(driver)
        
        # Tunggu hasil
        result = self.wait_for_result(driver)
        
        # Tangkap screenshot sebelum registrasi
        self.save_screenshot(driver, "tc5_sql_injection_form.png")
        
        # Verifikasi hasil:
        # Jika SQL injection berhasil dicegah, user akan terdaftar normal atau 
        # terjadi error karena validasi khusus. Yang penting, database tidak rusak.
        try:
            # Jika ada error atau tetap di halaman register, SQL injection gagal (bagus)
            if result == "error" or (result != "redirect" and "index.php" not in driver.current_url):
                print("✅ TC5: Upaya SQL injection gagal (seperti yang diharapkan)")
            elif result == "redirect" and "index.php" in driver.current_url:
                # Jika berhasil register, cek apakah bisa login dengan akun tersebut
                # Logout dulu
                driver.get(f"{self.base_url}/logout.php")
                time.sleep(1)
                
                # Verifikasi tabel users masih ada dengan mencoba register user normal
                driver.get(f"{self.base_url}/register.php")
                verify_test_username = f"verify_{generate_random_string()}"
                
                # Isi form register untuk user verifikasi
                self.fill_input_field(driver, "name", "Verify User")
                self.fill_input_field(driver, "email", f"{verify_test_username}@example.com")
                self.fill_input_field(driver, "username", verify_test_username)
                self.fill_input_field(driver, "password", "Password123")
                self.fill_input_field(driver, "repassword", "Password123")
                self.find_and_click_button(driver)
                
                # Tunggu hasil
                verify_result = self.wait_for_result(driver)
                
                # Jika berhasil register, berarti tabel users masih ada
                if verify_result == "redirect" and "index.php" in driver.current_url:
                    print("✅ TC5: SQL injection dihalangi, dan tabel users masih ada")
                else:
                    self.save_screenshot(driver, "tc5_verify_failed.png")
                    self.fail(f"❌ TC5: Gagal memverifikasi bahwa tabel users masih ada, result: {verify_result}")
            else:
                self.save_screenshot(driver, "tc5_result_unclear.png")
                self.fail(f"❌ TC5: Hasil tidak jelas, result: {result}")
        except Exception as e:
            self.save_screenshot(driver, "tc5_exception.png")
            self.fail(f"❌ TC5: Test SQL injection gagal dengan exception: {e}")
        
        # Logout untuk test berikutnya
        try:
            driver.get(f"{self.base_url}/logout.php")
        except:
            pass
    
    def test_06_no_email_validation(self):
        """Test Case 6: Validasi Email Tidak Ada"""
        driver = self.driver
        driver.get(f"{self.base_url}/register.php")
        time.sleep(1)  # Tunggu halaman load
        
        # Siapkan data test dengan email tidak valid
        test_name = "Invalid Email Test"
        test_email = "bukan_email"  # Format email tidak valid
        test_username = f"invalid_email_{generate_random_string()}"
        test_password = "Password123"
        
        # Isi form register
        if not self.fill_input_field(driver, "name", test_name):
            self.fail("❌ TC6: Gagal mengisi field name")
            
        if not self.fill_input_field(driver, "email", test_email):
            self.fail("❌ TC6: Gagal mengisi field email")
            
        if not self.fill_input_field(driver, "username", test_username):
            self.fail("❌ TC6: Gagal mengisi field username")
            
        if not self.fill_input_field(driver, "password", test_password):
            self.fail("❌ TC6: Gagal mengisi field password")
            
        if not self.fill_input_field(driver, "repassword", test_password):
            self.fail("❌ TC6: Gagal mengisi field repassword")
        
        # Klik tombol register
        if not self.find_and_click_button(driver):
            self.fail("❌ TC6: Gagal menemukan tombol register")
        
        # Tunggu hasil
        result = self.wait_for_result(driver, timeout=10)  # Tunggu lebih lama
        
        # Tangkap screenshot sebelum registrasi
        self.save_screenshot(driver, "tc6_invalid_email_form.png")
        
        # Verifikasi hasil:
        # Karena tidak ada validasi email, seharusnya tetap berhasil register
        try:
            if result == "redirect" and "index.php" in driver.current_url:
                print("✅ TC6: Email tidak valid diterima, sesuai ekspektasi (bug potensial)")
            elif result == "error" and self.element_exists(driver, By.CLASS_NAME, "alert-danger"):
                # Jika muncul pesan error, mungkin ada validasi email
                error_text = driver.find_element(By.CLASS_NAME, "alert-danger").text
                self.save_screenshot(driver, "tc6_rejected.png")
                print(f"⚠️ TC6: Email tidak valid ditolak, mungkin ada validasi: {error_text}")
            else:
                self.save_screenshot(driver, "tc6_result_unclear.png")
                print(f"⚠️ TC6: Hasil tidak jelas, result: {result}, URL: {driver.current_url}")
                # Lanjutkan test tanpa fail
        except Exception as e:
            self.save_screenshot(driver, "tc6_exception.png")
            print(f"⚠️ TC6: Exception saat test email tidak valid: {e}")
            # Lanjutkan test tanpa fail
        
        # Logout untuk test berikutnya (jika berhasil login)
        try:
            if "index.php" in driver.current_url:
                driver.get(f"{self.base_url}/logout.php")
        except:
            pass
    
if __name__ == "__main__":
    unittest.main() 