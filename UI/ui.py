import datetime
import os
from msvcrt import getch


from peewee import MySQLDatabase, InternalError as PeeweeInternalError
from Book.book import Book
from Library.library import Library


class Ui:

    def __init__(self):
        self.library = Library(
            data_base=MySQLDatabase('library', user='hanaan', password='X9G-Hd5-vt6-TMV', host='localhost', port=3306))
        self.library.connect()

    def print_all(self):
        os.system('cls')
        print("Нажмите <Esc> для выхода в главное меню или <Enter> для вывода всех книг")
        key = ord(getch())
        if key == 27:
            return
        while True:
            os.system('cls')
            books = self.library.get_all_books()
            print('ID   Название   Автор   Год')
            for result in books:
                (book_id, book) = result
                formatted_book = "%s: %s, %s %s" % (book_id, book.title, book.author, book.year)
                print(formatted_book)
            print("Нажмите <Esc> для выхода или <Enter> для повторного вывода")
            key = ord(getch())
            if key == 27:
                return

    def find_books_year(self):
        while True:
            os.system("cls")
            year = input("Введите год книги:")
            book = self.library.find_by_year(year)
            if not book:
                print('Книга с данным годом не найдена.\nХотите попробовать другой год - 1 \nили выйти - <Esc>')
                key = ord(getch())
                if key == 27:
                    return
                else:
                    self.find_books_year()
            print("Найдено: ", book)
            return book

    def find_books_author(self):
        while True:
            os.system("cls")
            author = input("Введите автора книги:")
            book = self.library.find_by_author(author)
            if not book:
                print('Книга с данным автором не найдена.\nХотите попробовать другого автора - 1 \nили выйти - <Esc>')
                key = ord(getch())
                if key == 27:
                    return
                else:
                    self.find_books_author()
            print("Найдено: ", book)
            return book

    def find_books_title(self):
        while True:
            os.system("cls")
            title = input("Введите название книги:")
            book = self.library.find_by_title(title)
            if not book:
                print(
                    'Книга с данным названием не найдена.\nХотите попробовать другое название - 1 \nили выйти - <Esc>')
                key = ord(getch())
                if key == 27:
                    return
                else:
                    self.find_books_title()
            print("Найдено: ", book)
            return book

    def find_books(self):
        os.system("cls")
        while True:
            os.system("cls")
            print(
                "Произвести поиск по \nНазванию - 1 \nАвтору - 2 \nГоду - 3 \nИли <Esc> для выхода \nВведите соотвествующее число: ")
            search = ord(getch())
            if search == 27:
                return
            elif search == 51:
                self.find_books_year()
            elif search == 50:
                self.find_books_author()
            elif search == 49:
                self.find_books_title()
            print("Нажмите <Esc> для выхода или <Enter> для повторного поиска")
            key = ord(getch())
            if key == 27:
                return

    def change_title(self, book_number, book):
        os.system("cls")
        title = input("Введите название книги (пусто, чтобы оставить без изменений):")
        if title == "" or book.title == title:
            input("Книга не изменена")
            return
        book.title = title
        self.library.update_at(book_number, book)

    def change_author(self, book_number, book):
        os.system("cls")
        author = input("Введите автора книги (пусто, чтобы оставить без изменений):")
        if author == "" or book.author == author:
            input("Книга не изменена")
            return
        book.author = author
        self.library.update_at(book_number, book)

    def change_year(self, book_number, book):
        os.system("cls")
        year = input("Введите год книги (пусто, чтобы оставить без изменений):")
        if year == "" or book.year == year:
            input("Книга не изменена")
            return
        book.year = year
        self.library.update_at(book_number, book)

    def update_book(self):
        os.system("cls")
        print("Нажмите <Esc> для выхода в главное меню или <Enter> для продолжения изменения книги")
        key = ord(getch())
        if key == 27:
            return
        while True:
            os.system('cls')
            book_id = int(input("Введите номер книги которую необходимо обновить:"))
            while book_id <= 0:
                os.system('cls')
                book_id = int(input('Введите номер книги еще раз: '))
            book = self.library.get_at(book_id)

            while not Book:
                print("Книга не найдена. Нажмите <Esc> для выхода\n Или <Enter> если хотите попробовать еще раз")
                key = ord(getch())
                if key == 27:
                    return
                if key == 13:
                    break

            print("Изменение книги: ", book,
                  "\nЧто необходимо изменить? \n1-Название \n2-Автор \n3-Год \n<Esc> для выхода")
            change_option = ord(getch())
            if change_option == 27:
                return
            if change_option == 49:
                self.change_title(book_id, book)
            elif change_option == 50:
                self.change_author(book_id, book)
            elif change_option == 51:
                self.change_year(book_id, book)

            if change_option == 49 or 50 or 51:
                print("Применить изменения\n %s? \n 1-Да\n 2-Нет" % book)
                change_option = ord(getch())

                if change_option == 49:
                    self.library.update_at(book_id, book=book)
                    print("Изменена книга ", book)
                else:
                    print("Нажмите <Esc> для выхода")
                    key = ord(getch())
                    if key == 27:
                        return

    def add_book(self):
        os.system("cls")
        while True:
            print("Нажмите <Esc> для выхода в главное меню или <Enter> для продолжения")
            key = ord(getch())
            s = key
            if key == 27:
                break
            os.system('cls')
            title = input("Введите название книги: ")
            if title == '':
                while title == '':
                    print(
                        'Введено пустое поле\n Введите 1 чтобы попробовать еще раз или <Esc> если хотите выйти: ')
                    key = ord(getch())
                    if key == 49:
                        self.add_book()
                    elif key == 27:
                        return
            author = input("Введите автора книги: ")
            if author == '':
                while author == '':
                    print(
                        'Введено пустое поле\n Введите 1 чтобы попробовать еще раз или <Esc> если хотите выйти:')
                    key = ord(getch())
                    if key == 49:
                        author = input("Введите автора книги еще раз: ")
                    elif key == 27:
                        return
            try:
                year = int(input("Введите год издания книги:"))
                while year < 0 or year > int(datetime.date.today().year):
                    year = int(input("Попробуйте ввести год еще раз: "))
            except ValueError:
                print('Введите число! Чтобы повторить введите 1')
                key = ord(getch())
                if key == 49:
                    self.add_book()
            book = Book(title, year, author)
            print("Хотите добавить книгу\n %s? \n 1-Да, 2-Нет" % book)
            change_option = ord(getch())

            if change_option == 49 or change_option == 13:
                self.library.add(book=book)
                print('Книга добавлена')
            else:
                print('Книга не добавлена')

            print("Нажмите <Esc> для выхода")
            key = ord(getch())
            if key == 27:
                break

    def delete_book(self):
        os.system("cls")
        print("Нажмите <Esc> для выхода в главное меню или <Enter> для продолжения")
        key = ord(getch())
        if key == 27:
            return
        while True:
            os.system("cls")
            book_number = input("Введите номер книги для удаления:")
            book = self.library.get_at(book_number)
            if not book:
                print("Книга не найдена\n Повторить поиск - 1 \n Выйти - <Esc>")
                key = ord(getch())
                if key == 27:
                    return
                else:
                    self.delete_book()
            print("Действително удалить книгу %s? \n1-Да \n2-Нет" % book)
            change_option = ord(getch())
            if change_option == 49:
                self.library.remove_at(book_number)
                print("Книга %s была удалена" % book)
            print("Нажмите <Esc> для выхода")
            key = ord(getch())
            if key == 27:
                break
            else:
                print('Удалить еще одну книгу?')

    def count_books(self):
        books = self.library.get_all_books()
        books = len(books)
        book = str(books)
        if books > 10 and book == '11' or book == '12' or book == '13' or book == '14':
            n = 'книг'
        elif book[-1] == '1':
            n = 'книга'
        elif book[-1] == '2' or book[-1] == '3' or book[-1] == '4':
            n = 'книги'
        else:
            n = 'книг'
        print('Сейчас в библиотеке', books, n)

    def run(self):
        try:
            while True:
                os.system('cls')

                self.count_books()
                print(
                    'Выберете одну из команд:\n'
                    '1 - Вывести все книги\n'
                    '2 - Найти книгу\n'
                    '3 - Изменить книгу\n'
                    '4 - Удалить книгу\n'
                    '5 - Добавить книгу\n'
                    "<Esc>- для выхода\n"
                    ': ', end=''
                )
                key = ord(getch())
                if key == 27:
                    break
                elif key == 49:
                    self.print_all()
                elif key == 50:
                    self.find_books()
                elif key == 51:
                    self.update_book()
                elif key == 52:
                    self.delete_book()
                elif key == 53:
                    self.add_book()

            self.library.close()
        except PeeweeInternalError as px:
            print(str(px))
        os.system('cls')
        print("Конец программы")