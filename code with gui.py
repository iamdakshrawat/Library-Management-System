import mysql.connector
from datetime import date,timedelta
import tkinter as tk
from tkinter import messagebox
connection = mysql.connector.connect(host="localhost",user="root",password="Daksh@123",database="library")
cursor = connection.cursor()
gui=tk.Tk()
gui.title("Library Management System")
gui.geometry("315x340+600+150") #size of box + posiotion of box
gui.minsize(315,340)
gui.maxsize(315,340)
gui.configure(bg='#856ff8')


def main():
    cursor.execute("select book_id from books")
    bookid_list=[] #empty list to store all book id's
    for i in cursor:
        bookid_list.append(i[0])
    #Label(parent window/master, command/option)
    menu_label=tk.Label(gui,text="Welcome to our Library",font=('Ariel 20 bold underline'),fg='red',bg='yellow')
    empty_label = tk.Label(text="",bg='#856ff8')
    table_button = tk.Button(gui,text="1- Show Tables", font='8', command=show_tables, width=20)
    alter_button = tk.Button(gui,text="2- Alter Library Books", font='8', command= lambda: alter_library(bookid_list), width=20)
    issue_button = tk.Button(gui,text="3- Issue Book", font='8', command= lambda: issue_book(bookid_list), width=20)
    return_button = tk.Button(gui,text="4- Return Book", font='8', command= lambda: return_book(bookid_list), width=20)
    exit_button = tk.Button(gui,text="5- Exit", font='8', command=exit, width=20)

    menu_label.grid(row=0, column=0)
    empty_label.grid(row=1, column=0, pady=1)
    table_button.grid(row=2, column=0, pady=5)
    alter_button.grid(row=3, column=0, pady=5)
    issue_button.grid(row=4, column=0, pady=5)
    return_button.grid(row=5, column=0, pady=5)
    exit_button.grid(row=6, column=0, pady=5)


