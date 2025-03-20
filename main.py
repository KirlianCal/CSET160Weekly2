from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
app = Flask(__name__)

conn_str = 'mysql://root:cset155@localhost/boatdb'
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def default():
    return render_template('base.html')

@app.route('/search', methods = ['POST', 'GET'])
def search():
    result = None
    if request.method == 'POST':
        boat_id = request.form['id']
        try:
            result = conn.execute(text('select * from boats where id = :id'), {'id': boat_id}).all()
            if not result:
                return render_template('search.html', result=None)
        except:
            return render_template('search.html', result=None)
    return render_template('search.html', result = result)

@app.route('/delete', methods = ['POST', 'GET'])
def delete():
    msg = None
    if request.method == 'POST':
        boat_id = request.form['id']
        try:
            result = conn.execute(text('select * from boats where id = :id'), {'id': boat_id}).all()
            if result:
                conn.execute(text('delete from boats where id = :id'), {'id': boat_id})
                conn.commit()
                msg = f'Boat at ID {boat_id} deleted'
        except:
            msg = f'Boat at ID {boat_id} not found'
    return render_template('delete.html', msg = msg)

@app.route('/update', methods = ['POST', 'GET'])
def update():
    msg = None
    if request.method == 'POST':
        boat_id = request.form['id']
        name = request.form['name']
        type = request.form['type']
        owner_id = request.form['owner_id']
        rental_price = request.form['rental_price']
        try:
            result = conn.execute(text('select * from boats where id = :id'), {'id': boat_id}).all()
            if result:
                conn.execute(text('update boats set name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price WHERE id = :id'), {'id': boat_id, 'name': name, 'type': type, 'owner_id': owner_id, 'rental_price': rental_price})
                conn.commit()
                msg = f'Boat at ID {boat_id} updated'
            else:
                msg = f'Boat at ID {boat_id} not found'
        except:
            msg = f'Boat at ID {boat_id} not found'
    return render_template('update.html', msg = msg)


if __name__ == '__main__':
    app.run(debug=True)