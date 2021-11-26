# Import các thư viện cần thiết
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from website.models import BenhNhan, DanhSachKham, TaiKhoan, PhieuKham, ToaThuoc, Thuoc, chitiettoathuoc, HoaDon
from datetime import datetime, timedelta

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
def get_taikhoan():
    return TaiKhoan.query.all()


# --------------------BỆNH NHÂN---------------------

# --------------------PHIẾU KHÁM--------------------

# --------------------TOA THUỐC---------------------

# ----------------CHI TIẾT TOA THUỐC----------------

# ---------------------THUỐC------------------------

# ---------------------HOÁ ĐƠN----------------------


# -----------------DANH SÁCH KHÁM-------------------
def get_ds_all():
    return DanhSachKham.query.all()


def get_ds_today():
    return DanhSachKham.query.filter(
        DanhSachKham.ngaykham.between(today, tomorrow)).all()


if __name__ == '__main__':
    print(get_ds_today())
