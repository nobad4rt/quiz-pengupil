<?php
/**
 * Script untuk setup database pengujian
 * Digunakan untuk mempersiapkan tabel dan data awal
 * untuk keperluan pengujian otomatis
 */

// Konfigurasi database
$db_host = 'localhost';
$db_user = 'root';
$db_pass = '';
$db_name = 'quiz_pengupil';

// Cek apakah ini dijalankan pada CI/CD environment
if (getenv('CI') === 'true') {
    $db_host = '127.0.0.1';
    $db_pass = 'root';
}

// Koneksi ke database
try {
    echo "Mencoba menghubungkan ke database...\n";
    $conn = new mysqli($db_host, $db_user, $db_pass);
    
    if ($conn->connect_error) {
        die("Koneksi gagal: " . $conn->connect_error . "\n");
    }
    
    echo "Koneksi berhasil!\n";
    
    // Cek apakah database sudah ada
    $result = $conn->query("SHOW DATABASES LIKE '$db_name'");
    if ($result->num_rows == 0) {
        echo "Membuat database $db_name...\n";
        if ($conn->query("CREATE DATABASE $db_name")) {
            echo "Database berhasil dibuat.\n";
        } else {
            die("Gagal membuat database: " . $conn->error . "\n");
        }
    } else {
        echo "Database $db_name sudah ada.\n";
    }
    
    // Pilih database
    $conn->select_db($db_name);
    
    // Buat tabel users jika belum ada
    $sql = "CREATE TABLE IF NOT EXISTS users (
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )";
    
    if ($conn->query($sql)) {
        echo "Tabel users berhasil dibuat atau sudah ada.\n";
    } else {
        die("Error membuat tabel users: " . $conn->error . "\n");
    }
    
    // Cek apakah ada user test
    $result = $conn->query("SELECT * FROM users WHERE username = 'test_user'");
    if ($result->num_rows == 0) {
        // Buat user untuk keperluan test
        $name = "Test User";
        $email = "test@example.com";
        $username = "test_user";
        $password = password_hash("test123", PASSWORD_DEFAULT);
        
        $sql = "INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssss", $name, $email, $username, $password);
        
        if ($stmt->execute()) {
            echo "User test berhasil dibuat.\n";
        } else {
            echo "Error membuat user test: " . $stmt->error . "\n";
        }
        
        $stmt->close();
    } else {
        echo "User test sudah ada.\n";
    }
    
    echo "Setup database selesai!\n";
    $conn->close();
    
} catch (Exception $e) {
    die("Error: " . $e->getMessage() . "\n");
}
?> 