DROP TABLE IF EXISTS NhanVien;
DROP TABLE IF EXISTS NV_QL;
DROP TABLE IF EXISTS Timesheet;
DROP TABLE IF EXISTS NV_RequestLeave;
DROP TABLE IF EXISTS NV_RequestWFH;
DROP TABLE IF EXISTS NV_RequestUpdate;

-- Create NhanVien table
CREATE TABLE IF NOT EXISTS NhanVien (
    ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    MaNV VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(50) DEFAULT '123',
    HoTen VARCHAR(200) DEFAULT '',
    GioiTinh VARCHAR(10) DEFAULT '',
    CCCD VARCHAR(20) UNIQUE,
    NgaySinh DATE DEFAULT '2000-01-01',
    MaSoThue VARCHAR(20) UNIQUE,
    DiaChi VARCHAR(100) DEFAULT '',
    SDT VARCHAR(20) UNIQUE,
    Email VARCHAR(50) UNIQUE,
    STK VARCHAR(50) UNIQUE
);

-- Create NV_QL table without foreign keys
CREATE TABLE IF NOT EXISTS NV_QL (
    ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    MaNV VARCHAR(50) UNIQUE NOT NULL,
    MaQL VARCHAR(50) NOT NULL
);

-- Create Timesheet table without foreign key
CREATE TABLE IF NOT EXISTS Timesheet (
    ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Ngay DATE DEFAULT '2000-01-01',
    MaNV VARCHAR(50),
    Checkin TIME,
    Checkout TIME,
    isLeave BOOLEAN DEFAULT FALSE,
    isWFH BOOLEAN DEFAULT FALSE
);

-- Create NV_RequestLeave table without foreign key
CREATE TABLE IF NOT EXISTS NV_RequestLeave (
    ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    MaYC VARCHAR(10) UNIQUE NOT NULL,
    MaNV VARCHAR(10) NOT NULL,
    NgayGui DATETIME DEFAULT '2000-01-01 00:00:00',
    NgayDuyet DATETIME DEFAULT '2000-01-01 00:00:00',
    NgayRequest DATETIME DEFAULT '2000-01-01 00:00:00',
    TrangThai VARCHAR(50),
    IDNguoiDuyet VARCHAR(10)
);

-- Create NV_RequestWFH table without foreign key
CREATE TABLE IF NOT EXISTS NV_RequestWFH (
    ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    MaYC VARCHAR(10) UNIQUE NOT NULL,
    MaNV VARCHAR(10) NOT NULL,
    NgayGui DATETIME DEFAULT '2000-01-01 00:00:00',
    NgayDuyet DATETIME DEFAULT '2000-01-01 00:00:00',
    NgayRequest DATETIME DEFAULT '2000-01-01 00:00:00',
    TrangThai VARCHAR(50),
    IDNguoiDuyet VARCHAR(10)
);

-- Create NV_RequestUpdate table without foreign key
CREATE TABLE IF NOT EXISTS NV_RequestUpdate (
    ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    MaYC VARCHAR(10) UNIQUE NOT NULL,
    MaNV VARCHAR(10) NOT NULL,
    Ngay DATE DEFAULT '2000-01-01',
    Checkin TIME,
    updateCheckin TIME,
    Checkout TIME,
    updateCheckout TIME,
    NgayGui DATETIME DEFAULT '2000-01-01 00:00:00',
    ChiTiet TEXT,
    TrangThai VARCHAR(50),
    NgayDuyet DATETIME DEFAULT '2000-01-01 00:00:00',
    IDNguoiDuyet VARCHAR(10)
);

-- Ensure AUTO_INCREMENT starts at 1 for all tables
ALTER TABLE NhanVien AUTO_INCREMENT = 1;
ALTER TABLE NV_QL AUTO_INCREMENT = 1;
ALTER TABLE Timesheet AUTO_INCREMENT = 1;
ALTER TABLE NV_RequestLeave AUTO_INCREMENT = 1;
ALTER TABLE NV_RequestWFH AUTO_INCREMENT = 1;
ALTER TABLE NV_RequestUpdate AUTO_INCREMENT = 1;
