from mcp.server.fastmcp import FastMCP
import sqlite3

mcp=FastMCP("Library Management")

database=sqlite3.connect("library.db")
cursor=database.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS books(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Title TEXT NOT NULL,
Author TEXT NOT NULL,
Available INTEGER NOT NULL DEFAULT 1)''')
database.commit()

@mcp.tool()
def add_book(title:str,author:str):
    if not title.strip() or not author.strip():
        return "Error: Book title and author cannot be empty."
    cursor.execute('''INSERT INTO books(Title,Author) 
        values(?, ?)''',(title,author))
    database.commit()
    return f"Book '{title}' Succesfully Added"

@mcp.tool()
def search_book(title:str):
    cursor.execute('''Select * from books
    where "Title" like ?''',(f"%{title}%",))
    result=cursor.fetchall()
    return result

@mcp.tool()
def borrow_book(book_id:int):
    cursor.execute('''Update books set Available=0 where ID=?
    AND Available=1''',(book_id,))
    updated_row=cursor.rowcount
    if updated_row==0:
        return f"The books is not found or borrowed already."
    else:
        database.commit()
        return f"Book ID {book_id} borrowed succesfully."

@mcp.resource("library://books")
def catalogue():
    cursor.execute('''Select * from books''')
    result=cursor.fetchall()
    return result

@mcp.prompt()
def recommend_book(interst:str):
    return f"Recommend a book for a reader interested in {interst}"

mcp.run(transport="stdio")