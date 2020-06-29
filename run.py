import argparse
from project import create_app, wait_for_db, db


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--init_db', help='Creates tables in db', action='store_true')
parser.add_argument(
    '-w', '--wait_for_db', help="Waits for db to ensue it's running", action='store_true'
)
args = parser.parse_args()

app = create_app()

if __name__ == '__main__':
    if args.wait_for_db:
        wait_for_db()
    if args.init_db:
        db.create_all(app=app)
    app.run(host='0.0.0.0')
