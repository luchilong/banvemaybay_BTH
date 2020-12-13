from mainmb import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time, Enum
from sqlalchemy.orm import relationship, backref
import enum
import datetime


class LoaiGhe(enum.Enum):
    GheL1 = 1
    GheL2 = 2


lichtrinh = db.Table("lichtrinh",
                     Column('MaSB', Integer,
                            ForeignKey('Sanbay.MaSB'),
                            primary_key=True),
                     Column("MaCB", Integer,
                            ForeignKey('Chuyenbay.MaCB'),
                            primary_key=True),
                     Column('SBdi', String(50), nullable=False),
                     Column('SBden', String(50), nullable=False))


class Sanbay(db.Model):
    __tablename__ = "Sanbay"
    MaSB = Column(Integer, primary_key=True, autoincrement=True)
    TenNuocSB = Column(String(50), nullable=False)
    BangDG = relationship('BangDonGia', backref="sanbay", lazy=True)
    ChuyenBayS = relationship('Chuyenbay', secondary='lichtrinh', backref=backref("sanbay", lazy=True), lazy='subquery')
    CTChuyenBay = relationship('Chitietchuyenbay', backref="sanbay", lazy=True)


class Hangkhach(db.Model):
    __tablename__ = "Hangkhach"
    MaHK = Column(Integer, primary_key=True, autoincrement=True)
    HoTen = Column(String(50), nullable=False)
    CMND = Column(Integer, nullable=False)
    DT = Column(Integer, nullable=False)
    Vechuyenbay = relationship('Vechuyenbay', backref="sanbay", lazy=True)


class Chuyenbay(db.Model):
    __tablename__ = "Chuyenbay"
    MaCB = Column(Integer, primary_key=True, autoincrement=True)
    TenCB = Column(String(50), nullable=False)
    Ngaybay = Column(Date, nullable=False)
    TGbay = Column(Time, nullable=False)
    LGhe = Column(Enum(LoaiGhe), nullable=False)


class Bangdongia(db.Model):
    __tablename__ = "Bangdongia"
    MaDG = Column(Integer, primary_key=True, autoincrement=True)
    sanbay_MaSB = Column(Integer, ForeignKey(Sanbay.MaSB), nullable=False)
    GiaTien = Column(Float, nullable=False)


class Vechuyenbay(db.Model):
    __tablename__ = "Vechuyenbay"
    MaVCB = Column(Integer, primary_key=True, autoincrement=True)
    MaCB = Column(Integer, ForeignKey(Chuyenbay.MaCB), nullable=False)
    MaHK = Column(Integer, ForeignKey(Hangkhach.MaHK), nullable=False)
    Hangve = Column(String(50))
    MaDG = Column(Integer, ForeignKey(Bangdongia.MaDG), nullable=False)


class Phieudatcho(db.Model):
    __tablename__ = "Phieudatcho"
    MaPDC = Column(Integer, primary_key=True, autoincrement=True)
    MaVCB = Column(Integer, ForeignKey(Vechuyenbay.MaVCB), nullable=False)


class Chitietchuyenbay(db.Model):
    __tablename__ = "Chitietchuyenbay"
    MaCTLCB = Column(Integer, primary_key=True, autoincrement=True)
    MaCB = Column(Integer, ForeignKey(Chuyenbay.MaCB), nullable=False)
    MaSBchunggian = Column(Integer, ForeignKey(Sanbay.MaSB), nullable=False)
    TGstop = Column(Time)
    Ghichu = Column(String(255))


if __name__ == "__main__":
    db.create_all()