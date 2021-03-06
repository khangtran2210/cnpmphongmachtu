# Import các thư viện cần thiết
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from website import db
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin

# ----------------------- Tạo class ----------------


class QuyDinh(db.Model):
    __tablename__ = "QuyDinh"
    maquydinh = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenquydinh = db.Column(db.String(300), nullable=False)
    quydinh = db.Column(db.Float, nullable=False)


class Quyen(db.Model):
    __tablename__ = "Quyen"
    maquyen = db.Column(db.Integer, primary_key=True)
    tenquyen = db.Column(db.String(300), nullable=False)
    taikhoans = db.relationship("TaiKhoan", backref="o_quyen", lazy=False)


class TaiKhoan(db.Model, UserMixin):
    __tablename__ = "TaiKhoan"
    madangnhap = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tendangnhap = db.Column(db.String(150), unique=True)
    matkhau = db.Column(db.String(150), nullable=False)
    ma_quyen = db.Column(db.Integer, db.ForeignKey(Quyen.maquyen), unique=True)


class DanhSachKham(db.Model):
    __tablename__ = "DanhSachKham"
    mads = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ngaykham = db.Column(db.Date, default=datetime.now().date())
    hoten = db.Column(db.String(300), nullable=False)
    gioitinh = db.Column(db.Integer, nullable=False)
    namsinh = db.Column(db.String(300), nullable=False)
    diachi = db.Column(db.String(300), nullable=False)
    cmnd = db.Column(db.String(300), nullable=False)
    sdt = db.Column(db.String(300), nullable=False)
    trangthai = db.Column(db.Boolean, nullable=False)


class BenhNhan(db.Model):
    __tablename__ = "BenhNhan"
    mabn = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hoten = db.Column(db.String(300), nullable=False)
    gioitinh = db.Column(db.Integer, nullable=False)
    namsinh = db.Column(db.String(300), nullable=False)
    diachi = db.Column(db.String(300), nullable=False)
    cmnd = db.Column(db.String(300), unique=True, nullable=False)
    sdt = db.Column(db.String(300), nullable=False)
    phieukhams = relationship("PhieuKham", backref="o_benhnhan", lazy=False)


class PhieuKham(db.Model):
    __tablename__ = "PhieuKham"
    mapk = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ngaykham = db.Column(db.Date, default=datetime.now().date())
    trieuchung = db.Column(db.String(300), nullable=False)
    loaibenh = db.Column(db.String(300), nullable=False)
    tienkham = db.Column(db.Float, default=0)
    ma_bn = db.Column(db.Integer, db.ForeignKey(BenhNhan.mabn), nullable=False)
    toathuocs = relationship("ToaThuoc", backref="o_phieukham", lazy=False)
    hoadons = relationship("HoaDon", backref="o_phieukham", lazy=False)


class ToaThuoc(db.Model):
    __tablename__ = "ToaThuoc"
    matoa = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ngayke = db.Column(db.Date, default=datetime.now().date())
    tienthuoc = db.Column(db.Float, default=0)
    ma_pk = db.Column(db.Integer, db.ForeignKey(PhieuKham.mapk), unique=True)
    hoadons = relationship("HoaDon", backref="o_toathuoc", lazy=False)
    chitiettoas = relationship("ChiTietToa", backref="o_toathuoc", lazy=False)


class HoaDon(db.Model):
    __tablename__ = "HoaDon"
    mahd = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ngayban = db.Column(db.Date, default=datetime.now().date())
    tongthu = db.Column(db.Float, default=0)
    dathanhtoan = db.Column(db.Boolean, default=False)
    ma_pk = db.Column(db.Integer, db.ForeignKey(PhieuKham.mapk), unique=True)
    ma_toa = db.Column(db.Integer, db.ForeignKey(ToaThuoc.matoa), unique=True)


class CachDung(db.Model):
    __tablename__ = "CachDung"
    macachdung = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tencachdung = db.Column(db.String(300), nullable=False)
    thuocs = relationship("Thuoc", backref="o_cachdung", lazy=True)


class DonVi(db.Model):
    __tablename__ = "DonVi"
    madonvi = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tendonvi = db.Column(db.String(300), nullable=False)
    thuocs = relationship("Thuoc", backref="o_donvi", lazy=True)


class Thuoc(db.Model):
    __tablename__ = "Thuoc"
    mathuoc = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenthuoc = db.Column(db.String(300), unique=True, nullable=False)
    soluong = db.Column(db.Integer, default=0)
    dongia = db.Column(db.Float, default=0)
    madonvi = db.Column(db.Integer, db.ForeignKey(DonVi.madonvi), unique=True)
    macachdung = db.Column(db.Integer,
                           db.ForeignKey(CachDung.macachdung),
                           unique=True)
    trangthai = db.Column(db.Integer, default=1)


class ChiTietToa(db.Model):
    __tablename__ = "ChiTietToa"
    matoa = db.Column(db.Integer,
                      db.ForeignKey(ToaThuoc.matoa),
                      primary_key=True)
    mathuoc = db.Column(db.Integer,
                        db.ForeignKey(Thuoc.mathuoc),
                        primary_key=True)
    soluong = db.Column(db.Integer, default=0)
    tienthuoc = db.Column(db.Float, default=0)
    thuocs = db.relationship("Thuoc", backref="o_chitiettoa", lazy=False)


if __name__ == "__main__":
    # Xoá database
    #db.drop_all()
    # Tạo database
    db.create_all()
