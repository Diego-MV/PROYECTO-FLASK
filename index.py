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
		name = request.form['nombreedit']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO editorial (Nombre)VALUES ('%s')"%(name) )
		mysql.connection.commit()
		flash('Editorial Agregada Correctamente')
		return redirect(url_for('add_editorial'))

#######################################################################################
@app.route('/categorias')
def categorias():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Categoria')
	data = cur.fetchall()
	return render_template('list_categoria.html', categorias = data)
@app.route('/add_categoria')
def add_categoria():
	return render_template('add_categoria.html')
@app.route('/add_categoriapost', methods = ['POST'])
def add_categoriapost():
	if request.method == 'POST':
		name = request.form['nombreedit']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO categoria (Nombre)VALUES ('%s')"%(name) )
		mysql.connection.commit()
		flash('Categoria Creada Correctamente')
		return redirect(url_for('add_categoria'))
@app.route('/delete_categoria/<string:id>')
def delete_categoria(id):
	cur = mysql.connection.cursor()
	cur.execute('DELETE FROM Categoria WHERE Id_Categoria= {0}'.format(id))
	mysql.connection.commit()
	flash('Categoria Eliminada')
	return redirect(url_for('categorias'))
#######################################################################################################################
@app.route('/libros')
def libros():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Libro')
	data = cur.fetchall()
	return render_template('list_libros.html', libros = data)
@app.route('/add_libro')
def add_libro():
	return render_template('add_libro.html')
@app.route('/add_libropost', methods = ['POST'])
def add_libropost():
	if request.method == 'POST':
		nombre = request.form['nombre']
		ejemplares = request.form['ejemplares']
		editorial = request.form['editorial']
		autor = request.form['autor']
		resumem=request.form['resumen']
		NumPaginas=request.form['numpag']

		cur = mysql.connection.cursor()
		
		cur.execute('select Id_Editorial from editorial where Nombre=%s'%(editorial))
		mysql.connection.commit()
		edit=cur.fetchall()
		cur.execute('SELECT Id_Autor FROM autor WHERE Nombre=`%s`'%(autor))
		mysql.connection.commit()
		aut=cur.fetchall()
		
		
		cur.execute("INSERT INTO libro (Nombre,FechaLanz,NumPaginas,Ejemplares,Id_Editorial,Id_Autor)VALUES ('%s')"%(nombre, resumem,NumPaginas ,ejemplares, edit, aut) )
		mysql.connection.commit()
		flash('Categoria Creada Correctamente')
		return redirect(url_for('add_categoria'))
if __name__=='__main__':
	app.run(port=5000,debug=True)