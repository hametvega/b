create database Canciones;
use Canciones;

CREATE TABLE personasp(
  id_persona INT NOT NULL auto_increment primary key,
  Nombre_persona VARCHAR(45) NOT null,
  Apellido_persona VARCHAR(45) NOT NULL,
  Nombre_usuario VARCHAR(45) NOT NULL,
  correo VARCHAR(45) NOT NULL,
  celular VARCHAR(45) NOT NULL,
  dirección VARCHAR(45) NOT NULL,
  contraseña varchar (255) not null
  );

  describe personasp;
  select * from personasp;
  
				/*Canciones*/
                
create table Canciones( 
	id_cancion int auto_increment primary key ,
    Titulo_song varchar(25) not null,
    Nombre_artist varchar(25) not null,
    Genero_song varchar (25) not null,
    Precio float (10) not null,
    Fecha_lanza date not null,
	Img blob,
    Rol varchar (45) not null
    );
    select * from Canciones;

drop table Canciones;

create table Compras (
	id_compra int not null primary key ,
    fecha_compra  varchar(50) not null,
    Precio_compra varchar(50) not null,
    Personas_id int not null,
    Canciones_id int not null,
    foreign key (Personas_id) references personasp (id_persona),
    foreign key (Canciones_id) references Canciones(id_cancion)
    );
    select * from Compras;



