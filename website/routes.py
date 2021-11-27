import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from website import app, db, utils
from website.models import BenhNhan, DanhSachKham, TaiKhoan, PhieuKham, ToaThuoc, Thuoc, chitiettoathuoc, HoaDon

# Tạo tên các prefix
yta = Blueprint('yta', __name__)
user = Blueprint('user', __name__)
bacsi = Blueprint('bacsi', __name__)
admin = Blueprint('admin', __name__)


# Xử lí các trang
#--------------------NGƯỜI DÙNG---------------------
# Chặn người dùng đăng nhập trái phép
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('user.user_login'))

    return wrap


@user.route('/')
@login_required
def user_home():
    return render_template('home.html')


@user.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        session.pop('user', None)
        tentaikhoan = request.form['username']
        matkhau = request.form['password']
        dangnhap = utils.get_login(tentaikhoan, matkhau)
        if dangnhap == None:
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "error")
        else:
            #Tạo session
            session["maquyen"] = dangnhap.maquyen
            session["logged_in"] = True
            #Phân quyền với 0 - Admin, 1 - Bác sĩ, 2 - Y tá, 3 - Người dùng
            if (dangnhap.maquyen == 0):
                return redirect(url_for("admin.home"))
            if (dangnhap.maquyen == 1):
                return redirect(url_for("bacsi.home"))
            if (dangnhap.maquyen == 2):
                return redirect(url_for("yta.yta_home"))
            if (dangnhap.maquyen == 3):
                return redirect(url_for("user.user_home"))
    return render_template('login.html')


@user.route('/logout')
@login_required
def user_logout():
    session.clear()
    return redirect(url_for('user.user_login'))


@user.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        session.pop('user', None)
        tentaikhoan = request.form['username']
        matkhau = request.form['password']
        matkhau_nhaplai = request.form['repassword']
        print(tentaikhoan)
        print(matkhau_nhaplai)
        print(matkhau)
        dangnhap = utils.get_taikhoan_by_usernames(tentaikhoan)
        if (dangnhap is None):
            if (matkhau == matkhau_nhaplai):
                taiKhoanMoi = TaiKhoan(tendangnhap=tentaikhoan,
                                       matkhau=matkhau,
                                       maquyen=3)
                db.session.add(taiKhoanMoi)
                db.session.commit()
                flash("Tạo tài khoản thành công", "success")
            else:
                flash("Mật khẩu nhập lại phải trùng khớp", "error")
        else:
            flash("Tài khoản đã tồn tại", "error")
    return render_template('register.html')


#--------------------Y TÁ---------------------


#Homepage
@yta.route('/home')
@login_required
def yta_home():
    return render_template('yta.html')


#Lập hoá đơn
@yta.route('/laphoadon', methods=['GET', 'POST'])
@login_required
def yta_laphoadon():
    maphieukham = request.form.get('maphieukham')
    matoa = request.form.get('matoathuoc')
    ngayban = utils.today
    dathanhtoan = 0

    try:
        phieukham_obj = utils.get_pk_by_mapk(maphieukham)
        toathuoc_obj = utils.get_toathuoc_by_matoa(matoa)
        # Tạo ra một hoá đơn có mã phiếu khám và mã toa
        # Xử lí tính tổng thu qua phiếu khám và mã toa
        if (phieukham_obj != None and toathuoc_obj != None):
            new_hoadon = HoaDon(maphieukham=maphieukham,
                                ngayban=ngayban,
                                o_phieukham=phieukham_obj,
                                o_toathuoc=toathuoc_obj,
                                tongthu=phieukham_obj.tienkham +
                                toathuoc_obj.tienthuoc,
                                dathanhtoan=False)
            db.session.add(new_hoadon)
            db.session.commit()
            print("Thêm thành công")
        else:
            print("Không lấy được đối tượng")
        return redirect(url_for("yta.yta_laphoadon"))

    except:
        print("Thêm thất bại")
    return render_template('laphoadon.html')


#CRUD Danh sách khám
#Thêm bệnh nhân khám
@yta.route('/themdskham', methods=['POST', 'GET'])
@login_required
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
@login_required
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
@login_required
def yta_danhsachkham():
    danhsachkham = utils.get_ds_all()
    return render_template('danhsachkham.html', danhsach=danhsachkham)


# Báo cáo
@yta.route('/baocao')
@login_required
def yta_baocao():
    danhsachbc = utils.get_baocao()
    return render_template('baocao.html', danhsach=danhsachbc)


#Thêm người
#--------------------BÁC SĨ--------------------


#--------------------ADMIN---------------------
def create_app():
    app.register_blueprint(yta, url_prefix='/yta')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(bacsi, url_prefix='/bacsi')
    app.register_blueprint(user, url_prefix='/')
    return app