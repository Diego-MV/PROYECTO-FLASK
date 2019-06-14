from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']    ='localhost'
app.config['MYSQL_USER']    ='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']      ='biblioteca'
app.config['MYSQL_PORT']    =3306

app.secret_key = 'diego'

mysql=MySQL(app)
@app.route('/')
def home():
	return render_template('home.html')
####################################################################################################################
@app.route('/add_autor')
def add_autor():
	return render_template('add_autor.html')
@app.route('/add_autorpost', methods = ['POST'])
def add_autorpost():
	if request.method == 'POST':
		nombre       = request.form['nombre']
		nacionalidad = request.form['nacionalidad']
		if nombre != '' and nacionalidad !='':
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Autor (Nombre,Nacionalidad) VALUES(%s,%s)",(nombre,nacionalidad))
			mysql.connection.commit()
			flash('Autor Agregado Correctamente')
			return redirect(url_for('add_autor'))
		else:
			return redirect(url_for('add_autor'))
@app.route('/autores')
def autores():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Autor')
	data = cur.fetchall()
	return render_template('list_autor.html', contacts = data)
@app.route('/deleteautor/<string:id>')
def deleteautor(id):
	cur = mysql.connection.cursor()
	cur.execute('DELETE FROM Autor WHERE Id_Autor= {0}'.format(id))
	mysql.connection.commit()
	flash('Autor Eliminado')
	return redirect(url_for('autores'))
@app.route('/editautor/<id>')
def edit_autor(id):
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Autor WHERE Id_Autor={0}'.format(id))
	data = cur.fetchall()
	return render_template('edit_autor.html',autor=data[0])
@app.route('/updateautor/<id>', methods=['POST'])
def update_autor(id):
	if request.method == 'POST':
		nombre       = request.form['nombre']
		nacionalidad = request.form['nacionalidad']
		cur=mysql.connection.cursor()
		cur.execute('UPDATE Autor SET Nombre=%s, Nacionalidad=%s WHERE Id_Autor=%s',(nombre,nacionalidad,id))
		mysql.connection.commit()
		flash('Autor Editado')
		return redirect(url_for('autores'))
################################################################################################################################################
@app.route('/registrar_usuario')
def registrar_usuarioget():
	return render_template('add_user.html')

@app.route('/registrar_usuariopost', methods=['POST'])
def registrar_usuario():
	if request.method == 'POST':
		nombre       = request.form['nombre']
		telefono     = request.form['telefono']
		mail         = request.form['mail']
		contrasena   = request.form['contrasenna']
		if nombre != '' and telefono !='' and mail!='' and contrasena!='':
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Usuario (Nombre,Telefono,Mail,Contraseña) VALUES(%s,%s,%s,%s)",(nombre,telefono,mail,contrasena))
			mysql.connection.commit()
			flash('Usuario Registrado Correctamente')
			return redirect(url_for('home'))
		else:
			return redirect(url_for('registrar_usuario'))
###############################################################################################################################################3
@app.route('/editoriales')
def editoriales():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Editorial')
	data = cur.fetchall()
	return render_template('list_editorial.html', editorials = data)
@app.route('/add_editorial')
def add_editorial():
	return render_template('add_editorial.html')
@app.route('/add_editorialpost', methods = ['POST'])
def add_editorialpost():
	if request.method == 'POST':
		nombre = request.form['nombreedit']
		
		
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Editorial (Nombre) VALUES(%s)",(nombre))
		mysql.connection.commit()
		flash('Editorial Agregada Correctamente')
		return redirect(url_for('add_editorial'))
	else:
		return redirect(url_for('add_editorial'))

if __name__=='__main__':
	app.run(port=3000,debug=True)