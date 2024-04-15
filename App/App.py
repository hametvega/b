#los templates son las vistas o pestañas de

from flask import Flask,render_template,request,redirect,url_for,flash,session
#para importar las cosas de una libreria
import mysql.connector #importamos el SQL
import base64
from werkzeug.security import generate_password_hash, check_password_hash
# import bcrypt
app=Flask(__name__)
app.secret_key='12346'
#configurar conexción
db = mysql.connector.connect(
    host="localhost", #valor por default
    user="root",
    password="",
    database="Canciones"
)

cursor =db.cursor() #es la connxión 

#Crear una instancia de la clase flsk

#encriptar contraseña  Y generar un hash de la contraseña
@app.route('/password/<contraencrip>')
def Encriptar(contraencrip):
    # encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'), bcrypt.gensalt());
    encriptar = generate_password_hash(contraencrip)
    valor = check_password_hash(encriptar,contraencrip)
    return "Encriptado:{0}| coincide:{1}".format(encriptar,valor)

                        #login
@app.route('/Login', methods =['GET','POST'])
def login():
    #verificar las credenciales
    if request.method=='POST':
        Username_login= request.form.get('name_usuario')
        passworld_login= request.form.get('contrasena_log')

        cursor = db.cursor()  # Llamar al método cursor() para crear una nueva instancia
        Query="SELECT Nombre_usuario, contraseña FROM personasp WHERE Nombre_usuario = %s"  # Agregar un espacio antes de WHERE
        cursor.execute(Query, (Username_login,))
        Username = cursor.fetchone()

        print(Username)
        if Username is not None:
            Password_Uncripted = check_password_hash(Username[1], passworld_login) 
            print(Password_Uncripted)

            if Password_Uncripted:
                session['User'] = Username_login
                session['Type_User'] = Username[2]
                if Username[2] == 'Administrador':
                    return redirect(url_for('Lista'))
                else:
                    return redirect(url_for('Lista_songs'))
            else:
                print("La contraseña ingresada es incorrecta. ")
                Error = 'Credenciales invalidas. intentaro nuevamente'
                return render_template('Login.html')
        else:
            print("El usuario no existe. ")
            Error = 'Credenciales invalidas. intentaro nuevamente'
            return render_template('Login.html')

    return render_template('Login.html', Error = Error)
# @app.route('/Login', methods =['GET','POST'])
# def login():
#             #verificar las credenciales
#     if request.method=='POST':
#         Username_login= request.form.get('name_usuario')
#         passworld_login= request.form.get('contrasena_log')

#         cursor = db.cursor  
#         Query="SELECT Nombre_usuario, contraseña FROM personasp wher Nombre_usuario = %s"
#         cursor.execute(Query, (Username_login))
#         Username = cursor.fetchone()
#         #usuarios= cursor.fetchone()# el fetch one es para una sola vlaidación
        
#         print(Username)
#         Password_Uncripted = check_password_hash(Username[1], passworld_login) 
#         print(Password_Uncripted)
        
#         if Username is not None and check_password_hash(Username[1], passworld_login):
            
#             session['User'] = Username_login
#             session['Type_User'] = Username[2]
#             if Username[2] == 'Administrador':
#                 return redirect(url_for('Lista'))
#             else:
#                 return redirect(url_for('Lista_songs'))
#         else:
#             print("Las canciones ingresadas son invalidas. ")
#             Error = 'Credenciales invalidas. intentaro nuevamente'
#             return render_template('Login.html')

#     return render_template('Login.html', Error = Error)
                        #lista


@app.route('/Logout')
def logout():
    #eliminar el usuario
    session.pop('Usuario',None)
    
    print("la sesión se cerro")

#Definir rutas
@app.route('/')
def Lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personasp')
    usuarios = cursor.fetchall() #Busca los datos en la tabla
    return render_template('Lista.html', Canciones = usuarios)
    

#@app.route <-Esto sirve para crear una ruta nueva
@app.route('/Saludo')  #lo de adentro de los parentesis es la dirección de la web
def Saludo():
    return"Creando rutas al proyecto"

@app.route('/Registrar', methods=['GET','POST']) #enviar info por medio de la url
def Registrar_usuario():

    if request.method == "POST":
        Nombres =request.form.get('name')
        Apellidos= request.form.get('apellido')
        usuario = request.form.get('usuario')
        correo = request.form.get('correo')
        Celular = request.form.get('celular')
        dirección= request.form.get('direccion')
        contraseña= request.form.get('contrasena')
        contraencriptada = generate_password_hash(contraseña)
    #insertar datos en la tabla
        cursor.execute("INSERT INTO personasp (Nombre_persona, Apellido_persona, Nombre_usuario, correo, celular, dirección, contraseña) VALUES(%s, %s, %s, %s, %s, %s, %s)",(Nombres, Apellidos, usuario, correo, Celular, dirección, contraseña))
        db.commit()
        flash("Usuario creado correctamente","success") #generar mensages
        
    #redirige a la misma pagina si el metodo es post
    
        return redirect(url_for('Registrar_usuario')) #se llama la función 
    
    #si el motodo es get me renderiza al formulario
    
    return render_template("Registrar.html")