def show_tables():

    def show_books():
        tables_window.withdraw() #this will hide the previous window which here was the tables_window
        books_window = tk.Toplevel(tables_window)
        books_window.title("Books")
        books_window.geometry("460x380+545+100") #size of box + posiotion of box
        books_window.minsize(460,380)
        books_window.maxsize(460,380)
        books_window.configure(bg='#856ff8')
        books_window.protocol("WM_DELETE_WINDOW", lambda: (books_window.destroy(),tables_window.deiconify()))

        book_label = tk.Label(books_window, text="( Book Id , Book Name , Author Name , Quantity)",font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        book_label.pack()

        cursor.execute("SELECT * FROM books")
        books_info = "(Book ID, Book name, Author name, Quantity)\n"   
        for row in cursor:
            book_info = f"{(row[0], row[1], row[2], row[3])}\n\n"
            books_info += book_info
        
        books_text = tk.Text(books_window, font=('Ariel 10 bold'),fg='black',bg='#AEF16B', height=20, width=50)
        books_text.tag_configure("center", justify="center")
        books_text.insert(tk.END, books_info,"center")
        books_text.pack(pady=10)
        
    def show_currently_borrowed():
        tables_window.withdraw()
        borrowed_books_window = tk.Toplevel(tables_window)
        borrowed_books_window.title("Borrowed Books")
        borrowed_books_window.geometry("460x380+545+100") #size of box + posiotion of box
        borrowed_books_window.minsize(460,380)
        borrowed_books_window.maxsize(460,380)
        borrowed_books_window.configure(bg='#856ff8')
        borrowed_books_window.protocol("WM_DELETE_WINDOW", lambda: (borrowed_books_window.destroy(),tables_window.deiconify()))

        borrowed_label = tk.Label(borrowed_books_window, text="(Std ID , Book ID , Date of Issue , Due Date)",font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        borrowed_label.pack()

        cursor.execute("SELECT * FROM currently_borrowed")
        books_info = "(Std ID, Book ID, Issue Date, Due Date)\n\n"   
        for row in cursor:
            book_info = f"{(row[0], row[1], row[2], row[3])}\n"
            books_info += book_info
        
        books_text = tk.Text(borrowed_books_window, font=('Ariel 10 bold'),fg='black',bg='#AEF16B', height=20, width=80)
        books_text.tag_configure("center", justify="center")
        books_text.insert(tk.END, books_info,"center")
        books_text.pack(pady=10)

    def show_borrowing_history():
        tables_window.withdraw()
        borrowing_history_window = tk.Toplevel(tables_window)
        borrowing_history_window.title("Borrowing History")
        borrowing_history_window.geometry("470x600+545+100") #size of box + posiotion of box
        borrowing_history_window.minsize(470,380)
        borrowing_history_window.maxsize(470,380)
        borrowing_history_window.configure(bg='#856ff8')
        borrowing_history_window.protocol("WM_DELETE_WINDOW", lambda: (borrowing_history_window.destroy(),tables_window.deiconify()))

        history_label = tk.Label(borrowing_history_window, text="(Std ID , Book ID , Date of Issue , Due Date , Fine)",font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        history_label.pack()

        cursor.execute("SELECT * FROM borrowing_history")
        books_info = "(Std ID, Book ID, Issue Date, Return Date, Fine)\n\n"   
        for row in cursor:
            book_info = f"{(row[0], row[1], row[2], row[3], row[4])}\n"
            books_info += book_info
        
        books_text = tk.Text(borrowing_history_window, font=('Ariel 10 bold'),fg='black',bg='#AEF16B', height=20, width=100)
        books_text.tag_configure("center", justify="center")
        books_text.insert(tk.END, books_info,"center")
        books_text.pack(pady=10)

    gui.withdraw()
    tables_window = tk.Toplevel(gui)
    tables_window.title("Tables")
    tables_window.protocol("WM_DELETE_WINDOW", lambda: (tables_window.destroy(), gui.deiconify()))
    tables_window.geometry("444x220+550+150") #size of box + posiotion of box
    tables_window.minsize(444,220)
    tables_window.maxsize(444,220)
    tables_window.configure(bg='#856ff8')
    table_label = tk.Label(tables_window, text="Select table you would like to see", font=('Ariel 20 bold underline'),fg='red',bg='yellow')
    empty_label = tk.Label(tables_window,text="",bg='#856ff8')
    books_button = tk.Button(tables_window,text="1- Show Books", font='8', command=show_books, width=30)
    currently_button = tk.Button(tables_window,text="2- Show currently borrowed books", font='8', command=show_currently_borrowed, width=30)
    history_button = tk.Button(tables_window,text="3- Show entire borrowing history", font='8', command=show_borrowing_history, width=30)

    table_label.grid(row=0, column=0)
    empty_label.grid(row=1, column=0, pady=1)
    books_button.grid(row=2, column=0, pady=5)
    currently_button.grid(row=3, column=0, pady=5)
    history_button.grid(row=4, column=0, pady=5)


def issue_book(bookid_list):
    def issue():
        student_id = int(std_entry.get())
        cursor.execute("SELECT COUNT(student_id) FROM currently_borrowed WHERE student_id = %s", (student_id,))
        data = cursor.fetchone()
        if data[0] >= 3:
            messagebox.showwarning("Issue Book", f"Maximum limit reached for ID {student_id}. No more books can be issued.")
            issue_window.destroy()
            gui.deiconify()
            return
        def issuing():
            issued_books = []
            cursor.execute("SELECT book_id FROM currently_borrowed WHERE student_id = %s", (student_id,))
            for row in cursor:
                issued_books.append(row[0])

            book_id = int(book_entry.get())
            if book_id not in bookid_list:
                ans= messagebox.askyesno("Issue Book", "No such book available in the library. Want to issue other book?")
                if not ans:
                    issue_books_window.destroy()
                    issue_window.destroy()
                    gui.deiconify()
                else:
                    issue_books_window.destroy()
                    issue_window.deiconify()
            elif book_id in issued_books:
                ans= messagebox.askyesno("Issue Book", "This book is already with you. Want to issue other book?")
                if not ans:
                    issue_books_window.destroy()
                    issue_window.destroy()
                    gui.deiconify()
                else:
                    issue_books_window.destroy()
                    issue_window.deiconify()
            elif book_id in bookid_list and book_id not in available_books:
                ans= messagebox.askyesno("Issue Book", "Sorry! This book is currently out of stock. Want to issue other book?")
                if not ans:
                    issue_books_window.destroy()
                    issue_window.destroy()
                    gui.deiconify()
                else:
                    issue_books_window.destroy()
                    issue_window.deiconify()
            else:
                issue_date = date.today()
                return_date = issue_date + timedelta(30)
                cursor.execute("INSERT INTO currently_borrowed VALUES (%s, %s, %s, %s)",
                               (student_id, book_id, issue_date, return_date))
                cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
                connection.commit()
                ans= messagebox.askyesno("Issue Book", "Book issued successfully!!! Want to issue other book?")
                if not ans:
                    issue_books_window.destroy()
                    issue_window.destroy()
                    gui.deiconify()
                else:
                    issue_books_window.destroy()
                    issue_window.deiconify()
        

        available_books = []
        cursor.execute("SELECT book_id FROM books WHERE quantity > 0")
        for row in cursor:
            available_books.append(row[0])

        issue_books_window = tk.Toplevel(issue_window)
        issue_books_window.title("Issue Books")
        issue_books_window.protocol("WM_DELETE_WINDOW", lambda: (issue_window.destroy() ,issue_books_window.destroy(), issue_book(bookid_list)))
        issue_books_window.geometry("490x520+550+120") #size of box + posiotion of box
        issue_books_window.minsize(490,520)
        issue_books_window.maxsize(490,520)
        issue_books_window.configure(bg='#856ff8')

        cursor.execute("SELECT book_id, book_name FROM books WHERE quantity > 0")
        books_info = "Available Stock\n"
        for row in cursor:
            book_info = f"{row[0]} ---> {row[1]}\n"
            books_info += book_info

        heading_label = tk.Label(issue_books_window, text="3 total books can be issued with 1 ID.", font=('Ariel 20 bold underline'),fg='red',bg='yellow') 
        books_text = tk.Text(issue_books_window, font=('Ariel 10 bold'),fg='black',bg='cyan', height=20, width=30)
        books_text.tag_configure("center", justify="center")
        books_text.insert(tk.END, books_info,"center")
        book_label = tk.Label(issue_books_window, text="Enter Book ID to issue:", font=('Ariel 20 bold underline'),fg='red',bg='yellow')
        book_entry = tk.Entry(issue_books_window, width=15, font=('Ariel 15'))
        submit_button = tk.Button(issue_books_window, text="Submit", font='8', command=issuing, width=8)
        
        heading_label.pack()
        books_text.pack(pady=5)
        book_label.pack(pady=5)
        book_entry.pack(pady=10)
        submit_button.pack(pady=10)


    gui.withdraw()
    issue_window = tk.Toplevel(gui)
    issue_window.title("Issue Book")
    issue_window.protocol("WM_DELETE_WINDOW", lambda: (issue_window.destroy(), gui.deiconify()))
    issue_window.geometry("315x160+600+150") #size of box + posiotion of box
    issue_window.minsize(315,160)
    issue_window.maxsize(315,160)
    issue_window.configure(bg='#856ff8')
    std_label = tk.Label(issue_window, text="Enter Student ID:", font=('Ariel 20 bold underline'),fg='red',bg='yellow')
    std_entry = tk.Entry(issue_window, width=20, font=('Ariel 20'))
    issue_button = tk.Button(issue_window, text="Continue", font='8', command=issue, width=8)

    std_label.grid(row=0, column=0)
    std_entry.grid(row=1, column=0, padx= 5, pady=10)
    issue_button.grid(row=2, column=0, pady=15)


def return_book(bookid_list):
    def return_submit():
        student_id = int(std_entry.get())
        cursor.execute("SELECT COUNT(student_id) FROM currently_borrowed WHERE student_id = %s", (student_id,))
        data = cursor.fetchone()
        if data[0] == 0:
            messagebox.showinfo("Return Book", f"No books are with ID {student_id}.")
            return_window.destroy()
            gui.deiconify()
            return
        def returning():
            book_id = int(book_entry.get())
            if book_id not in bookid_list:
                ans= messagebox.askyesno("Return Book", "No such book available in library.  Want to return some other book?")
                if not ans:
                    return_books_window.destroy()
                    return_window.destroy()
                    gui.deiconify()
                else:
                    return_books_window.destroy()
                    return_window.deiconify()

            elif book_id in bookid_list and book_id not in issued_books:
                ans= messagebox.askyesno("Return Book", "You don't have this book with you. Want to return some other book?")
                if not ans:
                    return_books_window.destroy()
                    return_window.destroy()
                    gui.deiconify()
                else:
                    return_books_window.destroy()
                    return_window.deiconify()

            else:
                cursor.execute("SELECT * FROM currently_borrowed WHERE student_id = %s AND book_id = %s",(student_id, book_id))
                data = cursor.fetchone()
                issue_date = data[2]
                return_date = data[3]
                today_date = date.today()
                diff = (today_date - return_date).days
                if diff <= 0:
                    messagebox.showinfo("Return Book", "Thank you for returning the book on time. Have a nice day!!!")
                    fine = 0
                else:
                    fine = diff * 5
                    messagebox.showinfo("Return Book", f"Book returned successfully!!!. Fine to be paid is rupees {fine}.")
                cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))
                cursor.execute("DELETE FROM currently_borrowed WHERE student_id = %s AND book_id = %s",(student_id, book_id))
                cursor.execute("INSERT INTO borrowing_history VALUES (%s, %s, %s, %s, %s)",(student_id, book_id, issue_date, today_date, fine))
                connection.commit()
                ch= messagebox.askyesno("Return Book", "Want to return some other book?")
                if not ch:
                    return_books_window.destroy()
                    return_window.destroy()
                    gui.deiconify()
                else:
                    return_books_window.destroy()
                    return_window.deiconify()
        return_books_window = tk.Toplevel(return_window)
        return_books_window.title("Return Books")
        return_books_window.protocol("WM_DELETE_WINDOW", lambda: (return_window.destroy() ,return_books_window.destroy(), return_book(bookid_list)))
        return_books_window.geometry("320x320+550+120") #size of box + posiotion of box
        return_books_window.minsize(320,320)
        return_books_window.maxsize(320,320)
        return_books_window.configure(bg='#856ff8')

        issued_books = []
        cursor.execute("SELECT book_id FROM currently_borrowed WHERE student_id = %s", (student_id,))
        for row in cursor:
            issued_books.append(row[0])

        books_info = "Books with you are-\n"
        for book in issued_books:
            books_info += f"{book}\n"

        return_label = tk.Label(return_books_window, text="Books to return:", font=('Ariel 20 bold underline'),fg='red',bg='yellow')
        books_text = tk.Text(return_books_window, font=('Ariel 15 bold'),fg='black',bg='cyan', height=5, width=20)
        books_text.tag_configure("center", justify="center")
        books_text.insert(tk.END, books_info,"center")
        book_label = tk.Label(return_books_window, text="Enter Book ID to return:", font=('Ariel 20 bold underline'),fg='red',bg='yellow')
        book_entry = tk.Entry(return_books_window, width=15, font=('Ariel 15'))
        submit_button = tk.Button(return_books_window, text="Submit", font='8', command=returning, width=8)

        return_label.pack()
        books_text.pack(pady=5)
        book_label.pack(pady=5)
        book_entry.pack(pady=10)
        submit_button.pack(pady=10)


    gui.withdraw()
    return_window = tk.Toplevel(gui)
    return_window.title("Return Book")
    return_window.protocol("WM_DELETE_WINDOW", lambda: (return_window.destroy(), gui.deiconify()))
    return_window.geometry("315x160+600+150") #size of box + posiotion of box
    return_window.minsize(315,160)
    return_window.maxsize(315,160)
    return_window.configure(bg='#856ff8')
    std_label = tk.Label(return_window, text="Enter Student ID:", font=('Ariel 20 bold underline'),fg='red',bg='yellow')
    std_entry = tk.Entry(return_window, width=20, font=('Ariel 20'))
    return_button = tk.Button(return_window, text="Continue", font='8', command=return_submit, width=8)

    std_label.grid(row=0, column=0)
    std_entry.grid(row=1, column=0, padx= 5, pady=10)
    return_button.grid(row=2, column=0, pady=15)


def alter_library(bookid_list):
    def update_stock():
        def update_submit():
            book_id = int(book_id_entry.get())
            if book_id not in bookid_list:
                messagebox.showinfo("Update Stock", "No such Book exists in the record!")
                alter_window.destroy()
                update_stock_window.destroy()
                gui.deiconify()
            else:
                quantity = int(quantity_entry.get())
                cursor.execute("UPDATE books SET quantity = quantity + %s WHERE book_id = %s", (quantity, book_id))
                connection.commit()
                messagebox.showinfo("Update Stock", "Data updated successfully!")
                alter_window.destroy()
                update_stock_window.destroy()
                gui.deiconify()


        alter_window.withdraw()
        update_stock_window = tk.Toplevel(alter_window)
        update_stock_window.title("Update Stock")
        update_stock_window.protocol("WM_DELETE_WINDOW", lambda: (update_stock_window.destroy(), alter_window.deiconify()))
        update_stock_window.geometry("425x250+545+150") #size of box + posiotion of box
        update_stock_window.minsize(425,250)
        update_stock_window.maxsize(425,250)
        update_stock_window.configure(bg='#856ff8')
        book_id_label = tk.Label(update_stock_window, text="Enter Book ID whose stock is to be updated:", font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        book_id_entry = tk.Entry(update_stock_window, width=20, font=('Ariel 20'))
        quantity_label = tk.Label(update_stock_window, text="Enter amount to be updated:", font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        quantity_entry = tk.Entry(update_stock_window, width=20, font=('Ariel 20'))
        submit_button = tk.Button(update_stock_window, text="Submit", font='8', command=update_submit, width=10)
        
        book_id_label.grid(row=0, column=0)
        book_id_entry.grid(row=1, column=0, pady=10)
        quantity_label.grid(row=2, column=0, pady=10)
        quantity_entry.grid(row=3, column=0, pady=5)
        submit_button.grid(row=4, column=0, pady=20)
    

    def add_book():
        def add_submit():
            book_id = int(id_entry.get())
            if book_id in bookid_list:
                messagebox.showinfo("Add Book", "Book already exists in the record!")
                alter_window.destroy()
                add_book_window.destroy()
                gui.deiconify()
            else:
                book = book_entry.get()
                author = author_entry.get()
                quantity = int(quantity_entry.get())
                cursor.execute("INSERT INTO books VALUES (%s, %s, %s, %s)", (book_id, book, author, quantity))
                connection.commit()
                messagebox.showinfo("Add Book", "Data added successfully!")
                alter_window.destroy()
                add_book_window.destroy()
                gui.deiconify()


        alter_window.withdraw()
        add_book_window = tk.Toplevel(alter_window)
        add_book_window.title("Add Book")
        add_book_window.protocol("WM_DELETE_WINDOW",  lambda: (add_book_window.destroy(), alter_window.deiconify()))
        add_book_window.geometry("235x340+630+150") #size of box + posiotion of box
        add_book_window.minsize(235,340)
        add_book_window.maxsize(235,340)
        add_book_window.configure(bg='#856ff8')
        id_label = tk.Label(add_book_window, text="Enter book ID:", font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        id_entry = tk.Entry(add_book_window, width=20, font=('Ariel 15'))
        book_label = tk.Label(add_book_window, text="Enter Book name:", font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        book_entry = tk.Entry(add_book_window, width=20, font=('Ariel 15'))
        author_label = tk.Label(add_book_window, text="Enter Author name:", font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        author_entry = tk.Entry(add_book_window, width=20, font=('Ariel 15'))
        quantity_label = tk.Label(add_book_window, text="Enter quantity:", font=('Ariel 15 bold underline'),fg='red',bg='yellow')
        quantity_entry = tk.Entry(add_book_window, width=20, font=('Ariel 15'))
        submit_button = tk.Button(add_book_window, text="Submit",  font='8', command=add_submit, width=10)

        id_label.grid(row=0, column=0)
        id_entry.grid(row=1, column=0, padx=5, pady=5)
        book_label.grid(row=2, column=0, pady=5)
        book_entry.grid(row=3, column=0, padx=5, pady=5)
        author_label.grid(row=4, column=0, pady=5)
        author_entry.grid(row=5, column=0, padx=5, pady=5)
        quantity_label.grid(row=6, column=0, pady=5)
        quantity_entry.grid(row=7, column=0, padx=5, pady=5)
        submit_button.grid(row=8, column=0, pady=5)



    gui.withdraw()
    alter_window = tk.Toplevel(gui)
    alter_window.title("Alter Library")
    alter_window.protocol("WM_DELETE_WINDOW", lambda: (alter_window.destroy(), gui.deiconify()))
    alter_window.geometry("363x165+575+150") #size of box + posiotion of box
    alter_window.minsize(363,165)
    alter_window.maxsize(363,165)
    alter_window.configure(bg='#856ff8')
    alter_label = tk.Label(alter_window, text="What would you like to do?", font=('Ariel 20 bold underline'),fg='red',bg='yellow')
    empty_label = tk.Label(alter_window,text="",bg='#856ff8')
    update_button = tk.Button(alter_window,text="1- Update current book stock", font='8', command=update_stock, width=30)
    add_button = tk.Button(alter_window,text="2- Add new books", font='8', command=add_book, width=30)

    alter_label.grid(row=0, column=0)
    empty_label.grid(row=1, column=0, pady=1)
    update_button.grid(row=2, column=0, pady=5)
    add_button.grid(row=3, column=0, pady=5)


#calling main function to start the program
main()
#this will execute the main tkinter file which we declared in starting with variable named 'gui' 
gui.mainloop()
