from pydantic import BaseModel
from datetime import datetime, date


class Book(BaseModel):
    book_id: int
    book_title:str
    book_edition: str
    book_author: str
    book_publisher:str
    book_copies:int
    book_costs:float
    book_remarks: str

    class Config:
        orm_mode = True

class LibraryStaff(BaseModel):
    staff_id: int
    staff_firstname: str
    staff_lastname: str
    staff_mobilenumber:str
    staff_email:str
    staff_password:str
    staff_authsalt: str
    staff_category: str

    class Config:
        orm_mode = True



class Members(BaseModel):
    member_id: int
    member_firstname:str
    member_lastname: str
    member_dateofbirth: date
    member_gender:str
    member_mobile:str
    member_email:str

class BorrowersRecords(BaseModel):
    borrowers_id: int
    member_id:int
    staff_id: int
    borrowers_dateborrowed: datetime
    borrowers_duereturndate:datetime

class BorrowersRecordDetails(BaseModel):
    
    detail_id:int
    borrowers_id:int
    book_id:int
    detail_numberofcopies:int



class BookReturnRecords(BaseModel):
    return_id: int
    borrowers_id:int
    return_datereturned: datetime

class BookReturnRecordDetails(BaseModel):
    detail_id: int
    return_id: int
    book_id: int
    details_numberofcopies: int

    class Config:
        orm_mode= True