<?php
// Memulai session (diperlukan untuk menghapus session)
session_start();

// Memeriksa apakah session ada sebelum menghapus
if(isset($_SESSION)) {
    // Hapus semua variabel session
    $_SESSION = array();

    // Hapus cookie session jika ada
    if (isset($_COOKIE[session_name()])) {
        setcookie(session_name(), '', time()-42000, '/');
    }

    // Hancurkan session
    session_destroy();
}

// Redirect ke halaman login
header("Location: login.php");
exit; 