from flask import Flask, request, render_template, send_file
from modules import *
from modules.xls import create_xls
from modules.pdf import create_pdf
import os


app = Flask(__name__)

MAIN_ROUTE = '<a href="/">wróć do strony głównej</a>'
height = 0
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@app.route("/", methods=["GET"])
def main():
    if request.method == 'GET':
        return render_template('main_child.html')


@app.route("/add-expenses", methods=('GET', 'POST'))
def add_ex():
    if request.method == 'GET':
        (cnx, cursor) = create_connection()

        sql = "SELECT id, name FROM categories;"
        cursor.execute(sql)

        category_names = cursor.fetchall()

        return render_template('add-expenses.html', category_names=category_names)

    else:
        (cnx, cursor) = create_connection()

        sql = f"""INSERT INTO expenses
                (category_id, name, expense, date)
                VALUES(
                    {request.form['category']},
                    '{request.form['name']}',
                    {request.form['expense']},
                    '{request.form['date']}'
                );"""
        cursor.execute(sql)

        close_connection(cnx, cursor)

        return f"<p>Dodano wydatek</p><p>{MAIN_ROUTE}</p>"


@app.route("/get-expenses", methods=["GET"])
def get_ex():
    if request.method == 'GET':
        (cnx, cursor) = create_connection()

        sql = """SELECT expenses.id, 
                        expenses.name, 
                        expenses.expense,
                        expenses.date,
                        categories.name
                FROM expenses 
                LEFT JOIN categories 
                ON expenses.category_id=categories.id;"""
        cursor.execute(sql)

        expenses = cursor.fetchall()

        close_connection(cnx, cursor)

        height = (33 * (len(expenses) + 1)) + 101

        create_xls(expenses)

        os.rename(f'{BASE_DIR}/expenses.xlsx', f'{BASE_DIR}/download/expenses.xlsx')

        create_pdf(expenses)

        os.rename(f'{BASE_DIR}/expenses.pdf', f'{BASE_DIR}/download/expenses.pdf')

        return render_template('get-expenses.html', expenses=expenses, height=height)


@app.route("/delete-expense/<expense_id>", methods=["GET"])
def del_ex(expense_id):
    if request.method == 'GET':
        (cnx, cursor) = create_connection()

        sql = f"DELETE FROM expenses WHERE id={expense_id}"
        cursor.execute(sql)

        close_connection(cnx, cursor)

        return f'<p>Usunięto</p><p>{MAIN_ROUTE}</p>'


@app.route("/get-xls", methods=["GET"])
def xls():
    if request.method == 'GET':

        try:
            return send_file(f'{BASE_DIR}/download/expenses.xlsx',
                             attachment_filename='expenses.xlsx')
        except Exception as e:
            return str(e)


@app.route("/get-pdf", methods=["GET"])
def pdf():
    if request.method == 'GET':

        try:
            return send_file(f'{BASE_DIR}/download/expenses.pdf',
                             attachment_filename='expenses.pdf')
        except Exception as e:
            return str(e)