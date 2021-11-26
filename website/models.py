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


class TaiKhoan(db.Model, UserMixin):
    __tablename__ = "TaiKhoan"
    madangnhap = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tendangnhap = db.Column(db.String(150), unique=True)
    matkhau = db.Column(db.String(150), nullable=False)
    maquyen = db.Column(db.Integer, default=3)


class DanhSachKham(db.Model):
    __tablename__ = "DanhSachKham"
    mads = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ngaykham = db.Column(db.DateTime, default=datetime.now())
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
    ngaykham = db.Column(db.DateTime, default=datetime.now())
    trieuchung = db.Column(db.String(300), nullable=False)
    loaibenh = db.Column(db.String(300), nullable=False)
    tienkham = db.Column(db.Float, default=0)
    ma_bn = db.Column(db.Integer, db.ForeignKey(BenhNhan.mabn), nullable=False)
    toathuocs = relationship("ToaThuoc", backref="o_phieukham", lazy=False)
    hoadons = relationship("HoaDon", backref="o_phieukham", lazy=False)


class ToaThuoc(db.Model):
    __tablename__ = "ToaThuoc"
    matoa = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ngayke = db.Column(db.DateTime, default=datetime.now())
    tienthuoc = db.Column(db.Float, default=0)
    ma_pk = db.Column(db.Integer, db.ForeignKey(PhieuKham.mapk), unique=True)
    hoadons = relationship("HoaDon", backref="o_toathuoc", lazy=False)
    thuocs = relationship(
        "Thuoc",
        secondary="chitiettoathuoc",
        backref=db.backref("o_toathuoc", lazy=False),
    )


class HoaDon(db.Model):
    __tablename__ = "HoaDon"
    mahd = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ngayban = db.Column(db.DateTime, default=datetime.now())
    tongthu = db.Column(db.Float, default=0)
    dathanhtoan = db.Column(db.Boolean, default=False)
    ma_pk = db.Column(db.Integer, db.ForeignKey(PhieuKham.mapk), unique=True)
    ma_toa = db.Column(db.Integer, db.ForeignKey(ToaThuoc.matoa), unique=True)


class Thuoc(db.Model):
    __tablename__ = "Thuoc"
    mathuoc = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenthuoc = db.Column(db.String(300), nullable=False)
    donvi = db.Column(db.String(300), nullable=False)
    soluong = db.Column(db.Integer, default=0)
    dongia = db.Column(db.Float, default=0)
    cachdung = db.Column(db.String(300), nullable=False)


chitiettoathuoc = db.Table(
    "chitiettoathuoc",
    db.Column("matoa", db.Integer, db.ForeignKey(ToaThuoc.matoa)),
    db.Column("mathuoc", db.Integer, db.ForeignKey(Thuoc.mathuoc)),
    db.Column("soluong", db.Integer, default=0),
)

# if __name__ == "__main__":
#     db.create_all()
