<?php
session_start(); // Bắt đầu phiên làm việc
session_unset(); // Xóa tất cả các biến phiên
session_destroy(); // Hủy phiên làm việc

// Chuyển hướng đến trang đăng nhập hoặc trang khác
header("Location: login.html");
exit();
?>
