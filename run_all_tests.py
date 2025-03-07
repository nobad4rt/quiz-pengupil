import unittest
import time
import sys

def run_all_tests():
    """Menjalankan semua test untuk modul login dan register"""
    print("=" * 80)
    print("MEMULAI PENGUJIAN MODUL LOGIN DAN REGISTER")
    print("=" * 80)
    
    try:
        # Import test modules
        from test_login_module import TestLoginModule
        from test_register_module import TestRegisterModule
        
        # Jalankan test register terlebih dahulu
        print("\n" + "=" * 40)
        print("MODUL REGISTER")
        print("=" * 40)
        
        register_suite = unittest.TestLoader().loadTestsFromTestCase(TestRegisterModule)
        register_result = unittest.TextTestRunner(verbosity=2).run(register_suite)
        
        print(f"\nTotal test register: {register_result.testsRun}")
        print(f"Berhasil: {register_result.testsRun - len(register_result.failures) - len(register_result.errors)}")
        print(f"Gagal: {len(register_result.failures)}")
        print(f"Error: {len(register_result.errors)}")
        
        # Jalankan test login
        print("\n" + "=" * 40)
        print("MODUL LOGIN")
        print("=" * 40)
        
        login_suite = unittest.TestLoader().loadTestsFromTestCase(TestLoginModule)
        login_result = unittest.TextTestRunner(verbosity=2).run(login_suite)
        
        print(f"\nTotal test login: {login_result.testsRun}")
        print(f"Berhasil: {login_result.testsRun - len(login_result.failures) - len(login_result.errors)}")
        print(f"Gagal: {len(login_result.failures)}")
        print(f"Error: {len(login_result.errors)}")
        
        # Laporan summary
        print("\n" + "=" * 40)
        print("RINGKASAN HASIL")
        print("=" * 40)
        total_tests = register_result.testsRun + login_result.testsRun
        total_fails = len(register_result.failures) + len(login_result.failures)
        total_errors = len(register_result.errors) + len(login_result.errors)
        total_success = total_tests - total_fails - total_errors
        
        print(f"Total test: {total_tests}")
        print(f"Berhasil: {total_success}")
        print(f"Gagal: {total_fails}")
        print(f"Error: {total_errors}")
        
        # Return non-zero exit code jika ada test yang gagal
        return 1 if (total_fails > 0 or total_errors > 0) else 0
        
    except ImportError as e:
        print(f"❌ Gagal mengimpor modul test: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return 1

def generate_html_report():
    """Generate HTML report menggunakan pytest"""
    try:
        import pytest
        timestamp = int(time.time())
        report_file = f"test_report_{timestamp}.html"
        
        print(f"Membuat laporan HTML: {report_file}")
        pytest.main([
            "test_login_module.py", 
            "test_register_module.py", 
            f"--html={report_file}", 
            "--self-contained-html"
        ])
        print(f"Laporan HTML tersimpan di: {report_file}")
        return 0
    except ImportError:
        print("❌ pytest dan/atau pytest-html tidak terinstal.")
        print("   Jalankan: pip install pytest pytest-html")
        return 1
    except Exception as e:
        print(f"❌ Error saat membuat laporan HTML: {e}")
        return 1

if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--html":
        sys.exit(generate_html_report())
    else:
        sys.exit(run_all_tests()) 