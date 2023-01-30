from database import Base
from sqlalchemy import String, Integer, Float, Column, Date, DateTime, ForeignKey

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    book_title = Column(String)
    book_edition= Column(String)
    book_author = Column(String)
    book_publisher = Column(String)
    book_copies= Column(Integer)
    book_costs= Column(Float)
    book_remarks= Column(String)

    def __repr__(self):
        return f"Item name = {self.book_title}"


class LibraryStaff(Base):
    __tablename__ = 'librarystaff'
    staff_id = Column(Integer, primary_key=True)
    staff_firstname = Column(String)
    staff_lastname= Column( String)
    staff_mobilenumber = Column(String)
    staff_email = Column( String)
    staff_password = Column(String)
    staff_authsalt= Column(String)
    staff_category= Column(String)


class Members(Base):
    __tablename__ = 'members'
    member_id = Column(Integer, primary_key=True)
    member_firstname = Column(String)
    member_lastname= Column( String)
    member_dateofbirth = Column(Date)
    member_gender = Column(String)
    member_mobile = Column(String)
    member_email= Column(String)


class BorrowersRecords(Base):
    __tablename__ = 'borrowersrecords'
    borrowers_id = Column(Integer, primary_key=True)
    member_id = Column(Integer)
    staff_id= Column( Integer)
    borrowers_dateborrowed = Column(DateTime)
    borrowers_duereturndate = Column(DateTime)



class BorrowersRecordDetails(Base):
    __tablename__ = 'borrowersrecorddetails'
    details_id = Column(Integer, primary_key=True)
    borrowers_id = Column(Integer)
    book_id= Column(Integer)
    detail_numberofcopies = Column(Integer)



class BookReturnRecords(Base):
    __tablename__ = 'bookreturnrecords'
    return_id = Column(Integer, primary_key=True)
    borrowers_id = Column(Integer)
    return_datereturned= Column(DateTime)




class BookReturnRecordDetails(Base):
    __tablename__ = 'bookreturnrecorddetails'
    detail_id = Column(Integer, primary_key=True)
    return_id = Column(Integer)
    book_id= Column( Integer)
    detail_numberofcopies = Column(Integer)
 

