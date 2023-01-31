from fastapi import FastAPI, HTTPException
from schema import Book, BookReturnRecordDetails, BookReturnRecords, BorrowersRecords, BorrowersRecordDetails, LibraryStaff, Members
from database import SessionLocal
import models
from datetime import datetime, date, timedelta

"""
A RESTful api project by Adedara Adeloro
To display the UI, use the url: localhost:8000/docs
"""

"""
API Version - 1.0.1
"""

db = SessionLocal()
app = FastAPI()

#-------------------------------------------------->
# End point to GET a specific book by its ID
@app.get('/Books/{books_ID}')
def get_a_book(book_ID):
    book = db.query(models.Book).filter(models.Book.book_id == book_ID).first()
    return book

#Endpoint to UPDATE a specific book by its ID
@app.put('/Books/{book_ID}')
def update_a_book(book_ID:int, book:Book):
    book_to_update = db.query(models.Book).filter(models.Book.book_id == book_ID).first()
    
    book_to_update.book_id = book.book_id
    book_to_update.book_title = book.book_title
    book_to_update.book_edition = book.book_edition
    book_to_update.book_author = book.book_author
    book_to_update.book_publisher = book.book_publisher
    book_to_update.book_copies = book.book_copies
    book_to_update.book_costs = book.book_costs
    book_to_update.book_remarks = book.book_remarks

    db.commit()
    return book_to_update

# Endpoint to DELETE a specific book by its ID
@app.delete('/Books/{book_ID}')
def delete_book(book_ID:int):
    book_to_delete = db.query(models.Book).filter(models.Book.book_id==book_ID).first()

    if book_to_delete is None:
        raise HTTPException (status_code=404, detail="Book does not exist")

    db.delete(book_to_delete)
    db.commit()

    return book_to_delete

#-------------------------------------------------->
#Endpoint to GET ALL books, by directly calling the book table
@app.get('/Books', status_code=200)
def get_all_books():
    books = db.query(models.Book).all()
    return books

#Endpoint to create a book and add it to the book table
@app.post('/Books')
def create_book(book:Book):
    new_book = models.Book(
        book_id = book.book_id,
        book_title = book.book_title,
        book_edition= book.book_edition,
        book_author = book.book_author,
        book_publisher = book.book_publisher,
        book_copies= book.book_copies,
        book_costs= book.book_costs,
        book_remarks= book.book_remarks
    )

    db_book = db.query(models.Book).filter(models.Book.book_id == new_book.book_id).first()
    if db_book is not None:
        raise HTTPException(status_code=400, detail= 'Book already exists')
    db.add(new_book)
    db.commit
    return new_book
#-------------------------------------------------->


# Endpoint to get a specific book by its AUTHOR
@app.get('/Books/ByAuthor/{author}')
def get_book_author(author:str):
    book_by_author = db.query(models.Book).filter(models.Book.book_author ==  author).first()
    return book_by_author
#-------------------------------------------------->

#Endpoint to get a specific book by its PUBLISHER
@app.get('/Books/ByPublisher/{publisher}')
def get_book_publisher(publisher:str):
    book_by_publisher = db.query(models.Book).filter(models.Book.book_publisher ==  publisher).first()
    return book_by_publisher
#-------------------------------------------------->

#Endpoint to get book borrowed in the last 30 days
"""
Logic behind it: This endpoint uses foreign keys. 
In this case, the table BorrowerRecords has a column for the 
dates the books were borrowed. We use this to calcuate for the time period a book has been borrowed for

The table also has a column for Borrowers ID, 
which is a primary key in this table but a foreign key in the BorrowerRecordDetails table.
This key leads us to the table BorrowersRecordDetails

In this BorrowersRecordDetails, the table has a column for the book ID borrowed 
by each entity with the BorrowerID that led us to this table. 
So we get the information for each book borrowed by linking us to the Book table through the foriegn key : BookID
"""
@app.get('/Books/Borrowed/Last30Days')
def get_book_borrowed_30():
    """today = datetime.today()
    borrowRecordJson = db.query(models.BorrowersRecords).all()
    dates_borrowed = [borrowRecordJson[i].borrowers_dateborrowed for i in range(0, len(borrowRecordJson))
                             if (today - (borrowRecordJson[i].borrowers_dateborrowed))/86400 < 30]
    diff = (today - (borrowRecordJson[0].borrowers_dateborrowed))/86400
    return float(diff)
    #  return (today - dates_borrowed[0])/86400
"""


    

    
#-------------------------------------------------->


