# Generate_expenses

Simple website to manage personal expenses, avaibles to download PDF or exel file with data.
- Used tools and technologies: Python, Flask, psycopg2, reportlab, XlsxWriter

To run project:
1. cd to the directory of repository.
2. activate your virtualenv.
3. run: `pip install -r requirements.txt` in your shell.
4. run: `python3 sync_db.py`.
5. run: `python3 main.py`.

It should set up the server on your localhost. If it doesn't, or you want to be on specified host navigate to `/modules/__init__.py` and modify connect values.
