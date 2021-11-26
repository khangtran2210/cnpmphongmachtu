# Import các thư viện cần thiết
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from website.models import BenhNhan, DanhSachKham, TaiKhoan, PhieuKham, ToaThuoc, Thuoc, chitiettoathuoc, HoaDon


# Xử lí các chức năng CRUD
#--------------------TÀI KHOẢN---------------------
def get_taikhoan():
    return TaiKhoan.query.all()


#--------------------BỆNH NHÂN---------------------

#--------------------PHIẾU KHÁM--------------------

#--------------------TOA THUỐC---------------------

#----------------CHI TIẾT TOA THUỐC----------------

#---------------------THUỐC------------------------

#---------------------HOÁ ĐƠN----------------------

#-----------------DANH SÁCH KHÁM-------------------