#For Books Borrowed At SpecificTimePeriod
"""
This Endpoint also implements the same logic used as in the Books/Borrowed/Last30Days endpoint.
But instead of using the current time to calculate the time period a book was borrowed, 
it uses a time period specified by a user
"""
@app.get('/Books/Borrowed/{DateFrom}/{DateTo}')
def get_book_borrowed_time(DateFrom, DateTo):
    pass
#-------------------------------------------------->



"""
This endpoint also uses a foreign key, in the table: BorrowersRecords.

The 'userID' in this case, stands for the member_ID, which is already present in this table.
The table has the borrowerID, which will link us to the BorrowerRecordDetails table, 
This new table has the BookID, which will lead us to the Book table
which is where we would get the book details borrowed by the member
"""
#For Books Borrowed by UserID
@app.get('/Books/Borrowed/{UserID}')
def get_book_borrowed_by_member(UserID:int):

    BorrowRecordsJsonList = db.query(models.BorrowersRecords).filter(models.BorrowersRecords.member_id == UserID).all()
    if BorrowRecordsJsonList is None:
        raise HTTPException(status_code=404, detail = "Borrower Does Not Exist!")
    
    #JSON LIST HANDLER
    length = len(BorrowRecordsJsonList)
    borrow_id_list = [BorrowRecordsJsonList[n].borrowers_id for n in range(0, length)]
    BorrowersRecordDetailsJsonList = [db.query(models.BorrowersRecordDetails).filter(models.BorrowersRecordDetails.borrowers_id == i).first() for i in borrow_id_list]
    BRDJL_without_None = [j for j in BorrowersRecordDetailsJsonList if j is not None]
    
    #SECOND JSON LIST HANDLER
    book_id_list = [BRDJL_without_None[k].book_id for k in range(0, len(BRDJL_without_None)) ]
    BookJsonList = [db.query(models.Book).filter(models.Book.book_id == i ).first() for i in book_id_list]
    return BookJsonList
#-------------------------------------------------->


#For Books Borrowed and approved by USERID/LibraryStaffID
@app.get('/Books/Borrowed/Approved/By/{staff_id}')
def get_book_borrowed_approved(staff_id:int):
    StaffRecordJsonList = db.query(models.BorrowersRecords).filter(models.BorrowersRecords.staff_id == staff_id).all()
    if StaffRecordJsonList is None:
        raise HTTPException(status_code=404, detail = "Staff Has Not Borrowed Anyone!")
    
    #JSON LIST HANDLER
    length = len(StaffRecordJsonList)
    borrow_id_list = [StaffRecordJsonList[n].borrowers_id for n in range(0, length)]
    BorrowersRecordDetailsJsonList = [db.query(models.BorrowersRecordDetails).filter(models.BorrowersRecordDetails.borrowers_id == i).first() for i in borrow_id_list]
    BRDJL_without_None = [j for j in BorrowersRecordDetailsJsonList if j is not None]
    
    #SECOND JSON LIST HANDLER
    book_id_list = [BRDJL_without_None[k].book_id for k in range(0, len(BRDJL_without_None)) ]
    BookJsonList = [db.query(models.Book).filter(models.Book.book_id == i ).first() for i in book_id_list]
    return BookJsonList
#-------------------------------------------------->

#For Books Borrowed for BookID
@app.get('/Book/Borrowed/{UserID}')
def get_book_borrowed_BorrowID(UserID:int):
    BorrowRecordsJsonList = db.query(models.BorrowersRecords).filter(models.BorrowersRecords.member_id == UserID).all()
    if BorrowRecordsJsonList is None:
        raise HTTPException(status_code=404, detail = "Borrower Does Not Exist!")
    
    #JSON LIST HANDLER
    length = len(BorrowRecordsJsonList)
    borrow_id_list = [BorrowRecordsJsonList[n].borrowers_id for n in range(0, length)]
    BorrowersRecordDetailsJsonList = [db.query(models.BorrowersRecordDetails).filter(models.BorrowersRecordDetails.borrowers_id == i).first() for i in borrow_id_list]
    BRDJL_without_None = [j for j in BorrowersRecordDetailsJsonList if j is not None]
    
    #SECOND JSON LIST HANDLER
    book_id_list = [BRDJL_without_None[k].book_id for k in range(0, len(BRDJL_without_None)) ]
    BookJsonList = [db.query(models.Book).filter(models.Book.book_id == i ).first() for i in book_id_list]
    return BookJsonList