#Se ejecuta la app o el servidor
@app.route('/Editar/<int:id>' ,methods = ['GET','POST'])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombre_p = request.form.get('Nombre_persona')
        apellido_p = request.form.get('Apellido_persona')
        email_p = request.form.get('Email')
        direccion_p = request.form.get('Dirección')
        telefono_p = request.form.get('Telefono')
        contraseña_p = request.form.get('contraseña_persona')

    #sentencia para actualizar los datos
        sql = "UPDATE personasp set Nombre_persona=%s,Apellido_persona=%s,correo=%s,celular=%s,dirección=%s,contraseña=%s where id_persona=%s"
        cursor.execute(sql,(nombre_p,apellido_p,email_p,telefono_p,direccion_p,contraseña_p,id ))
        db.commit()

        return redirect(url_for('Lista'))
    else:
        #obtener los datos de la persona que va a editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personasp WHERE id_persona = %s', (id,))
        data = cursor.fetchall()
    return render_template('Editar.html', personasp=data[0])
    
    


#canciónnnn


@app.route('/Registrar_canción', methods=['POST','GET']) #enviar info por medio de la url
def Registrar_song():

    if request.method == 'POST':
        Titulo =request.form.get('titulo')
        Artista= request.form.get('artista')
        Genero = request.form.get('genero')
        Precio = request.form.get('precio')
        Fecha = request.form.get('fecha')
        Portada= request.files['portada'] #imagen obtenida del registro        
        portadacover= Portada.read()
        
        

        
    #insertar datos en la tablas
        cursor.execute("INSERT INTO canciones (Titulo_song, Nombre_artist, Genero_song, Precio, Fecha_lanza, Img) VALUES(%s, %s, %s, %s, %s, %s)",(Titulo, Artista, Genero, Precio, Fecha, portadacover))
        db.commit()
        # flash("Canción agregada con exito","success") #generar mensages
        
        
    #redirige a la misma pagina si el metodo es post
    
    return render_template('Registrar_cancion.html')#se llama la función 
    
    #si el motodo es get me renderiza al formulario
        #canciónnnn

@app.route('/canciones')
def Lista_songs():
    cursor = db.cursor()
    cursor.execute('SELECT id_cancion, Titulo_song, Nombre_artist, Genero_song, Fecha_lanza, Img, Precio FROM canciones')
    canciones = cursor.fetchall() #Busca los datos en la tabla
    if canciones:
        listacanciones = []
        for cancion in canciones:
            
            imagen = base64.b64encode(cancion[5]).decode('utf-8')
            listacanciones.append({
                "hamet" : cancion[0],
                "titulo": cancion[1],  
                "artista": cancion[2],
                "genero": cancion[3],
                "Fecha" : cancion[4],
                "precio" : cancion[6],
                "img": imagen
                })
    return render_template('Lista_canciones.html', canciones=listacanciones)
    # return redirect(url_for('Lista_songs', Canciones = users))

    
    
    #canciónnnn
    
    
@app.route('/Editar_cancion/<int:id>' ,methods = ['GET','POST'])
def editar_song(id):
    cursor = db.cursor()
    if request.method == 'POST':
        Titulo = request.form.get('titulo')
        Artista = request.form.get('artista')
        Duración = request.form.get('duracion')
        Fecha = request.form.get('fecha')
        Portada = request.form.get('portada')
        Genero = request.form.get('genero')

    #sentencia para actualizar los datos
        sql = "UPDATE Canciones set Titulo_song=%s,Nombre_artist=%s,Precio=%s,Fecha_lanza=%s,img=%s,Genero_song=%s where id_cancion=%s"
        cursor.execute(sql,(Titulo,Artista,Duración,Portada,Fecha,Genero,id ))
        db.commit()

        return redirect(url_for('Lista_songs'))
    else:
        #obtener los datos de la persona que va a editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM canciones WHERE id_cancion = %s', (id,))
        data = cursor.fetchall()

        return render_template('Editar_canción.html', Canciones=data[0])
    
@app.route('/eliminar_cancion/<int:id>', methods=['GET'])
def eliminar_song(id):
    if request.method == 'POST' or request.method == 'GET':
        cursor.execute('delete FROM Canciones WHERE id_cancion = %s', (id,))
        db.commit()
        return redirect(url_for('Lista_songs'))

        
@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    if request.method == 'POST' or request.method == 'GET':
        cursor.execute('delete FROM personasp WHERE id_persona = %s', (id,))
        db.commit()
        return redirect(url_for('Lista'))
    
    
    
#Canciones 
#Verificar credenciales
        
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    app.add_url_rule('/', view_func=Lista)
    app.    run(debug=True,port=5005)



