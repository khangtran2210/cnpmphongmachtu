import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Blueprint, render_template, request, redirect, url_for
from website import app, db, utils
from website.models import BenhNhan, DanhSachKham, TaiKhoan, PhieuKham, ToaThuoc, Thuoc, chitiettoathuoc, HoaDon

# Tạo tên các prefix
yta = Blueprint('yta', __name__)
user = Blueprint('user', __name__)
bacsi = Blueprint('bacsi', __name__)
admin = Blueprint('admin', __name__)

# Xử lí các trang
#--------------------NGƯỜI DÙNG---------------------


@user.route('/')
def user_home():
    return render_template('home.html')


#--------------------Y TÁ---------------------


#Homepage
@yta.route('/home')
def yta_home():
    return render_template('yta.html')


#Lập hoá đơn
@yta.route('/laphoadon')
def yta_laphoadon():
    return render_template('laphoadon.html')


#CRUD Danh sách khám
#Thêm bệnh nhân khám
@yta.route('/themdskham', methods=['POST', 'GET'])
def yta_themdskham():
    ngaykham = utils.today
    hoten = request.form.get("hoten")
    gioitinh = request.form.get("gioitinh")
    namsinh = request.form.get("namsinh")
    cmnd = request.form.get("cmnd")
    diachi = request.form.get("diachi")
    sdt = request.form.get("sdt")
    trangthai = 0
    nguoikham = DanhSachKham(ngaykham=ngaykham,
                             hoten=hoten,
                             gioitinh=gioitinh,
                             namsinh=namsinh,
                             cmnd=cmnd,
                             diachi=diachi,
                             sdt=sdt,
                             trangthai=trangthai)

    try:
        db.session.add(nguoikham)
        db.session.commit()
        print("Thêm thành công")
        return redirect("danhsachkham")
    except:
        print("Thêm thất bại")
    return render_template('themdskham.html')


# Xoá bệnh nhân trong danh sách khám
@yta.route('/xoa-danhsachkham/<int:id>', methods=['GET', 'POST'])
def yta_xoadanhsachkham(id):
    id = str(id)
    nguoikham = DanhSachKham.query.filter(DanhSachKham.mads == id).first()
    print("Mã danh sách lấy được : " + "'" + str(id) + "'")
    print(nguoikham)
    try:
        db.session.delete(nguoikham)
        db.session.commit()
        print("Xoá thành công")
        #redirect thì truyền tên hàm phía dưới route theo cú pháp <blueprint-name>.<tên hàm>
        return redirect(url_for("yta.yta_danhsachkham"))
    except:
        print("Xoá thất bại")
    return redirect(url_for("yta.yta_danhsachkham"))


# Danh sách bệnh nhân khám ngày hôm nay
@yta.route('/danhsachkham')
def yta_danhsachkham():
    danhsachkham = utils.get_ds_all()
    return render_template('danhsachkham.html', danhsach=danhsachkham)


# Báo cáo
@yta.route('/baocao')
def yta_baocao():
    return render_template('baocao.html')


#Thêm người
#--------------------BÁC SĨ--------------------


#--------------------ADMIN---------------------
def create_app():
    app.register_blueprint(yta, url_prefix='/yta')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(bacsi, url_prefix='/bacsi')
    app.register_blueprint(user, url_prefix='/')
    return app