# Import các thư viện cần thiết
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from website.models import BenhNhan, DanhSachKham, TaiKhoan, PhieuKham, ToaThuoc, Thuoc, chitiettoathuoc, HoaDon
from datetime import datetime, timedelta
from sqlalchemy.sql import func

#Xử lí một số vấn đề về thời gian
# Lấy thời gian ngày hôm nay [ngày và giờ hiện tại]
today_str = datetime.today()
# Chuyển thời gian lấy được qua String
date_str = today_str.strftime("%Y-%m-%d")
# Chuyển thời gian từ String qua DateTime [ngày hiện tại, giờ 00:00:00]
today = today_str.strptime(date_str, "%Y-%m-%d")
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)


# Xử lí các chức năng CRUD
# --------------------TÀI KHOẢN---------------------
def get_taikhoan_all():
    return TaiKhoan.query.all()


def get_login(username, password):
    return TaiKhoan.query.filter(TaiKhoan.tendangnhap == username,
                                 TaiKhoan.matkhau == password).first()


def get_taikhoan_by_usernames(usernames):
    return TaiKhoan.query.filter(TaiKhoan.tendangnhap == usernames).first()


# --------------------BỆNH NHÂN---------------------


# --------------------PHIẾU KHÁM--------------------
def get_pk_by_mapk(mapk):
    return PhieuKham.query.filter(PhieuKham.mapk == mapk).first()


# --------------------TOA THUỐC---------------------
def get_toathuoc_by_matoa(matoa):
    return ToaThuoc.query.filter(ToaThuoc.matoa == matoa).first()


# ----------------CHI TIẾT TOA THUỐC----------------

# ---------------------THUỐC------------------------


# ---------------------HOÁ ĐƠN----------------------
# Lấy hoá đơn chưa thanh toán hiện lên
def get_hoadon():
    return HoaDon.query.filter(HoaDon.dathanhtoan == 0).all()


# Lấy báo cáo doanh thu
def get_baocao():
    return HoaDon.query.with_entities(
        HoaDon.ngayban,
        func.sum(HoaDon.ma_pk).label("tong_bn"),
        func.sum(HoaDon.tongthu).label("doanh_thu")).order_by(
            HoaDon.ngayban).all()


# -----------------DANH SÁCH KHÁM-------------------
def get_ds_all():
    return DanhSachKham.query.all()


def get_ds_today():
    return DanhSachKham.query.filter(
        DanhSachKham.ngaykham.between(today, tomorrow)).all()


if __name__ == '__main__':
    print(get_login(1, 2))
