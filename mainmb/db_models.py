from mainmb import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date, Time, Enum
from sqlalchemy.orm import relationship
import enum
from enum import Enum as UseEnum
from flask_login import UserMixin, current_user


class user_role(UseEnum):
    USER = 1
    ADMIN = 2


class Hangkhach(db.Model, UserMixin):
    __tablename__ = "Hangkhach"
    id = Column(Integer, primary_key=True, autoincrement=True)
    HoTen = Column(String(50), nullable=False)
    tendangnhap = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    CMND = Column(String(50), nullable=False)
    DT = Column(String(50), nullable=True)
    Loaiacc = Column(Enum(user_role), default=user_role.USER)
    active = Column(Boolean, default=True)

    VeCB = relationship('Vechuyenbay', backref="hangkhach", lazy=True)

    def is_accessible(self):
        return False


class LoaiGhe(enum.Enum):
    GheL1 = 1
    GheL2 = 2


class Sanbay(db.Model):
    __tablename__ = "Sanbay"
    MaSB = Column(Integer, primary_key=True, autoincrement=True)
    TenNuocSB = Column(String(50), nullable=False)
    BangDG = relationship('Bangdongia', backref="sanbay", lazy=True)
    CTChuyenBay = relationship('Chitietchuyenbay', backref="sanbay", lazy=True)
    SB_trunggian = relationship('SanBayTrungGian', backref="sanbay", lazy=True)

    def is_accessible(self):
        return current_user.is_authenticated


class Chuyenbay(db.Model):

    __tablename__ = "Chuyenbay"
    MaCB = Column(Integer, primary_key=True, autoincrement=True)
    TenCB = Column(String(50), nullable=False)
    Ngaybay = Column(Date, nullable=False)
    TGbay = Column(Time, nullable=False)
    SBdi = Column(Integer, ForeignKey(Sanbay.MaSB), nullable=False)
    SBden = Column(Integer, ForeignKey(Sanbay.MaSB), nullable=False)
    LoaiGhe = Column(Enum(LoaiGhe), nullable=False)
    VeCB = relationship('Vechuyenbay', backref="chuyenbay", lazy=True)
    VeCTB = relationship('Chitietchuyenbay', backref="chuyenbay", lazy=True)
    SB_trunggian = relationship('SanBayTrungGian', backref="chuyenbay", lazy=True)
    MaSBdi = relationship('Sanbay', lazy=True, foreign_keys=[SBdi])
    MaSBden = relationship('Sanbay', lazy=True, foreign_keys=[SBden])

    def is_accessible(self):
        return current_user.is_authenticated


class Bangdongia(db.Model):
    __tablename__ = "Bangdongia"
    MaDG = Column(Integer, primary_key=True, autoincrement=True)
    sanbay_MaSB = Column(Integer, ForeignKey(Sanbay.MaSB), nullable=False)
    GiaTien = Column(Float, nullable=False)
    VeCB = relationship('Vechuyenbay', backref="Bangdongia", lazy=True)

    def is_accessible(self):
        return current_user.is_authenticated


class Vechuyenbay(db.Model):
    __tablename__ = "Vechuyenbay"
    MaVCB = Column(Integer, primary_key=True, autoincrement=True)
    MaCB = Column(Integer, ForeignKey(Chuyenbay.MaCB), nullable=False)
    MaHK = Column(Integer, ForeignKey(Hangkhach.id), nullable=False)
    Hangve = Column(String(50))
    MaDG = Column(Integer, ForeignKey(Bangdongia.MaDG), nullable=False)

    def is_accessible(self):
        return current_user.is_authenticated


class Phieudatcho(db.Model):
    __tablename__ = "Phieudatcho"
    MaPDC = Column(Integer, primary_key=True, autoincrement=True)
    MaVCB = Column(Integer, ForeignKey(Vechuyenbay.MaVCB), nullable=False)

    def is_accessible(self):
        return current_user.is_authenticated


class Chitietchuyenbay(db.Model):
    __tablename__ = "Chitietchuyenbay"
    MaCTLCB = Column(Integer, primary_key=True, autoincrement=True)
    MaCB = Column(Integer, ForeignKey(Chuyenbay.MaCB), nullable=False)
    MaSBchunggian = Column(Integer, ForeignKey(Sanbay.MaSB), nullable=False)
    TGstop = Column(Time)
    Ghichu = Column(String(255))

    def is_accessible(self):
        return current_user.is_authenticated


class SanBayTrungGian(db.Model):
    MaCB = Column(Integer, ForeignKey(Chuyenbay.MaCB), primary_key=True)
    MaSB = Column(Integer, ForeignKey(Sanbay.MaSB), primary_key=True)
    GioNghi = Column(String(255), nullable=False)

    def is_accessible(self):
        return current_user.is_authenticated


if __name__ == "__main__":
    db.create_all()