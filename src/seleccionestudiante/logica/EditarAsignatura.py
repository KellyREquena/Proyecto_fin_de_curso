import sys
import os

from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic
from tkinter import messagebox

from src.proyectofindecurso.modelo.Asignatura import Asignatura
from src.proyectofindecurso.modelo.declarative_base import engine, Base, session

from datetime import datetime
from src.proyectofindecurso.modelo.Asignatura import Asignatura
from src.proyectofindecurso.modelo.Estudiante import Estudiante
from src.proyectofindecurso.modelo.Equipo import Equipo
from src.proyectofindecurso.modelo.Actividad import Actividad
from src.proyectofindecurso.logica.GestionAsignatura import GestionAsignatura
from src.proyectofindecurso.modelo.declarative_base import Session

class Dialogo (QDialog):
    def __init__(self):
        Base.metadata.create_all (engine)
        self.session = Session ()
        ruta = os.path.dirname (os.path.abspath (__file__)) + r"\..\vista\EditarAsignatura.ui"
        QDialog.__init__ (self)
        uic.loadUi (ruta, self)

        self.pbGuardar.clicked.connect (self.guardar)
        self.pbCancelar.clicked.connect (self.cerrar)

        self.estudiante1 = Estudiante (apellidoPaterno="Ramos", apellidoMaterno="Ortega", nombres="Juan Carlos",
                                       elegible=True)
        self.estudiante2 = Estudiante (apellidoPaterno="Solis", apellidoMaterno="Matos", nombres="Pedro",
                                       elegible=True)
        self.estudiante3 = Estudiante (apellidoPaterno="Paredes", apellidoMaterno="Torres", nombres="Luis Alberto",
                                       elegible=True)
        self.estudiante4 = Estudiante (apellidoPaterno="Garcia", apellidoMaterno="Mateo", nombres="Miguel Angel",
                                       elegible=True)

        self.session.add (self.estudiante1)
        self.session.add (self.estudiante2)
        self.session.add (self.estudiante3)
        self.session.add (self.estudiante4)
        self.session.commit ()

        # crear asignatura
        self.asignatura1 = Asignatura (nombreAsignatura="Análisis y diseño de sistemas")
        self.asignatura2 = Asignatura (nombreAsignatura="Pruebas de software")
        self.session.add (self.asignatura1)
        self.session.add (self.asignatura2)
        self.session.commit ()

        # crear equipo de trabajo
        self.equipo1 = Equipo (denominacionEquipo="Equipo01")
        self.equipo2 = Equipo (denominacionEquipo="Equipo02")
        self.session.add (self.equipo1)
        self.session.add (self.equipo2)
        self.session.commit ()

        # crear actividad
        self.actividad1 = Actividad (denominacionActividad="Prueba unitaria",
                                     fecha=datetime (2021, 9, 28, 00, 00, 00, 00000))
        self.actividad2 = Actividad (denominacionActividad="TDD", fecha=datetime (2021, 9, 25, 00, 00, 00, 00000))
        self.actividad3 = Actividad (denominacionActividad="BDD", fecha=datetime (2021, 10, 15, 00, 00, 00, 00000))
        self.session.add (self.actividad1)
        self.session.add (self.actividad2)
        self.session.add (self.actividad3)
        self.session.commit ()

        # Relacionar Asignatura con estudiantes
        self.asignatura1.estudiantes = [self.estudiante1, self.estudiante4]
        self.asignatura2.estudiantes = [self.estudiante2, self.estudiante3]
        self.session.commit ()

        # Relacionar equipo con estudiantes
        self.equipo1.estudiantes = [self.estudiante1, self.estudiante3]
        self.equipo2.estudiantes = [self.estudiante2, self.estudiante4]
        self.session.commit ()

        # Relacionar Equipo de trabajo con actividad
        self.equipo1.actividades = [self.actividad1, self.actividad2]
        self.equipo2.actividades = [self.actividad3]
        self.session.commit ()

        self.session.close ()

    def guardar(self):
        txtIDAsignatura=int(self.ltIDAsignatura.text())
        txtNombreAsignatura=str(self.ltNombreAsignatura.text())

        if len (txtNombreAsignatura) == 0:
            messagebox.showinfo("Alerta","Falta ingresar su nombre de la asignatura")
        else:
            busqueda = session.query (Asignatura).filter (Asignatura.nombreAsignatura == txtNombreAsignatura).all ()
            if len (busqueda) == 0:
                asignatura = session.query (Asignatura).filter (Asignatura.idAsignatura == txtIDAsignatura).first ()
                asignatura.nombreAsignatura = txtNombreAsignatura
                session.commit ()
                messagebox.showinfo ("Alerta","Se registraton los datos")
            else:
                messagebox.showinfo("Alerta","Existe el nombre de asignatura")


    def cerrar(self):
        resultado = messagebox.askquestion ("Salir", "¿Está seguro que desea salir?")
        if resultado == "yes":
            self.session = Session ()

            estudiantes = self.session.query (Estudiante).all ()
            for estudiante in estudiantes:
                self.session.delete (estudiante)
            self.session.commit ()
            self.session.close ()

            asignaturas = self.session.query (Asignatura).all ()
            for asignatura in asignaturas:
                self.session.delete (asignatura)
            self.session.commit ()
            self.session.close ()

            actividades = self.session.query (Actividad).all ()
            for actividad in actividades:
                self.session.delete (actividad)
            self.session.commit ()
            self.session.close ()

            equipos = self.session.query (Equipo).all ()
            for equipo in equipos:
                self.session.delete (equipo)
            self.session.commit ()
            self.session.close ()
            # exit(0)
            quit (0)

if __name__ == '__main__':
    app = QApplication (sys.argv)
    dialogo = Dialogo ()
    dialogo.show ()
    app.exec ()