#===============================================================>


#===============================================================>
#For Borrowed By BorrowID
@app.get('/Borrowed/{ID}')
def get_borrowed(BorrowID:int):
        books_borrowed_borrowID = db.query(models.BorrowersRecords).filter(models.BorrowersRecords.borrowers_id == BorrowID).first()
        return books_borrowed_borrowID

@app.put('/Borrowed/{ID}')
def update_borrowed(ID:int, borrow:BorrowersRecords ):
        borrow_to_update = db.query(models.BorrowersRecords).filter(models.BorrowersRecords.borrowers_id == ID).first()

        borrow_to_update.borrowers_id = borrow.borrowers_id 
        borrow_to_update.member_id = borrow.member_id 
        borrow_to_update.staff_id = borrow.staff_id 
        borrow_to_update.borrowers_dateborrowed = borrow.borrowers_dateborrowed 
        borrow_to_update.borrowers_duereturndate = borrow.borrowers_duereturndate
 
        db.commit()
        return borrow_to_update


@app.delete('/Borrowed/{ID}')
def delete_borrowed(ID):
    borrow_to_delete = db.query(models.BorrowersRecords).filter(models.BorrowersRecords.borrowers_id==ID).first()

    if borrow_to_delete is None:
        raise HTTPException (status_code=404, detail="Borrower does not exist")

    db.delete(borrow_to_delete)
    db.commit()
#-------------------------------------------------->


#For Borrowed (WITHOUT ID)
@app.get('/Borrowed/')
def get_all_borrowed():
    return db.query(models.BorrowersRecords).all()

@app.post('/Borrowed/')
def create_borrowed(new_borrow:BorrowersRecords):
        new_borrowed = models.BorrowersRecords(
            borrowers_id = new_borrow.borrowers_id,
            member_id = new_borrow.member_id,
            staff_id = new_borrow.staff_id,
            borrowers_dateborrowed = new_borrow.borrowers_dateborrowed,
            borrowers_duereturndate = new_borrow.borrowers_duereturndate,
    )

        db_book = db.query(models.BorrowersRecords).filter(models.BorrowersRecords.borrowers_id == new_borrowed.borrowers_id).first()
        if db_book is not None:
            raise HTTPException(status_code=400, detail= 'Book already exists')
        db.add(new_borrowed)
        db.commit
        return new_borrowed
#==================================================>

#For Books Returned (WITH ID)
@app.get('/Returned/{ID}')
def get_returned(ID):
    return db.query(models.BookReturnRecords).filter(models.BookReturnRecords.return_id == ID).first()

@app.put('/Returned/{ID}')
def update_returned(ID, returned:BookReturnRecords):
        returned_to_update = db.query(models.BookReturnRecords).filter(models.BookReturnRecords.return_id == ID).first()

        returned_to_update.return_id = returned.return_id
        returned_to_update.borrowers_id = returned.borrowers_id
        returned_to_update.return_datereturned = returned.return_datereturned
 
        db.commit()
        return returned_to_update

@app.delete('/Returned/{ID}')
def delete_returned(ID):
    returned_to_delete = db.query(models.BookReturnRecords).filter(models.BookReturnRecords.return_id==ID).first()

    if returned_to_delete is None:
        raise HTTPException (status_code=404, detail="Return_ID does not exist")

    db.delete(returned_to_delete)
    db.commit()

    return returned_to_delete
#-------------------------------------------------->


#For Returned (WITHOUT ID)
@app.get('/Returned/')
def get_all_returned():
    return db.query(models.BookReturnRecords).all()

@app.post('/Returned/')
def create_returned(new_returned:BookReturnRecords):
    new_returned = models.BookReturnRecords(
        return_id= new_returned.return_id,
        borrowers_id= new_returned.borrowers_id,
        return_datereturned= new_returned.return_datereturned,
    )

    db_returned_book = db.query(models.BookReturnRecords).filter(models.BookReturnRecords.return_id == new_returned).first()
    if db_returned_book is not None:
        raise HTTPException(status_code=400, detail= 'Return already exists!')
    db.add(new_returned)
    db.commit()
    return new_returned

#-------------------------------------------------->