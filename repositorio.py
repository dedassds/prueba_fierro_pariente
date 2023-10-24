from datetime import date, timedelta

import os
import sys
import subprocess
import git
import difflib
import shutil
import requests
import json

from PIL import Image, ImageTk


from PyQt5.QtWidgets import ( QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QPlainTextEdit, QDialog,
 QFileDialog, QMessageBox, QInputDialog, QGridLayout, QSplitter, QTreeView, QFileSystemModel, QHBoxLayout,
 QApplication, QMainWindow, QTableWidget, QTableWidgetItem)

from PyQt5.QtWidgets import QComboBox, QMenuBar, QMenu, QAction

from PyQt5.QtCore import Qt

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from ldap3 import Server, Connection, ALL, SUBTREE
from PyQt5.QtWidgets import QComboBox
from datetime import datetime
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QTextCursor, QTextCharFormat
from pathlib import Path
from difflib import unified_diff
from difflib import Differ



#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler
from configparser_crypt import ConfigParserCrypt
import configparser

#-----revisar librerias----------------

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# Variable de bandera para el inicio de sesión exitoso
login_successful = False

import requests

class GitHubOrganizations:
    def __init__(self, github_manager):
        self.github_manager = github_manager

    def get_organizations(self):
        url = f"{self.github_manager.base_url}/user/orgs"

        response = requests.get(url, headers=self.github_manager.headers)
        organizations = response.json()

        return organizations

    def switch_organization(self, organization):
        url = f"{self.github_manager.base_url}/user/memberships/orgs/{organization}"

        response = requests.patch(url, headers=self.github_manager.headers)
        if response.status_code == 200:
            print(f"Switched to organization: {organization}")
        else:
            print(f"Failed to switch to organization: {organization}")

class ProjectInfoManager:
    def __init__(self, json_path='project_info.json', directory_path='.'):
        self.json_path = json_path
        self.directory_path = directory_path
        self.data = {
            'site': 'B_29',
            'proyecto': 'Cisco',
            'Equipo': 'ICT',
            'BU': [],
            'Modelo': {}
        }
        self.initialize_json()

    def initialize_json(self):
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w') as f:
                json.dump([self.data], f, indent=4)

    def update_BU_and_Modelo(self):
        # Inicializar la lista que contendrá todos los diccionarios
        all_data = []

        # Obtener nombres de todas las carpetas (BU)
        bu_folders = [name for name in os.listdir(self.directory_path) if os.path.isdir(os.path.join(self.directory_path, name))]

        for bu in bu_folders:
            # Ruta a la carpeta BU
            bu_path = os.path.join(self.directory_path, bu)

            # Obtener nombres de todas las subcarpetas o archivos dentro del BU (Modelo)
            model_folders = [name for name in os.listdir(bu_path) if os.path.isdir(os.path.join(bu_path, name))]

            for model in model_folders:
                # Diccionario para cada BU y Modelo
                data = {
                    "site": "B_29",
                    "proyecto": "Cisco",
                    "Equipo": "ICT",
                    "BU": [bu],
                    "Modelo": {bu: [model]}
                }

                # Añadir este diccionario a la lista de todos los datos
                all_data.append(data)

        # Leer el archivo JSON existente
        try:
            with open(self.json_path, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        # Comparar all_data con existing_data
        if all_data != existing_data:
            # Si son diferentes, escribir all_data en el archivo JSON
            with open(self.json_path, 'w') as f:
                json.dump(all_data, f, indent=4)

    def write_to_json(self):
        with open(self.json_path, 'w') as f:
            json.dump([self.data], f, indent=4)


class HistorialManager:
    def __init__(self, file_path="C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\historial json\\historial.json"):
        self.file_path = file_path
        self.data_top = [["Ensamble", "Familia", "Cambios"]]
        self.inicializar_historial()
        
    def inicializar_historial(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def registrar_cambios_de_todos_los_repositorios(self,ruta_corregida_directory):

        
        #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"
        base_path = ruta_corregida_directory
        self.new_data = []  # Inicializamos una lista para guardar todos los nuevos datos
        
        for repo_name in os.listdir(base_path):
            self.repo_path = os.path.join(base_path, repo_name)
            if os.path.isdir(self.repo_path):
                # Aquí supongo que registrar_cambios() actualiza new_data con los cambios
                self.registrar_cambios(repo_name) 
                
        # Leer el archivo JSON existente
        existing_data = self.leer_historial()

        # Comparar new_data con existing_data
        if self.new_data != existing_data:
            # Si son diferentes, actualizar el archivo JSON
            self.escribir_historial(self.new_data)

    
    def leer_historial(self):
        """Lee el archivo JSON y devuelve la lista de cambios."""
        if not os.path.exists(self.file_path):
            return []
        
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return data

    def escribir_historial(self, data):
        """Escribe la lista de cambios al archivo JSON."""
        print(f"Escribiendo datos al archivo {self.file_path}: {data}")  # Agregar esta línea
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def obtener_repositorios(self, ruta_corregida_directory,selected_org):
        ruta_organizacion = os.path.join(ruta_corregida_directory,selected_org)
        if os.path.isdir(ruta_organizacion):
            return [nombre for nombre in os.listdir(ruta_organizacion) if os.path.isdir(os.path.join(ruta_organizacion, nombre))]
        else:
            return []

    def registrar_cambios(self, organizacion):
        repositorios = self.obtener_repositorios(self.repo_path, organizacion)
        for repo_name in repositorios:
            repo_path = os.path.join(self.repo_path, organizacion, repo_name)
            os.chdir(repo_path)
            output = subprocess.getoutput('git log --name-status')
            
            for line in output.split('\n'):
                if '\t' in line:
                    status, file_path = line.split('\t', 1)
                
                    if status == 'M':
                        ensamble = self.get_ensamble(file_path)
                        archivo = self.get_file_name(file_path)
                        familia = self.get_familia(repo_path)
                        version = self.get_version(file_path, repo_path)
                        responsable = self.get_responsable()
                        cambios = self.get_cambios()
                        
                        # Verificar si el ensamble ya existe en new_data
                        ensamble_existente = next((item for item in self.new_data if item["ensamble"] == ensamble and item["familia"] == familia), None)
                        
                        if ensamble_existente is None:
                            cambio = self.agregar_cambio(ensamble, archivo, familia, version, responsable, cambios)
                            self.new_data.append(cambio)

            
    def agregar_cambio(self, ensamble, archivo, familia, version, responsable, cambios):
        """Agrega o actualiza un cambio en el historial."""
        historial = self.leer_historial()

        # Buscar si el ensamble ya existe en el historial
        ensamble_existente = next((item for item in historial if item["ensamble"] == ensamble and item["familia"] == familia), None)
        
        if ensamble_existente is not None:
            # Si el ensamble ya existe, actualiza el registro
            print(f"Actualizando cambio existente para el ensamble: {ensamble}, familia: {familia}")
            ensamble_existente["cambios"] = cambios  # Asigna el nuevo valor
            cambio = ensamble_existente  # Para que la función devuelva el cambio actualizado
        else:
            # Si el ensamble no existe, crea un nuevo registro
            print(f"Agregando nuevo cambio: {ensamble}, {archivo}, {familia}, {version}, {responsable}, {cambios}")
            cambio = {
                "ensamble": ensamble,
                "familia": familia,
                "cambios": cambios  # Asigna el nuevo valor
            }
            historial.append(cambio)
        
        self.escribir_historial(historial)
        return cambio



    def determinar_version(self, ensamble, archivo):
        historial = self.leer_historial()
        
        cambios = [c for c in historial if c["ensamble"] == ensamble and c["archivo"] == archivo]
        
        if not cambios:
            return "1.0.0"
        
        ultima_version = cambios[-1]["version"]
        mayor, medio, menor = map(int, ultima_version.split('.'))
        
        nueva_version = f"{mayor}.{medio}.{menor + 1}"
        
        return nueva_version

    def get_ensamble(self, file_path):
        return file_path.split('/')[0]


    def get_file_name(self,file_path):
        return os.path.basename(file_path)

    def get_familia(self, selected_repo):
        return os.path.basename(selected_repo)

    def get_version(self,file_path, repo_path):
        os.chdir(repo_path)
        commit_count = subprocess.getoutput(f'git log --oneline {file_path} | wc -l')
        return f'1.0.0.{commit_count}'

    def get_responsable(self):
        return None

    def get_cambios(self):
        return "Cambios realizados"

    def comprobar_cambios(self, existing_repositories, tabla):
        modified_files = []  # Esta lista deberá llenarse con los archivos modificados
        
        for file_path in modified_files:
            ensamble = self.get_ensamble(file_path)
            file_name = self.get_file_name(file_path)
            familia = self.get_familia(existing_repositories)
            #version = self.get_version(file_path, repo_path)
            responsable = self.get_responsable()
            cambios = self.get_cambios()
            
            self.data_top.append([ensamble, familia, cambios])
        
        self.actualizar_tabla(tabla)  # Pasar tabla como argumento

    def actualizar_tabla(self, tabla):
        historial = self.leer_historial()  # Leer los datos del historial.json
        self.data_top = [self.data_top[0]] + historial  # Mantener solo el primer elemento (encabezados) de data_top y añadir el historial

        tabla.setRowCount(len(self.data_top))  # Ahora cuenta todos los elementos, incluyendo los encabezados
        tabla.setColumnCount(len(self.data_top[0]))

        for i, row_data in enumerate(self.data_top):  # Ahora incluye los encabezados en el llenado de la tabla
            for j, column_data in enumerate(row_data.values() if isinstance(row_data, dict) else row_data):  # Si es un diccionario, usa .values()
                tabla.setItem(i, j, QTableWidgetItem(str(column_data)))
  

# Ejemplo de uso
#historial_manager = HistorialManager()
#historial_manager.agregar_cambio("Rama_A", "archivo1.txt", "Repo_X", "1.0.0", "Usuario1", "Archivo añadido")




class VisualizadorTabla(QMainWindow):
    def __init__(self,controlador):
        super().__init__()
        self.controlador = controlador
        self.iniciarUI()

    def iniciarUI(self):
        self.setWindowTitle('Comparacion de archivos')
        self.setGeometry(100, 100, 800, 600)

        #self.instance_with_method = GitViewer(QMainWindow)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        

         #------Primer terminal--------------------------------------
        #widgets para la imagen y el nombre del usuario
        self.usuario_Archivo = QLabel('Master')
        self.text_master = QPlainTextEdit( self )

        #layout = QVBoxLayout()
        #layout.addWidget(tabla)
        #central_widget.setLayout(layout)

        #Modificacion del ancho
        self.text_master.setMinimumWidth(100)
        self.text_master.setMaximumWidth(400)

        #Modificacion de la altura
        self.text_master.setMinimumHeight(300)
        self.text_master.setMaximumHeight(600)

        #Segunda terminal
        self.usuario_Archivo_2 = QLabel('Actual')
        self.text_Actual = QPlainTextEdit( self )

        #Modificacion del ancho
        self.text_Actual.setMinimumWidth(100)
        self.text_Actual.setMaximumWidth(400)

        #Modificacion de la altura
        self.text_Actual.setMinimumHeight(300)
        self.text_Actual.setMaximumHeight(600)

        #Organizacion por layout vertical
        verticalInnerLayout = QVBoxLayout()
        verticalInnerLayout.addWidget( self.usuario_Archivo)
        verticalInnerLayout.addWidget( self.text_master )

        verticalInnerLayout_2 = QVBoxLayout()
        verticalInnerLayout_2.addWidget( self.usuario_Archivo_2)
        verticalInnerLayout_2.addWidget( self.text_Actual )

        horizontalInnerLayout = QHBoxLayout()
        horizontalInnerLayout.addLayout( verticalInnerLayout )
        horizontalInnerLayout.addLayout( verticalInnerLayout_2 )       

        self.groupBox1 = QGroupBox( "Comparación" )
        self.groupBox1.setLayout( horizontalInnerLayout )

        #Boton para mostrar cambios en las terminales
        self.show_changes_button = QPushButton("Show Changes", self)       
        self.show_changes_button.clicked.connect(self.controlador.show_changes)
        
        self.show_changes_button.setGeometry(10, 420, 200, 40)

        # Botón para sincronizar archivos con la ruta1 (Master)
        self.sync_button = QPushButton("Sincronizar con Master")
        self.sync_button.clicked.connect(self.controlador.sync_files_with_master)

        verticalInnerLayout = QVBoxLayout()
        verticalInnerLayout.addWidget( self.show_changes_button )

        horizontalInnerLayout = QHBoxLayout()
        horizontalInnerLayout.addLayout( verticalInnerLayout )
        horizontalInnerLayout.addWidget( self.sync_button )
        

        self.groupBox2 = QGroupBox( "Filtros" )
        self.groupBox2.setLayout( horizontalInnerLayout )

        #Definir un groupbox en un layout para el central_widget
        main_layout = QVBoxLayout(central_widget)  # Crea un QVBoxLayout para central_widget
        main_layout.addWidget(self.groupBox1)  # Agrega groupBox1 al layout
        main_layout.addWidget(self.groupBox2)


class ConfigRead:
    """It creates an encrypted config file"""

    def __init__(self):
        """initialize ConfigRead class"""
        # Variable definition
        self.generic_path = Path(os.getcwd())
        self.complete_path_section = None
        self.value_from_file = None
        self.file_path = None
        self.AES_KEY = None

        # Class Initialization
        self.config = ConfigParserCrypt()
        self.file = "config.ini"
        self.is_file()

    def is_file(self):
        """it validates if config file exists"""
        self.file_path = Path(self.file)
        if self.file_path.is_file():
            self.read_file()
        else:
            self.create_sections()

    def read_file(self):
        """read the file using the encrypted key"""
        with open("DAT", "rb") as configfile:
            self.AES_KEY = next(configfile)
        self.config.aes_key = self.AES_KEY
        self.config.read_encrypted(self.file)

    def create_sections(self):
        """_summary_.
        """
        # Key Generation
        self.config.generate_key()
        self.AES_KEY = self.config.aes_key
        with open("DAT", "wb") as key:
            key.write(self.AES_KEY)

        # Section Creation
        self.config.add_section("PATHS")
        self.config.add_section("CONTROL")
        self.config.add_section("GITHUB")  # <-- Añadir sección GITHUB para el token

        # Keys Creation
        self.config["PATHS"] = {
            "MasterPath": self.generic_path,
            "LocalPath": self.generic_path,
            
        }
        self.config["SPECIAL_VALUES"] = {"SEND": "True", "NEWBORN": "True"}
        self.config["CONTROL"] = {'clean_enabler': False,'clean_counter': '10'}
        self.config["GITHUB"] = {'Token': ''}  # <-- Añadir clave Token en la sección GITHUB

        with open(self.file, "wb") as configfile:
            self.config.write_encrypted(configfile)

    def read_paths_section(self):
        """read complete PATHS section from config file"""
        self.complete_path_section = tuple(self.config.items("PATHS"))
        return self.complete_path_section

    def write_to_file(self, section, key, value):
        """write key to config file"""
        self.config[section][key] = value
        with open(self.file, "wb") as configfile:
            self.config.write_encrypted(configfile)

    def read_from_file(self, section, key):
        """read key from config file"""
        self.value_from_file = self.config[section][key]
        return self.value_from_file

    # Estos son los nuevos métodos que agregamos para manejar el token de GitHub:
    def set_token(self, token):
        """Set the GitHub token in the encrypted config file."""
        self.write_to_file('GITHUB', 'Token', token)

    def get_token(self):
        """Get the GitHub token from the encrypted config file."""
        return self.read_from_file('GITHUB', 'Token')

    

class GitHubManager:
    def __init__(self):

        config_manager = ConfigRead()
        self.token = config_manager.get_token()
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def create_repository(self, selected_org, repo_name, description="", private=False):
        org_url = f'{self.base_url}/orgs/{selected_org}/repos'
        data = {
            'name': repo_name,
            'description': description,
            'private': private
        }

        response = requests.post(org_url, headers=self.headers, json=data)

        if response.status_code == 201:
            return True, 'Repositorio creado con éxito.'
        else:
            return False, f'Error: {response.content}'

    def get_existing_repositories(self, selected_org):
        try:
            url = f"{self.base_url}/orgs/{selected_org}/repos"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            repos = response.json()

            return [repo['name'] for repo in repos]
        except requests.RequestException as e:
            print(f"Error al obtener los repositorios: {e}")
            return []
        
        
    
    def get_branches_of_repository(self, selected_org, repo_name):
        try:
            
            
            url = f"{self.base_url}/repos/{selected_org}/{repo_name}/branches"
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            branches = response.json()
            return [branch['name'] for branch in branches]
        except requests.RequestException as e:
            print(f"Error al obtener las ramas de {repo_name}: {e}")
            return []


    
    #funcionalidad de crear y empujar ramas directamente desde tu máquina local

    def create_and_push_initial_branch(self, selected_org, repo_path, branch_name):
        try:
            # Cambiar al directorio del repositorio
            os.chdir(repo_path)

            # Clonar el repositorio a la máquina local
            subprocess.check_call(['git', 'clone', self.base_url + selected_org + repo_path])

            # Cambiar al directorio del repositorio clonado
            os.chdir(repo_path)

            # Crear la nueva rama huérfana
            subprocess.check_call(['git', 'checkout', '--orphan', branch_name])

            # Limpiar la rama de sus archivos en espera
            subprocess.check_call(['git', 'reset'])
            subprocess.check_call(['git', 'clean', '-f', '-d'])

            # Hacer un commit inicial
            subprocess.check_call(['git', 'commit', '--allow-empty', '-m', f'Commit inicial en {branch_name}'])

            # Empujar la rama al remoto
            subprocess.check_call(['git', 'push', 'origin', branch_name])

            return True, 'Rama creada y empujada con éxito al nuevo repositorio.'
        except subprocess.CalledProcessError as e:
            return False, f'Error al ejecutar el comando: {e}'

    def push_new_branch_to_existing_repo(self, repo_name, branch_name, repo_path):
            
        try:
            print("Ruta al repositorio:", repo_path)
            os.chdir(repo_path)
            ...


            # Crear la nueva rama huérfana
            subprocess.check_call(['git', 'checkout', '--orphan', branch_name])

            # Limpiar la rama de sus archivos en espera
            subprocess.check_call(['git', 'reset'])
            subprocess.check_call(['git', 'clean', '-f', '-d'])

            # Hacer un commit inicial
            subprocess.check_call(['git', 'commit', '--allow-empty', '-m', f'Commit inicial en {branch_name}'])

            # Empujar la rama al remoto
            subprocess.check_call(['git', 'push', 'origin', branch_name])

            return True, 'Rama creada y empujada con éxito al repositorio existente.'
        except subprocess.CalledProcessError as e:
            return False, f'Error al ejecutar el comando: {e}'

    def clone_repository_to_local(self, org_name, repo_name, local_path):
        repo_url = f'https://github.com/{org_name}/{repo_name}.git'
        try:
            subprocess.check_call(['git', 'clone', repo_url, local_path])
            return True, 'Repositorio clonado con éxito en el sistema local.'
        except subprocess.CalledProcessError as e:
            return False, f'Error al clonar el repositorio: {e}'


    def create_and_push_branch(self, repo_name, branch_name):
        
        try:
            # Cambiar al directorio del repositorio
            os.chdir(f"C:/ruta/a/tus/repositorios/{repo_name}")

            # Crear la rama localmente
            subprocess.check_call(['git', 'checkout', '-b', branch_name])

            # Empujar la rama al remoto
            subprocess.check_call(['git', 'push', '-u', 'origin', branch_name])

            return True, 'Rama creada y empujada con éxito.'
        except subprocess.CalledProcessError as e:
            return False, f'Error al ejecutar el comando: {e}'
    
    #self.github_manager.upload_file_to_repo(self.selected_repo, self.branch_combo.currentText(), self.selected_file, repo_path)
    def upload_file_to_repo(self, repo_name, branch_name, file_path, repo_path):
        try:
            # Cambiar al directorio del repositorio
            os.chdir(repo_path)
            
            # Verificar y cambiar a la rama especificada
            subprocess.check_call(['git', 'checkout', branch_name])
            
            # Agregar el archivo al índice de Git
            subprocess.check_call(['git', 'add', file_path])

            # Hacer un commit con el archivo
            commit_message = f'Añadiendo archivo {file_path}'
            subprocess.check_call(['git', 'commit', '-m', commit_message])

            # Empujar los cambios a la rama especificada en el repositorio remoto
            subprocess.check_call(['git', 'push', 'origin', branch_name])
            
            # Cambiar a la rama main
            subprocess.check_call(['git', 'checkout', 'main'])

            # Intentar fusionar los cambios de la rama especificada en main
            try:
                subprocess.check_call(['git', 'merge', '--allow-unrelated-histories', '--no-ff', branch_name])
            except subprocess.CalledProcessError:
                # Si la fusión falla, abortarla y retornar un mensaje de error
                subprocess.check_call(['git', 'merge', '--abort'])
                return False, 'Error al fusionar las ramas.'

            # Empujar los cambios a la rama main en el repositorio remoto
            subprocess.check_call(['git', 'push', 'origin', 'main'])

            return True, 'Archivo subido con éxito a ambas ramas.'

        except subprocess.CalledProcessError as e:
            return False, f'Error al subir el archivo: {e}'


# Uso:
# token = 'TU_TOKEN_DE_ACCESO_PERSONAL'
# manager = GitHubManager(token)
# success, message = manager.create_repository('desarrolloSoftwareFT', 'nombre_del_repositorio', 'Descripción del repositorio')
# print(message)

class CreateRepoDialog(QDialog):
    #def __init__(self, selected_org, github_manager):
    def __init__(self, selected_org, github_manager):
        super().__init__()
        self.github_manager = github_manager
        self.selected_org = selected_org
        print(self.selected_org)
        self.initUI()

    def initUI(self):
        # Widgets
        self.repo_name_label = QLabel("Nombre del Repositorio:")
        self.repo_name_input = QLineEdit(self)
        self.repo_desc_label = QLabel("Descripción (opcional):")
        self.repo_desc_input = QLineEdit(self)
        
        # Nuevos widgets para seleccionar el directorio
        self.local_dir_label = QLabel("Directorio Local:")
        self.local_dir_input = QLineEdit(self)
        self.browse_button = QPushButton("Examinar", self)
        self.browse_button.clicked.connect(self.browse_directory)

        self.create_button = QPushButton("Crear Repositorio", self)
        self.create_button.clicked.connect(self.create_repo)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.repo_name_label)
        layout.addWidget(self.repo_name_input)
        layout.addWidget(self.repo_desc_label)
        layout.addWidget(self.repo_desc_input)
        
        # Layout para directorio local
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.local_dir_input)
        dir_layout.addWidget(self.browse_button)
        
        layout.addWidget(self.local_dir_label)
        layout.addLayout(dir_layout)
        layout.addWidget(self.create_button)
        self.setLayout(layout)

    def browse_directory(self):
        # Abre un cuadro de diálogo para seleccionar un directorio
        directory = QFileDialog.getExistingDirectory(self, "Selecciona un directorio")
        if directory:
            self.local_dir_input.setText(directory)

    def create_repo(self):
        repo_name = self.repo_name_input.text()
        description = self.repo_desc_input.text()
        local_path = self.local_dir_input.text()

        # Crear el repositorio en GitHub
        success, message = self.github_manager.create_repository(self.selected_org, repo_name, description)

        if success:
            # Clonar el repositorio creado en la ruta local
            clone_success, clone_message = self.github_manager.clone_repository_to_local(self.selected_org, repo_name, local_path)
            
            if clone_success:
                # Cambia al directorio clonado
                os.chdir(local_path)
                
                # Crea un archivo README.md con un mensaje inicial
                with open('README.md', 'w') as f:
                    f.write("# " + repo_name + "\nRepositorio inicializado con un archivo README.")
                    
                # Agrega el archivo al índice de git
                subprocess.check_call(['git', 'add', 'README.md'])
                
                # Confirma el archivo
                subprocess.check_call(['git', 'commit', '-m', 'Commit inicial con README'])
                
                # Hace un push de la confirmación a GitHub
                subprocess.check_call(['git', 'push', 'origin', 'main'])  # Ahora usamos 'main' en lugar de 'master'
                
            else:
                QMessageBox.warning(self, "Advertencia", clone_message)
            
        QMessageBox.information(self, "Información", message)
        if success:
            self.close()


class CreateBranchDialog(QDialog):
    def __init__(self, selected_org, github_manager):
        super().__init__()
        self.github_manager = github_manager
        self.selected_org = selected_org
        self.initUI()

    def initUI(self):
        # Widgets
        self.select_repo_label = QLabel("Seleccionar Repositorio:")
        self.select_repo_combo = QComboBox(self)
        
        existing_repositories = self.github_manager.get_existing_repositories(self.selected_org)
        self.select_repo_combo.addItems(existing_repositories)

        #Ahora el widget para crear la seleccion del a ruta al examinar directorios

        # Nuevos widgets para seleccionar el directorio
        self.local_dir_label_branch = QLabel("Directorio Rama Local:")
        self.local_dir_input_branch = QLineEdit(self)
        self.browse_button_branch = QPushButton("Examinar", self)
        self.browse_button_branch.clicked.connect(self.browse_directory)
        
        
        self.branch_name_label = QLabel("Nombre de la Rama:")
        self.branch_name_input = QLineEdit(self)
        
        self.create_button = QPushButton("Crear Rama", self)
        self.create_button.clicked.connect(self.create_branch)

        # Layout General
        layout = QVBoxLayout()
        layout.addWidget(self.select_repo_label)
        layout.addWidget(self.select_repo_combo)

        # Layout vertical directorio local
        #layout_2 = QVBoxLayout()
        #layout_2.addWidget(self.local_dir_label_branch)
        #layout_2.addWidget(self.local_dir_input_branch)

        # Layout para directorio local
        dir_layout = QHBoxLayout()
        dir_layout.addWidget( self.local_dir_input_branch)
        dir_layout.addWidget(self.browse_button_branch)

        layout.addWidget(self.local_dir_label_branch)
        layout.addLayout(dir_layout)
        layout.addWidget(self.branch_name_label)
        layout.addWidget(self.branch_name_input)
        layout.addWidget(self.create_button)
        self.setLayout(layout)
    
    def browse_directory(self):
        # Abre un cuadro de diálogo para seleccionar un directorio
        directory = QFileDialog.getExistingDirectory(self, "Selecciona un directorio")
        if directory:
            self.local_dir_input_branch.setText(directory)

    def create_branch(self):
        selected_repo = self.select_repo_combo.currentText()
        branch_name = self.branch_name_input.text()
        local_dir = self.local_dir_input_branch.text() # Captura la ruta del directorio aquí
        ...
        success, message = self.github_manager.push_new_branch_to_existing_repo(selected_repo, branch_name, local_dir)

        # Notificar al usuario sobre el resultado de la operación
        if success:
            QMessageBox.information(self, "Éxito", "Creación de rama exitosa.")
            self.close() # Cierra el cuadro de diálogo
        else:
            QMessageBox.warning(self, "Error", message)


class UploadFileDialog(QDialog):

    def __init__(self, selected_org, github_manager,ruta_corregida_directory):
        super().__init__()
        self.github_manager = github_manager
        self.selected_org = selected_org
        self.ruta_corregida_directory = ruta_corregida_directory
        #existing_repositories = self.github_manager.get_existing_repositories(self.selected_org)
        #self.selected_repo = existing_repositories
        self.selected_repo = None
        self.initUI()
    
    def initUI(self):
        # Widgets
        self.select_repo_label = QLabel("Seleccionar Repositorio:")
        self.select_repo_combo = QComboBox(self)

        self.branch_label = QLabel("Seleccionar Rama:")
        self.branch_combo = QComboBox(self)

        # Widgets para seleccionar y mostrar el archivo/carpeta
        self.select_file_button = QPushButton("Seleccionar", self)
        self.select_file_button.clicked.connect(self.select_file_or_directory)
        self.file_path_label = QLabel("Ruta del directorio: No seleccionado")

        # Botón para subir el archivo/carpeta
        self.upload_button = QPushButton("Subir directorio", self)
        self.upload_button.clicked.connect(self.upload_to_github)


        
        existing_repositories = self.github_manager.get_existing_repositories(self.selected_org)
        self.select_repo_combo.addItems(existing_repositories)

        layout = QVBoxLayout()
        layout.addWidget(self.select_repo_label)
        layout.addWidget(self.select_repo_combo)
        layout.addWidget(self.branch_label)
        layout.addWidget(self.branch_combo)

        layout.addWidget(self.select_file_button)
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.upload_button)


        self.setLayout(layout)
        
        # Conectar el cambio de ítem seleccionado en el combo box a una función
        self.select_repo_combo.currentIndexChanged.connect(self.on_repo_selected)
        

    def select_file_or_directory(self):
        msgBox = QMessageBox(self)
        msgBox.setText("Directorio a subir Master/Local")
        
        fileButton = msgBox.addButton("Archivo", QMessageBox.ActionRole)
        directoryButton = msgBox.addButton("Directorio", QMessageBox.ActionRole)
        cancelButton = msgBox.addButton(QMessageBox.Cancel)
        
        msgBox.exec_()
        
        
        if msgBox.clickedButton() == fileButton:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Todos los archivos (*);;", options=options)
            if file_name:
                self.file_path_label.setText(f"Ruta del archivo: {file_name}")
                self.selected_file = file_name
            else:
                self.selected_file = None
        
        elif msgBox.clickedButton() == directoryButton:
        #if msgBox.clickedButton() == directoryButton:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            directory_name = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "", options=options)
            if directory_name:
                self.file_path_label.setText(f"Ruta de la carpeta: {directory_name}")
                self.selected_file = directory_name
            else:
                self.selected_file = None


    
    def get_branches_of_repository(self, repo_name):
        try:
            url = f"{self.base_url}/repos/{self.selected_org}/{repo_name}/branches"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            branches = response.json()
            return [branch['name'] for branch in branches]
        except requests.RequestException as e:
            print(f"Error al obtener las ramas de {repo_name}: {e}")
            return []
    
    def on_repo_selected(self):
        self.selected_repo = self.select_repo_combo.currentText()
        # Aquí puedes llamar a la función para obtener las ramas del repositorio seleccionado
        branches = self.github_manager.get_branches_of_repository(self.selected_org, self.selected_repo)

        # Limpiar el combo box de ramas (si existe) y agregar las nuevas ramas
        self.branch_combo.clear()
        self.branch_combo.addItems(branches)
    
    def upload_to_github(self):
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un archivo o carpeta primero.")
            return

        #esta manera es cuando se hacia de manera directa
        #repo_path = GitViewer.resource_path(f"programas/{self.selected_repo}")

        repo_path = os.path.join(self.ruta_corregida_directory, self.selected_repo)

        #print("Archivo:", file_path)
        #if not os.path.exists(file_path):
        #    print(f"El archivo {file_path} no existe!")

        success, message = self.github_manager.upload_file_to_repo(self.selected_repo, self.branch_combo.currentText(), self.selected_file, repo_path)

        print("Directorio del repositorio:", repo_path)
        if not os.path.exists(repo_path):
            print(f"El directorio {repo_path} no existe!")
        
        print("Directorio actual:", os.getcwd())
        os.chdir(repo_path)
        print("Después de cambiar el directorio:", os.getcwd())

        print(subprocess.check_output(['git', 'branch']).decode())
        print(subprocess.check_output(['git', 'status']).decode())
        QMessageBox.information(self, "Información", message)


class GitViewer(QMainWindow):

    #def __init__(self, controlador, username=None):
    def __init__(self, selected_org, username,ruta_corregida_directory, controlador):
        super().__init__()
        self.username = username
        self.controlador = controlador
        self.selected_org = selected_org
        self.ruta_corregida_directory = ruta_corregida_directory

        # Asegúrate de que el objeto HistorialManager esté inicializado
        #Instancia de la clase HistorialManager:
        self.historial_manager = HistorialManager()

        # Instancia de la clase GitHubManager:
        self.github_manager = GitHubManager()

        # Registrar los cambios de todos los repositorios al inicio
        self.historial_manager.registrar_cambios_de_todos_los_repositorios(ruta_corregida_directory)
    
        # Crear una instancia de VisualizadorTabla (aún no se muestra)
        self.ventana_tabla = VisualizadorTabla(controlador)

        # Inicializar la UI
        self.initUI()

        #variable familia
        self.familia = self.controlador.current_familia
    

    
    def mostrar_tabla(self):
        # Mostrar la instancia de VisualizadorTabla cuando sea necesario
        self.ventana_tabla.show()
    
    #-----------------------metodo para la logica de comparacion --------------------------------

    def get_file_changes(self, commit_hash, file_path, master_repo_path):
        """Obtiene el contexto de las líneas modificadas en el archivo para la rama master."""
        repo = git.Repo(master_repo_path)
        # Obtener el contenido del archivo en la rama main
        main_content = repo.git.show(f"main:{file_path}")
        return main_content

    def get_file_changes_2(self, commit_hash, file_path, ruta2):
        """Obtiene las líneas modificadas en el archivo para la rama actual."""
        repo = git.Repo(ruta2)
        # Obtener el contenido del archivo en el commit especificado
        commit_content = repo.git.show(f"{commit_hash}:{file_path}")
        return commit_content

    def get_modified_files_from_commit(self, master_repo_path, selected_branch):
        """Obtiene una lista de archivos modificados entre la rama main y la rama seleccionada."""
        repo = git.Repo(master_repo_path)
        modified_files = repo.git.diff('main', '--', selected_branch, name_only=True).splitlines()
        return modified_files

 

    def show_changes(self):
        familia = self.controlador.current_familia
        #selected_branch = self.controlador.current_ensamble
        # Toma solo el primer fragmento del ensamble
        selected_branch = self.controlador.current_ensamble.split('/')[0]
        print(familia)
        print(selected_branch)

        self.ventana_tabla.text_master.clear()
        self.ventana_tabla.text_Actual.clear()

        # Formato de texto predeterminado
        char_format_default = QTextCharFormat()

        #repo_name = self.repositorio_combobox.currentText()
        repo_name= familia
        #selected_branch = self.branch_combobox.currentText()

        #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"
        base_path = self.ruta_corregida_directory

        master_repo_path = os.path.join(base_path, repo_name)
        ruta2 = os.path.join(base_path, repo_name)

        #-----pruebas de los datos a pasar ------
        print("las variables son")
        print(master_repo_path)
        print(selected_branch)

        modified_files = self.get_modified_files_from_commit(master_repo_path, selected_branch)

        for file_path in modified_files:
            latest_commit_hash = git.Repo(master_repo_path).commit(selected_branch).hexsha
            master_content = self.get_file_changes(latest_commit_hash, file_path, master_repo_path)
            actual_content = self.get_file_changes_2(latest_commit_hash, file_path, ruta2)

            # Agregar el nombre del archivo a las ventanas de texto en ambos "terminales"
            self.ventana_tabla.text_master.appendPlainText(f"Archivo: {file_path}\n")
            
            cursor = self.ventana_tabla.text_Actual.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(f"Archivo: {file_path}\n", char_format_default)  # Usar el formato de texto predeterminado
            
            diffs = list(unified_diff(master_content.splitlines(), actual_content.splitlines()))

            # Resaltar las líneas modificadas
            char_format_highlight = QTextCharFormat()
            char_format_highlight.setBackground(QColor("green"))
            char_format_highlight.setForeground(QColor("white"))
            
            for diff in diffs:
                if diff.startswith('-'):
                    self.ventana_tabla.text_master.appendPlainText(diff)
                elif diff.startswith('+'):
                    cursor = self.ventana_tabla.text_Actual.textCursor()
                    cursor.movePosition(QTextCursor.End)
                    cursor.insertText(diff + '\n', char_format_highlight)
                    cursor.insertText("", char_format_default)  # Restablecer el formato de texto a predeterminado
                else:
                    continue  # Ignorar líneas que no empiezan con '-' o '+'
            
            # Agregar un espacio en blanco al final de cada bloque de cambios
            self.ventana_tabla.text_master.appendPlainText("\n")
            cursor = self.ventana_tabla.text_Actual.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText("\n", char_format_default)  # Usar el formato de texto predeterminado


    def get_line_range(self, line_num, padding=10):
        """Devuelve un rango de líneas centrado en line_num, con un padding especificado."""
        start = max(line_num - padding, 0)  # Asegurarse de que no sea negativo
        end = line_num + padding
        return start, end
   
    def sync_files(self, master_repo_path, local_repo_path):
        """Sincroniza archivos de local_repo_path a master_repo_path."""
        
        # Obtener el nombre de la rama seleccionada
        selected_branch = self.branch_combobox.currentText()

        commits = self.get_modified_files_from_commit(master_repo_path, selected_branch)
        if not commits:
            return False

        for file_path in commits:
            source_file = os.path.join(local_repo_path, file_path)
            dest_file = os.path.join(master_repo_path, file_path)
            if os.path.exists(source_file):
                shutil.copy2(source_file, dest_file)
        return True

    def check_for_changes(self,master_repo_path):
        """Verificar si hay cambios en ruta1."""
        result = subprocess.run(['git', 'status', '--porcelain'], cwd=master_repo_path, capture_output=True, text=True)
        return bool(result.stdout.strip())

    def commit_and_push_changes(self,master_repo_path):
        """Registrar y subir los cambios de ruta1."""
        subprocess.run(['git', 'add', '.'], cwd=master_repo_path)
        subprocess.run(['git', 'commit', '-m', 'Sincronización con archivos de la ruta local'], cwd=master_repo_path)
        subprocess.run(['git', 'push'], cwd=master_repo_path)

    def sync_files_with_master(self):
            # Ruta base común
            #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"

            base_path = self.ruta_corregida_directory
            
            # Obtener los valores de familia y rama desde la tabla principal
            familia = self.controlador.current_familia
            rama = self.controlador.current_ensamble.split('/')[0]
            
            # Ruta del repositorio basada en la selección del usuario
            repo_name = familia
            repo_path = os.path.join(base_path, repo_name)

            # Cambiar a la rama deseada
            #print(f"Cambiando a la rama {rama}")
            #subprocess.run(['git', 'checkout', rama], cwd=repo_path)
            
            # Cambiar a la rama main para poder registrar y subir los cambios
            print("Cambiando a la rama main")
            subprocess.run(['git', 'checkout', 'main'], cwd=repo_path)
            
            # Hacer un merge de la rama local en la rama main
            print(f"Haciendo merge de la rama {rama} en la rama main")
            subprocess.run(['git', 'merge', rama], cwd=repo_path)

            # Empujar los cambios a la rama main del repositorio remoto
            print("Empujando los cambios a la rama main")
            subprocess.run(['git', 'push'], cwd=repo_path)
            
            QMessageBox.information(self, "Sincronización", "Archivos sincronizados con éxito con Master!")
    #----------------------------------------------------------------------------------------------------------------------------

    def git_add_commit_push(self, mensaje_commit, selected_repo_path):
        try:
            # Cambiar el directorio de trabajo a la ruta del repositorio local
            os.chdir(selected_repo_path)

            # Obtener el nombre de la rama seleccionada del combobox
            selected_branch = self.branch_combobox.currentText()

            # Cambiar a la rama seleccionada
            subprocess.run(['git', 'checkout', selected_branch])

            # Establecer la rama remota para la rama local
            subprocess.run(['git', 'branch', '--set-upstream-to=origin/' + selected_branch, selected_branch])

            # Agregar los cambios
            subprocess.run(['git', 'add', '.'])

            # Hacer el commit
            subprocess.run(['git', 'commit', '-m', mensaje_commit])

            # Realizar el pull con rebase para obtener los cambios del repositorio remoto y aplicar los cambios locales encima
            subprocess.run(['git', 'pull', '--rebase'])

            # Realizar el push con el token
            user="nicolas9710"
            token="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"
            repo_url = f"https://{user}:{token}@github.com/desarrolloSoftwareFT/SpitFire.git"
            subprocess.run(['git', 'push', repo_url])

            # Realizar un git push normal
            subprocess.run(['git', 'push'])

            # Muestra un mensaje de éxito
            QMessageBox.information(self, "Cambios finalizados", "Los cambios se han enviado al repositorio remoto.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al hacer commit y push: {str(e)}")


    
    "resolver rutas"
    @classmethod #de esta manera lo defines como metodo de clase
    def resource_path(cls, relative_path):
        

        # Get absolute path to resource, works for dev and for PyInstaller 
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def metodo_crear_rama(self):
        branch_dialog = CreateBranchDialog(self.selected_org,self.github_manager)
        branch_dialog.exec_()
    
    def metodo_subir_archivo(self):
        branch_dialog = UploadFileDialog(self.selected_org,self.github_manager,self.ruta_corregida_directory)
        branch_dialog.exec_()

    def metodo_crear_repo (self):
        #para la creacion de repositorios
        self.create_repo_dialog = CreateRepoDialog(self.selected_org, self.github_manager)
        self.create_repo_dialog.exec_()
    
    def on_repo_selected(self):
        self.selected_repo = self.repositorio_combobox.currentText()
        # Aquí puedes llamar a la función para obtener las ramas del repositorio seleccionado
        branches = self.github_manager.get_branches_of_repository(self.selected_org, self.selected_repo)

        # Limpiar el combo box de ramas (si existe) y agregar las nuevas ramas
        self.branch_combobox.clear()
        self.branch_combobox.addItems(branches)

    def initUI(self):
        #-----propiedades ventana Controlador de versiones-------------

        self.setWindowTitle('Control de versiones')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #------Separacion de contenedores en la ventana--------------

        # Crear un splitter para dividir la ventana en tres secciones
        splitter = QSplitter()

        # Crear tres frames para cada sección
        top_frame = QWidget()
        left_frame = QWidget()
        right_frame = QWidget()

        # Configurar el splitter para dividir horizontalmente
        splitter.setOrientation(Qt.Horizontal)  # Utiliza 'Qt.Horizontal' en lugar de 1

        # Agregar los frames al splitter
        splitter.addWidget(top_frame)
        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)

        # Configurar el tamaño inicial de los frames
        splitter.setSizes([400, 100, 500])

        #-------Creacion de la disposición del Top frame----------------
       
        # Crear un layout vertical para el frame superior
        #top_layout = QHBoxLayout() #Oorganiza los widgets de manera horizontal
        top_layout = QVBoxLayout()
        
        # Establece los márgenes alrededor de top_layout
        top_layout.setContentsMargins(0, 0, 0, 0)  # Ajusta los valores según tus preferencias

        # Establece el espacio entre widgets dentro de top_layout
        top_layout.setSpacing(0)  # Ajusta el valor según tus preferencias      

        # Establecer el splitter como widget central
        central_layout = QVBoxLayout()  # Crea un layout vertical para el widget central
        central_layout.addWidget(splitter)  # Agrega el splitter al layout central
        
        #Este elemento me indica como se va dividir la pantalla principal
        #central_widget.setLayout(central_layout)  # Establece el layout central en el widget central

         # Crear un layout de cuadrícula para organizar los tres frames
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)  # Establecer el layout de la ventana principal
  
        #grid_layout = QGridLayout()
        grid_layout.addWidget(top_frame, 0, 0, 1, 2)  # Frame superior ocupa dos columnas
        grid_layout.addWidget(left_frame, 1, 0)       # Frame izquierdo en la fila 1, columna 0
        grid_layout.addWidget(right_frame, 1, 1)      # Frame derecho en la fila 1, columna 1
        

        # Crear un layout para el frame derecho
        #Este layout le corresponde a colocar los elementos en cuadricula
        #layout = QGridLayout()
        layout = QVBoxLayout()

        # Crear un layout vertical para el frame izquierdo
        left_layout = QVBoxLayout()

        #--------datos para la tabla top------------------

         # Datos de ejemplo para la tabla (puedes reemplazarlos con tus propios datos)
        data_top = [
            ["Ensamble", "Nombre del archivo", "Familia","Version", "Responsable", "Cambios"],
            ["Alice", "25", "EE. UU."],
            ["Bob", "30", "Canadá"],
            ["Ch", "28", "Reino Unido"],
            ["Ch", "28", "Reino Unido"],
            ["Ch", "28", "Reino Unido"],
            ["Ch", "28", "Reino Unido"],
            
        ]
        
        self.data_top = data_top

        # Crear una tabla para mostrar los datos del top
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(len(self.data_top[0]))
        self.tabla.setRowCount(len(self.data_top))
        
        #Para cambiar el tamaño de la tabla se coloca de esta manera porque esta dentro de un layout
        self.tabla.setMinimumSize(650, 400)
        self.tabla.setMaximumSize(650, 400)

        #Ocultar el encabezado numerico tanto de las filas como las columnas
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setVisible(False)

        #De esta manera se redimensiona el tamaño de las filas y columnas al tamaño que ocupa la tabla
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #De esta manera se modifica el tamaño de las columnas vertical
        vh =self.tabla.verticalHeader()
        vh.setDefaultSectionSize(50)
        # vh.setResizeMode(QtGui.QHeaderView.Fixed)

        #De esta manera se modifica el tamaño de las filas horizontal
        hh = self.tabla.horizontalHeader()
        hh.setDefaultSectionSize(300)

        # Agregar los datos a la tabla
        color_cielo = QtGui.QColor("#6599FF")  # Color azul especificado
        for fila, datos_fila in enumerate(self.data_top):
            for columna, valor in enumerate(datos_fila):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Si es la primera fila, cambiar el color de fondo
                if fila == 0:
                    item.setBackground(color_cielo)

                self.tabla.setItem(fila, columna, item)


        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tabla.resizeColumnsToContents()

        #al hacer clic en la celdas
        self.tabla.cellClicked.connect(self.cell_was_clicked)

        #le acondiciono que la columna que tendra lo del clic sera la de cambios
        self.indice_columna_cambios = 2 #columna cambios

        self.layout_top = QVBoxLayout()
        self.layout_top.addWidget(self.tabla)
        #central_widget.setLayout(layout_top)

         # Aquí rellenas la tabla de la UI con los datos
        self.historial_manager.actualizar_tabla(self.tabla)  # Asumiendo que "tabla" es el nombre de tu QTableWidget

        #--------------Right Frame ---------------------------------

        self.cambios_output = QTextEdit()
        self.cambios_output.setReadOnly(True)
        #layout.addWidget(self.cambios_output)

        self.mostrar_cambios_button = QPushButton('Mostrar Cambios')
        #self.mostrar_cambios_button.setFont(QFont('Segoe UI', 12))  # Cambiar el estilo de fuente
        self.mostrar_cambios_button.clicked.connect(self.mostrar_cambios)
        self.mostrar_cambios_button.setMinimumWidth(50) 
        self.mostrar_cambios_button.setMaximumWidth(150)
        #layout.addWidget(self.mostrar_cambios_button)

        # Botón para revertir cambios
        self.revertir_cambios_button = QPushButton('Revertir Cambios')
        #self.revertir_cambios_button.setFont(QFont('Segoe UI', 12))  # Cambiar el estilo de fuente
        self.revertir_cambios_button.clicked.connect(self.revertir_cambios)
        self.revertir_cambios_button.setMinimumWidth(50) 
        self.revertir_cambios_button.setMaximumWidth(150)
        #layout.addWidget(self.revertir_cambios_button)

        #------Botones para eliminar ----------
        #  
        # Agregar un label 
        self.repositorio = QLabel('Seleccionar Repositorio:')
        
        # Agregar un combo box para seleccionar el repositorio
        self.repositorio_combobox = QComboBox()

        # Agregar al combo box los repositorios
        existing_repositories = self.github_manager.get_existing_repositories(self.selected_org)
        self.repositorio_combobox.addItems(existing_repositories)

        # Conectar la señal currentIndexChanged a la función registrar_cambios
        self.repositorio_combobox.currentIndexChanged.connect(self.registrar_cambios)


        #-------------------revisar esto --------------------------------

        historial_manager = HistorialManager()
        #selected_repo = self.repositorio_combobox.currentText()

        #repo_path = GitViewer.resource_path(f"programas/{selected_repo}")

        historial_manager.comprobar_cambios(existing_repositories, self.tabla)

        #-----------------------------------------------------------------

        # Agregar un label a la ventana principal
        
        self.branch_label = QLabel('Seleccionar Rama:')
        
        # Agregar un combo box para seleccionar las ramas
        self.branch_combobox = QComboBox()  

        self.selected_repo = self.branch_combobox.currentText()


        # Aquí puedes llamar a la función para obtener las ramas del repositorio seleccionado
        branches = self.github_manager.get_branches_of_repository(self.selected_org, self.selected_repo)

        self.repositorio_combobox.currentIndexChanged.connect(self.on_repo_selected)

        # Limpiar el combo box de ramas (si existe) y agregar las nuevas ramas
        self.branch_combobox.clear()
        self.branch_combobox.addItems(branches)

        # Agregar un label a la ventana principal
        self.branch_commit = QLabel('Seleccionar Commit:')
        #self.branch_commit.setFont(QFont('Segoe UI', 14))  # Cambiar el estilo de fuente

        # Agregar un combo box para seleccionar el commit a revertir
        self.commit_combobox = QComboBox()

        
        #modificar tamaño del combo box
        self.commit_combobox.setMinimumHeight(25)
        self.commit_combobox.setMaximumHeight(80)

        # Agregar un botón para actualizar la vista según la rama seleccionada
        self.actualizar_button = QPushButton('Comprobar cambios')
        #self.actualizar_button.setFont(QFont('Segoe UI', 12))  # Cambiar el estilo de fuente
        
        #logica anterior que solo llama a mandar un metodo
        self.actualizar_button.clicked.connect(self.actualizar_vista)

        #logica nueva que manda a llamar dos metodos
        #self.actualizar_button.clicked.connect(lambda: (self.actualizar_vista(), self.comprobar_cambios()))


        #------ con respecto a mostrar los commits-----------------------------

        # Agregar un botón para actualizar la vista según los commits
        self.actualizar_button_commit = QPushButton('Lista de cambios realizados') #lista de commits
        self.actualizar_button_commit.clicked.connect(self.actualizar_vista_commit)

        #modificar tamaño del boton actualizar lista de commits:
        self.actualizar_button_commit.setMinimumWidth(150)
        self.actualizar_button_commit.setMaximumWidth(200)


        #boton para escribir o sobreescribir el archivo versiones.log
        self.crear_versiones = QPushButton('Versiones.log')
        self.crear_versiones.clicked.connect(lambda: self.escribir_versiones_log(self._commits))

        #modificar tamaño del boton actualizar lista de commits:
        self.crear_versiones.setMinimumWidth(150)
        self.crear_versiones.setMaximumWidth(200)    

        self.mostrar_historial_button = QPushButton('Mostrar Historial')
        #self.mostrar_historial_button.setFont(QFont('Segoe UI', 12))  # Cambiar el estilo de fuente
        self.mostrar_historial_button.clicked.connect(self.mostrar_historial)

        # Botón para realizar commit y push
        self.commit_push_button = QPushButton('Enviar Cambios')
        #self.commit_push_button.setFont(QFont('Segoe UI', 12))  # Cambiar el estilo de fuente
        self.commit_push_button.clicked.connect(self.hacer_commit_y_push)


        #-------grupo para los botones mostrar y revertir cambios--------------

        verticalInnercambios = QVBoxLayout()
        verticalInnercambios.addWidget(self.mostrar_cambios_button)

        horizontalInnercambios = QHBoxLayout()
        horizontalInnercambios.addLayout( verticalInnercambios )
        horizontalInnercambios.addWidget( self.revertir_cambios_button )

        self.groupBox3 = QGroupBox( "Realizar cambios" )
        self.groupBox3.setLayout( horizontalInnercambios )

        #------grupo para los filtros para realizar el commit y el push-------

        verticalFiltros = QVBoxLayout()
        verticalFiltros.addWidget(self.repositorio)
        verticalFiltros.addWidget(self.repositorio_combobox)

        verticalFiltros_2 = QVBoxLayout()
        verticalFiltros_2.addWidget(self.branch_label)
        verticalFiltros_2.addWidget(self.branch_combobox)

        verticalFiltros_3 = QVBoxLayout()
        verticalFiltros_3.addWidget(self.branch_commit)
        verticalFiltros_3.addWidget(self.commit_combobox)

        horizontalFiltros = QHBoxLayout()
        horizontalFiltros.addLayout( verticalFiltros )
        horizontalFiltros.addLayout( verticalFiltros_2 )
        horizontalFiltros.addLayout( verticalFiltros_3 )
       
        self.groupBoxfiltros = QGroupBox( "Filtros" )
        self.groupBoxfiltros.setLayout( horizontalFiltros )

        #---------------groupbox Commits -------------------------------

        verticalcommits = QVBoxLayout()
        verticalcommits.addWidget(self.actualizar_button_commit)

        horizontalcommits = QHBoxLayout()
        horizontalcommits.addLayout( verticalcommits )
        horizontalcommits.addWidget( self.crear_versiones )

        self.groupBoxcommits = QGroupBox( "Lista cambios" )
        self.groupBoxcommits.setLayout( horizontalcommits )


        #------Organizar elementos Right Frame --------------------------------

        verticalInnerLayout_repositorio = QVBoxLayout()
        verticalInnerLayout_repositorio.addWidget(self.cambios_output)
        verticalInnerLayout_repositorio.addWidget(self.groupBox3)
        verticalInnerLayout_repositorio.addWidget(self.groupBoxfiltros)
        verticalInnerLayout_repositorio.addWidget(self.actualizar_button)
        verticalInnerLayout_repositorio.addWidget(self.groupBoxcommits)
        verticalInnerLayout_repositorio.addWidget(self.commit_push_button)

        self.groupBox_repositorio = QGroupBox( "Cambios en el Repositorio" )
        self.groupBox_repositorio.setLayout( verticalInnerLayout_repositorio )

        #-------------------------Frame Top ------------------------------

        #widgets para la imagen y el nombre del usuario
        self.usuario_label = QLabel('')
        self.usuario_label.setFont(QFont('Segoe UI', 14)) 
  
        self.usuario_label_login = QLabel('')
        self.usuario_label_login.setFont(QFont('Segoe UI', 14))
        self.usuario_label_login.setText(self.username)

        #Widget para colocar la imagen
        self.usuario_espacio = QLabel('')

        #Para el grupo de usuario

        verticalInnerLayout = QVBoxLayout()
        verticalInnerLayout.addWidget(self.usuario_label)
        verticalInnerLayout.addWidget(self.usuario_label_login)

        horizontalInnerLayout = QHBoxLayout()
        horizontalInnerLayout.addLayout( verticalInnerLayout )
        horizontalInnerLayout.addWidget( self.usuario_espacio )

        self.groupBox3 = QGroupBox( "Usuario" )
        self.groupBox3.setLayout( horizontalInnerLayout )


        # Botón para sincronizar archivos con la ruta1 (Master)
        self.sync_button = QPushButton("Sincronizar con Master")
        self.sync_button.clicked.connect(self.sync_files_with_master)      

        horizontalInnerLayout = QHBoxLayout()
        horizontalInnerLayout.addLayout( self.layout_top )
        #horizontalInnerLayout.addLayout( verticalInnerLayout_2 )
        
        self.groupBox1 = QGroupBox( "Historial de cambios" )
        self.groupBox1.setLayout( horizontalInnerLayout )

        #-----2 GroupBox TOP grame ----------------------

          # Crear un botón para el historial de cambios
        self.boton_prueba = QPushButton('Comparacion de archivos')
        #self.boton_prueba.setFont(QFont('Segoe UI', 12))  # Cambiar el estilo de fuente
        self.boton_prueba.setMinimumWidth(50)  # Establece el ancho mínimo
        self.boton_prueba.setMaximumWidth(150)  # Establece el ancho máximo
        self.boton_prueba.clicked.connect(self.mostrar_tabla)

          # Crear un botón para el historial de cambios
        self.boton_crear_repo = QPushButton('Creacion repositorio')
        self.boton_crear_repo.setMinimumWidth(50)  # Establece el ancho mínimo
        self.boton_crear_repo.setMaximumWidth(150)  # Establece el ancho máximo
        self.boton_crear_repo.clicked.connect(self.metodo_crear_repo)

        # Crear un botón para el historial de cambios
        self.boton_crear_rama = QPushButton('Creacion ramas')
        self.boton_crear_rama.setMinimumWidth(50)  # Establece el ancho mínimo
        self.boton_crear_rama.setMaximumWidth(150)  # Establece el ancho máximo
        self.boton_crear_rama.clicked.connect(self.metodo_crear_rama)

        # Crear un botón para el historial de cambios
        self.boton_subir_archivos = QPushButton('Subir Archivos a ramas')
        self.boton_subir_archivos.setMinimumWidth(50)  # Establece el ancho mínimo
        self.boton_subir_archivos.setMaximumWidth(150)  # Establece el ancho máximo
        self.boton_subir_archivos.clicked.connect(self.metodo_subir_archivo)

        verticalInnerLayout = QVBoxLayout()
        verticalInnerLayout.addWidget( self.boton_prueba )

        horizontalInnerLayout = QHBoxLayout()
        horizontalInnerLayout.addLayout( verticalInnerLayout )
        horizontalInnerLayout.addWidget( self.boton_crear_repo )
        horizontalInnerLayout.addWidget( self.boton_crear_rama )
        horizontalInnerLayout.addWidget( self.boton_subir_archivos )
        
        self.groupBox2 = QGroupBox( "Ventanas" )
        self.groupBox2.setLayout( horizontalInnerLayout )


        #modificar margenes
        self.usuario_label.setContentsMargins(0, 0, 0, 0)  # Establece los márgenes en cero
        self.usuario_label_login.setContentsMargins(0, 0, 0, 0)  # Establece los márgenes en cero

        #--------imagen usuario ------------

        # Carga la imagen utilizando resource_path
        imagen_path = self.resource_path('imagenes/user.png')
        pixmap = QPixmap(imagen_path)
        pixmap = pixmap.scaled(50, 50)
        self.usuario_label.setPixmap(pixmap)

         #-------imagen logo flex -----------

        # Carga la imagen utilizando resource_path
        imagen_path_2 = self.resource_path('imagenes/flex_loga.png')
        pixmap_2 = QPixmap(imagen_path_2)
        pixmap_2 = pixmap_2.scaled(100, 100)
        self.usuario_espacio.setPixmap(pixmap_2)

        #------------------------- Frame left  ------------------------------

        # Nuevo campo de entrada para mostrar el nombre de usuario
        self.Archivo_entry = QLineEdit()
        self.Archivo_entry.setPlaceholderText('Archivo')
        self.Archivo_entry.setReadOnly(True)
        self.Archivo_entry.setText("Aqui va el nombre del Archivo")  # Establecer el nombre de usuario aquí
        #self.Archivo_entry.setFont(QFont('Segoe UI', 12))  # Cambiar el estilo de fuente
        #layout.addWidget(self.usuario_entry)

        #horizontalInnerLayout = QHBoxLayout()
        #horizontalInnerLayout.addLayout( verticalInnerLayout_Archivo )
        #horizontalInnerLayout.addWidget( self.usuario_espacio )


        #-------------posicionamiento widgets right frame --------

        # Agregar widgets a la cuadrícula en celdas específicas
        #Ejemplo
        #layout.addWidget(self.archivos_label, 0, 0, 1, 2)  # (widget, row, column, rowspan, columnspan)


        #----Posicionamiento widgets right frame---------
        layout.addWidget(self.groupBox_repositorio)

        #------- posicionamiento widgets top frame ---------

        #top_layout.addWidget(self.usuario_label)
        #top_layout.addWidget( self.usuario_label_login)
        #top_layout.addWidget( self.usuario_espacio)
        top_layout.addWidget( self.groupBox3)
        top_layout.addWidget( self.groupBox1)
        top_layout.addWidget( self.groupBox2)
        

        #-------posicionamiento widgets left frame ---------

        #left_layout.addWidget(self.groupBox_Archivo)
        

        #------ carga de layouts a sus respectivos frames -----

        #central_widget.setLayout(layout)

        # Establecer el layout en el frame superior
        top_frame.setLayout(top_layout)  

        # Establecer el layout en el frame izquierdo
        left_frame.setLayout(left_layout)

        # Asignar el layout al frame derecho
        right_frame.setLayout(layout)

        # Crear la barra de menú
        menubar = self.menuBar()

        # Menú de Mostrar
        list_mantto_menu = QMenu('Configuracion', self)
        #list_mantto_menu.addAction('Branches', self.listar_ramas)
        #list_mantto_menu.addAction('Commits', self.configuracion)
        menubar.addMenu(list_mantto_menu)

        # Menú Info
        list_info_menu = QMenu('Info', self)
        list_info_menu.addAction('Update by Nicolás Perea Santos')  # No hay comando asignado aquí
        menubar.addMenu(list_info_menu)
    
    def cell_was_clicked(self, row, column):
        if column == 2:  # Asumiendo que la columna "Cambios" es la columna 2
            ensamble = self.tabla.item(row, 0).text()
            familia = self.tabla.item(row, 1).text()  # Obtiene el valor de "Familia" de la fila correspondiente
            self.abrir_visualizador_tabla(row, familia, ensamble)  # Pasa el valor de familia como un argumento adicional

    
    def abrir_visualizador_tabla(self, row, familia, ensamble):
        self.controlador.current_familia = familia
        self.controlador.current_ensamble = ensamble
        self.ventana_tabla.show()  # Usar la instancia precreada
        self.controlador.show_changes()  # Actualizar los datos en la instancia precreada



    
    def registrar_cambios(self):
        # Obtener el repositorio seleccionado en el combo box
        selected_repo = self.repositorio_combobox.currentText()

        # Registrar los cambios en el repositorio seleccionado
        self.historial_manager.registrar_cambios(selected_repo)

    
    
    def obtener_ultimos_archivos_agregados(self):
        try:
            # Ejecuta el comando 'git log' para obtener el historial de los últimos commits
            resultado = subprocess.run(['git', 'log', '--name-only', '--pretty=format:"%an, %ar : %s"'], 
                                        capture_output=True, text=True, shell=True)

            # Divide la salida en líneas
            lineas = resultado.stdout.splitlines()

            # Inicializa una lista para almacenar los archivos añadidos
            archivos_anadidos = []

            # Extrae los archivos añadidos de los últimos 10 commits
            for linea in lineas:
                # Comprueba si la línea comienza con '"' para indicar que es un archivo
                if linea.startswith('"'):
                    # Obtiene el nombre del archivo
                    nombre_archivo = linea.strip('"')

                    # Obtiene el autor del commit
                    autor = linea.split(' ')[0]

                    # Añade el archivo a la lista
                    archivos_anadidos.append({
                        'nombre_archivo': nombre_archivo,
                        'autor': autor,
                        'fecha': linea.split(' ')[1]
                    })

            # Verifica si el archivo log no existe
            if not os.path.exists('historial_archivos.log'):
                # Crea el archivo log
                with open('historial_archivos.log', 'w') as archivo_log:
                    archivo_log.write('')

            # Añade los archivos añadidos al archivo de registro (log)
            with open('historial_archivos.log', 'a') as archivo_log:
                for archivo_anadido in archivos_anadidos:
                    archivo_log.write(f"{archivo_anadido['nombre_archivo']} - {archivo_anadido['autor']}\n")

            # Convierte la lista de diccionarios a una lista de cadenas de texto
            archivos_anadidos_texto = [f"{archivo['nombre_archivo']} - {archivo['autor']}" for archivo in archivos_anadidos]

            # Muestra los últimos archivos añadidos en la terminal
            self.textEditWidget1.setPlainText('\n'.join(archivos_anadidos_texto))
            print(archivos_anadidos_texto)
        except Exception as e:
            self.textEditWidget1.setPlainText(f"Error al obtener el historial de archivos: {str(e)}")

   

    def revertir_cambios(self):
        # Obtener el nombre del repositorio seleccionado del combobox
        repo_name = self.repositorio_combobox.currentText()
        #repo_name = self.familia
        
        # Construir la ruta completa al repositorio local
        #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"
        base_path = self.ruta_corregida_directory

        selected_repo_path = os.path.join(base_path, repo_name)

        # Inicializar el repositorio git usando la ruta completa
        repo = git.Repo(selected_repo_path)
        
        # Obtener el nombre de la rama y del commit seleccionados del combobox
        selected_branch = self.branch_combobox.currentText()
        selected_commit = self.commit_combobox.currentText()

        if not selected_commit or selected_commit == 'Seleccionar Commit':
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un commit para revertir.")
            return

        try:
            # Cambiar a la rama seleccionada
            repo.git.checkout(selected_branch)

            # Separar el hash del commit del texto del combobox
            commit_hash = [commit[0] for commit in self._commits if commit[1].strip() in selected_commit][0]

            # Intentar revertir el commit seleccionado
            try:
                repo.git.revert(commit_hash, no_edit=True)
            except git.GitCommandError:
                # Si hay un conflicto, restablecer forzadamente el estado del archivo al commit especificado en el combo box
                repo.git.reset(commit_hash, '--hard')
                
            # Establecer la rama remota correspondiente si no está establecida
            try:
                repo.git.push('--set-upstream', 'origin', selected_branch)
            except git.GitCommandError:
                # Esto puede fallar si ya está configurado, así que lo atrapamos y continuamos
                pass
            
            # Empujar los cambios a la rama local 
            repo.git.pull('--rebase')
            # Empujar los cambios al remoto
            repo.git.push()

            QMessageBox.information(self, "Revertir Cambios", f"El commit {selected_commit} se ha revertido completamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al revertir cambios: {str(e)}")



    def mostrar_cambios(self):
        # Obtener el nombre del repositorio seleccionado del combobox
        repo_name = self.repositorio_combobox.currentText()

        #repo_name = self.familia
        # Construir la ruta completa al repositorio local
        #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"

        base_path = self.ruta_corregida_directory
        selected_repo_path = os.path.join(base_path, repo_name)

        # Inicializar el repositorio git usando la ruta completa
        repo = git.Repo(selected_repo_path)

        # Obtener el estado del repositorio usando gitpython
        untracked_files = repo.untracked_files
        diff = repo.index.diff(None)
        added_files = [item.a_path for item in diff.iter_change_type('A')]
        modified_files = [item.a_path for item in diff.iter_change_type('M')]
        deleted_files = [item.a_path for item in diff.iter_change_type('D')]

        def format_file_path(file_path):
            parts = file_path.split('/')
            if len(parts) > 1:
                rama = parts[0]
                archivo = parts[-1]
                carpetas = parts[1:-1]
                carpeta_str = " -> ".join(carpetas)  # Concatenar los nombres de las carpetas con '->'
                return f"Rama: {rama}\nCarpetas: {carpeta_str}\nArchivo: {archivo}\n"
            else:
                return f"Raíz:\nArchivo: {parts[0]}\n"

        # Construir el mensaje de salida
        output = "Cambios en espera para confirmación:\n\n"
        sections = []

        if added_files:
            sections.append("Agregado:\n" + '\n'.join([format_file_path(f) for f in added_files]))
        if modified_files:
            sections.append("Modificado:\n" + '\n'.join([format_file_path(f) for f in modified_files]))
        if deleted_files:
            sections.append("Eliminado:\n" + '\n'.join([format_file_path(f) for f in deleted_files]))
        if untracked_files:
            sections.append("Archivos nuevos sin seguimiento:\n" + '\n'.join([format_file_path(f) for f in untracked_files]))

        output += '\n\n'.join(sections)

        if not sections:
            output = "No hay cambios para confirmar."

        self.cambios_output.setPlainText(output)






    def actualizar_vista(self):

        selected_branch = self.branch_combobox.currentText()

        # Obtener el nombre del repositorio seleccionado del combobox
        repo_name = self.repositorio_combobox.currentText()

        
        # Construir la ruta completa al repositorio local
        #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"
        base_path =self.ruta_corregida_directory

        selected_repo_path = os.path.join(base_path, repo_name)

        # Inicializar el repositorio git usando la ruta completa
        repo = git.Repo(selected_repo_path)

        repo.git.checkout(selected_branch)
        messagebox.showinfo('Revisando', f'Cambios con respecto a la rama: {selected_branch}')
        self.mostrar_cambios()
    
    def actualizar_vista_commit(self):
        # Obtener el nombre del repositorio seleccionado del combobox
        repo_name = self.repositorio_combobox.currentText()


        # Construir la ruta completa al repositorio local
        #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"
        base_path = self.ruta_corregida_directory

        selected_repo_path = os.path.join(base_path, repo_name)

        # Inicializar el repositorio git usando la ruta completa
        repo = git.Repo(selected_repo_path)
        
        # Obtener el nombre de la rama seleccionada del combobox
        selected_branch = self.branch_combobox.currentText()

        # Cambiar a la rama seleccionada
        repo.git.checkout(selected_branch)
        
        # Llamar a mostrar_commits para llenar el combo box con los commits de la rama seleccionada
        self.mostrar_commits()


# ...

    def mostrar_commits(self):
        try:
            selected_branch = self.branch_combobox.currentText()
            repo_name = self.repositorio_combobox.currentText()
    
            base_path = self.ruta_corregida_directory
            #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"
            selected_repo_path = os.path.join(base_path, repo_name)
            repo = git.Repo(selected_repo_path)

            repo.git.checkout(selected_branch)
            commits = [(commit.hexsha, commit.message, commit.author.name, commit.committed_datetime) for commit in reversed(list(repo.iter_commits(selected_branch)))]

            # Invierte la lista de commits para mostrarlos en orden descendente
            commits.reverse()
            
            self.commit_combobox.clear()
            self.commit_combobox.addItem('Seleccionar Commit')  # Opción inicial

            # Calcula el número total de commits en la rama
            total_commits = len(commits)

            # Recorre los commits y asigna versiones en orden descendente
            version = total_commits
            for commit_hash, commit_message, author_name, committed_datetime in commits:
                version_str = f'Version {version}.0.0'
                self.commit_combobox.addItem(f'{version_str} - {commit_message}')
                version -= 1

            # Guarda los commits como una variable de instancia
            self._commits = commits
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener commits: {str(e)}")

    def escribir_versiones_log(self, commits):
        """
        Escribe los detalles de las versiones en el archivo versiones.log.
        
        :param commits: Lista de commits que se escribirán en el archivo.
        """
        # Abre el archivo versiones.log en modo escritura (lo crea si no existe, o sobrescribe si ya existe)
        with open('versiones.log', 'w') as version_log:
            # Agregar encabezados al archivo versiones.log
            version_log.write("Versiones - Numero de Commit - Responsable - Fecha\n")

        # Calcula el número total de commits
        total_commits = len(commits)

        # Recorre los commits y asigna versiones en orden descendente
        version = total_commits
        for commit_hash, commit_message, author_name, committed_datetime in commits:
            version_str = f'Version {version}.0.0'
            # Agregar el commit al archivo versiones.log
            with open('versiones.log', 'a') as version_log:
                version_log.write(f'{version_str} - {commit_hash} - {self.username} - {committed_datetime}\n')
            version -= 1




    def mostrar_historial(self):
        try:
            with open('acciones.log', 'r') as archivo_log:
                historial = archivo_log.read()
                if historial.strip():  # Verifica si el historial no está vacío
                    historial_dialog = QDialog(self)
                    historial_dialog.setWindowTitle('Historial de Acciones')
                    historial_dialog.setGeometry(200, 200, 600, 400)

                    layout = QVBoxLayout()

                    historial_text = QPlainTextEdit()
                    historial_text.setReadOnly(True)
                    historial_text.setPlainText(historial)

                    layout.addWidget(historial_text)
                    historial_dialog.setLayout(layout)
                    historial_dialog.exec_()
                else:
                    print("El archivo de historial está vacío.")
        except FileNotFoundError:
            # Si el archivo no existe, muestra un mensaje
            print("El archivo de historial aún no ha sido creado.")

    def hacer_commit_y_push(self):
        mensaje_commit, ok = QInputDialog.getText(self, 'Mensaje', 'Por favor, ingresa el motivo del cambio a enviar:')
        if ok:
            # Obtener la ruta completa al repositorio local
            repo_name = self.repositorio_combobox.currentText()
            base_path = self.ruta_corregida_directory
            #base_path = "C:\\Users\\gdlniper\\Desktop\\Nicolas Perea Santos\\AplicacionesNicolas\\Programa_2\\Repositorio Github-APP\\programas"
            selected_repo_path = os.path.join(base_path, repo_name)
            
            # Pasar la ruta local al método git_add_commit_push
            self.git_add_commit_push(mensaje_commit, selected_repo_path)
        

class FileDialogWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Seleccionar archivos")
        self['bg'] = '#FFFFFF'
        self.master = master
        self.container = tk.Frame(self)
        self.container['bg'] = "#FFFFFF"
        self.container.pack(fill='both', expand=1)

        self.title("Configuracion")

        # Crear un nuevo marco para user_label y self.json_path
        self.json_frame = tk.Frame(self.container)
        self.json_frame['bg'] = "#FFFFFF"

        self.json_label = tk.Label(self.json_frame, text='Json DB', font=('Segoe UI', 15), fg="#000000", bg="#FFFFFF")     
        self.json_path_entry = tk.Entry(self.json_frame, font=('Segoe UI', 12), width=30)
        self.json_path_button = tk.Button(self.json_frame, text="Buscar", command=self.select_json_path)
 
        self.json_label.pack(side=tk.LEFT, padx=(0, 1))  # Agregar un espacio de 5 píxeles a la derecha
        self.json_path_entry.pack(side=tk.LEFT, padx=(0, 1))
        self.json_path_button.pack(side=tk.RIGHT, padx=(25, 0))
        self.json_frame.pack()  # Empaquetar el nuevo marco

        # Crear un nuevo marco para user_label y self.json_path
        self.org_frame = tk.Frame(self.container)
        self.org_frame['bg'] = "#FFFFFF"

        self.org_label = tk.Label(self.org_frame, text='Organización', font=('Segoe UI', 15), fg="#000000", bg="#FFFFFF") 
        self.directory_path_entry = tk.Entry(self.org_frame, font=('Segoe UI', 12), width=30)
        self.directory_path_button = tk.Button(self.org_frame, text="Buscar", command=self.select_directory_path)
        self.org_label.pack(side=tk.LEFT, padx=(0, 1))
        self.directory_path_entry.pack(side=tk.LEFT, padx=(0, 1))
        self.directory_path_button.pack(side=tk.RIGHT, padx=(25,0))
        self.org_frame.pack()

        # Crear un nuevo marco para user_label y self.json_path
        self.salir_frame = tk.Frame(self.container)
        self.salir_frame['bg'] = "#FFFFFF"

        # Botón de guardar
        self.save_button = tk.Button(self.salir_frame, text="Guardar", command=self.save)
        self.save_button.pack(side=tk.LEFT, padx=(0, 1))

        self.close_button = tk.Button(self.salir_frame, text="salir", command=self.salir)
        self.close_button.pack(side=tk.RIGHT, padx=(25,0))
        self.salir_frame.pack()

        # Cargar las rutas desde el archivo de configuración
        self.load_paths()

    def save(self):
        # Obtener las rutas seleccionadas
        json_path = self.json_path_entry.get()
        directory_path = self.directory_path_entry.get()

        # Guardar las rutas en el archivo de configuración
        config = configparser.ConfigParser()
        config['Paths'] = {
            'JsonPath': json_path,
            'DirectoryPath': directory_path
        }
        with open('config_rutas.ini', 'w') as configfile:
            config.write(configfile)

        return json_path, directory_path
    
    def salir(self):
        json_path, directory_path = self.save()
        self.master.update_paths(json_path, directory_path)  # Actualiza las rutas en la instancia actual de LoginWindow_supervisor
        self.destroy()
        

    def select_json_path(self):
        directory = filedialog.askdirectory()
        self.json_path_entry.delete(0, tk.END)  # Limpiar el campo de entrada de texto
        self.json_path_entry.insert(tk.END, directory)  # Insertar la ruta seleccionada en el campo de entrada de texto

    def select_directory_path(self):
        directory = filedialog.askdirectory()
        self.directory_path_entry.delete(0, tk.END)  # Limpiar el campo de entrada de texto
        self.directory_path_entry.insert(tk.END, directory)  # Insertar la ruta seleccionada en el campo de entrada de texto

    def load_paths(self):
        # Cargar las rutas desde el archivo de configuración
        config = configparser.ConfigParser()
        config.read('config_rutas.ini')
        if 'Paths' in config:
            paths = config['Paths']
            if 'JsonPath' in paths:
                self.json_path_entry.insert(tk.END, paths['JsonPath'])
            if 'DirectoryPath' in paths:
                self.directory_path_entry.insert(tk.END, paths['DirectoryPath'])
                                        


class Controlador:
    def __init__(self,selected_org,username,json_path,directory_path):
        # Manejo del token
        self.config_manager = ConfigRead()
        self.current_familia = None
        self.current_ensamble = None
        if not self.config_manager.get_token():
            token = input("Introduce tu token de GitHub: ")
            self.config_manager.set_token(token)
        
        self.git_token = self.config_manager.get_token()

        self.json_path = json_path
        self.directory_path = directory_path


        print("clase controlador sus variables que se paso son:")
        print( self.json_path)
        print(self.directory_path)

        rutas_originales_json= self.json_path
        rutas_originales_directory=self.directory_path

        #La ruta corregida es la ruta del repositorio que se va a utilizar

        #ruta_corregida_json = rutas_originales_json.replace("/", "\\")
        ruta_corregida_json = rutas_originales_json.replace("/", "\\") + "\\\\project_info.json"
        ruta_corregida_directory = rutas_originales_directory.replace("/", "\\")

 
        print("las rutas corregidas son")
        print(ruta_corregida_json)
        print(ruta_corregida_directory)

        #instancia de la clase ProjectInfoManager
        self.project_info_manager = ProjectInfoManager(ruta_corregida_json, ruta_corregida_directory)
        self.project_info_manager.update_BU_and_Modelo()
        
        #instancia de la clase VisualizadorTabla
        self.visualizador_tabla = VisualizadorTabla(self)  # Pasar el controlador a la vista

        #Instancia de la clase Gitviewer
        self.git_viewer = GitViewer(selected_org,username,ruta_corregida_directory,controlador=self)  # Aquí asumo que pasas el controlador como argumento a GitViewer
        self.git_viewer.show()

        #Instancia de la clase Historialmanager

        self.historialmanager = HistorialManager()
        self.historialmanager.obtener_repositorios(ruta_corregida_directory,selected_org)
        #self.historialmanager.registrar_cambios_de_todos_los_repositorios(ruta_corregida_directory)

    def sync_files_with_master(self):
        self.git_viewer.sync_files_with_master()

    def show_changes(self):
        self.git_viewer.show_changes()


class LoginWindow_supervisor(tk.Frame):
    def __init__(self, master, json_path=None, directory_path=None):
        super().__init__(master)
        self.master = master
        self.json_path = json_path
        self.directory_path = directory_path

        self.load_paths()  # Cargar las rutas desde el archivo de configuración

        #print(self.json_path)
        #print(self.directory_path)

        #self.master.geometry("400x325")
        self['bg'] = '#FFFFFF'
        self.container = tk.Frame(self)
        self.container['bg'] = "#FFFFFF"
        self.container.pack(fill='both', expand=1)
        self._create_widgets()
        self._place_widgets()
    
    @classmethod #de esta manera lo defines como metodo de clase
    def resource_path(cls, relative_path):
        

        # Get absolute path to resource, works for dev and for PyInstaller 
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def load_paths(self):
        # Cargar las rutas desde el archivo de configuración
        config = configparser.ConfigParser()
        config.read('config_rutas.ini')
        if 'Paths' in config:
            paths = config['Paths']
            if 'JsonPath' in paths:
                self.json_path = paths['JsonPath']
            if 'DirectoryPath' in paths:
                self.directory_path = paths['DirectoryPath']

    def _create_widgets(self):
        self.user_label = tk.Label(self.container, text='User', font=('Segoe UI', 15), fg="#000000", bg="#FFFFFF")
        
        # Crear un nuevo marco para contener user_entry y login_button_config
        self.user_frame = tk.Frame(self.container)
        self.user_frame['bg'] = "#FFFFFF"

        self.user_entry = tk.Entry(
            self.user_frame,
            width=30,
            bg="#FFFFFF",
            fg="#000000",
            bd=0,
            highlightthickness=1,
            highlightbackground="#009ADD",
            font=('Segoe UI Semilight', 12),
            justify='center',
        )
        self.pass_label = tk.Label(self.container, text="Password", font=('Segoe UI', 15), fg="#000000", bg="#FFFFFF")
        self.pass_entry = tk.Entry(
            self.container,
            width=30,
            bg="#FFFFFF",
            fg="#000000",
            bd=0,
            highlightthickness=1,
            highlightbackground="#009ADD",
            font=('Segoe UI Semilight', 12),
            justify='center',
            show="*",
        )
        self.login_button = tk.Button(
            self.container,
            text='Login',
            font=('Segoe UI', 15),
            fg="#FFFFFF",
            bd=0,
            bg="#005486",
            highlightthickness=0,
            highlightbackground="#FFFFFF",
            activebackground="#009add",
            width=30,
            command=self.log_user_in
        )
        

        #--------imagen usuario ------------

        imagen_path = self.resource_path('imagenes/images.jpg')
        image = Image.open(imagen_path)
        image = image.resize((30, 30))
        pixmap = ImageTk.PhotoImage(image)
 
        self.login_button_config = tk.Button(
            self.user_frame,
            text='Login sin validar',
            font=('Segoe UI', 15),
            fg="#FFFFFF",
            bd=0,
            bg="#005486",
            highlightthickness=0,
            highlightbackground="#FFFFFF",
            activebackground="#009add",
            width=30,
            image=pixmap,
            command=self.open_file_dialog
            )

        self.login_button_sin_loguearse = tk.Button(
            self.container,
            text='sin validar',
            font=('Segoe UI', 15),
            fg="#FFFFFF",
            bd=0,
            bg="#005486",
            highlightthickness=0,
            highlightbackground="#FFFFFF",
            activebackground="#009add",
            width=30,
            command=self.loguearse_sin_validar
        )

            
        self.login_button_config.image = pixmap  # Guardar una referencia a la imagen para evitar que se elimine por el recolector de basura

        self.combo_label = tk.Label(self.container, text="Familia", font=('Segoe UI', 15), fg="#000000", bg="#FFFFFF")

        self.combo_box = ttk.Combobox(self.container)

        # Obtener las organizaciones
        github_manager = GitHubManager()
        github = GitHubOrganizations(github_manager)
        organizations = github.get_organizations()

        # Configurar las opciones del combobox con los nombres de las organizaciones
        self.combo_box['values'] = [org["login"] for org in organizations]
    
    def update_paths(self, json_path, directory_path):
        self.json_path = json_path
        self.directory_path = directory_path
        print("Rutas actualizadas: ", self.json_path, self.directory_path)

    def open_file_dialog(self):
        self.file_dialog_window = FileDialogWindow(self)


    def _place_widgets(self):
        self.user_label.pack()
        self.user_frame.pack(padx=(55, 0))  # Mover el marco 5 píxeles a la derecha  # Empaquetar el nuevo marco
        self.user_entry.pack(side=tk.LEFT, padx=(0, 1))  # Agregar un espacio de 5 píxeles a la derecha
        self.login_button_config.pack(side=tk.RIGHT, padx=(25, 0))  # Agregar un espacio de 5 píxeles a la izquierda
        self.pass_label.pack()
        self.pass_entry.pack()
        self.combo_label.pack()
        self.combo_box.pack()
        self.login_button.pack(pady=10)
        self.login_button_sin_loguearse.pack(pady=10)

    def log_user_in(self):
        global login_successful
        user = self.user_entry.get()
        password = self.pass_entry.get()
        domain = "americas.ad.flextronics.com"
        server = Server('10.10.28.70', use_ssl=True, get_info=ALL)
        full_user = user + '@' + domain
        try:
            conn = Connection(server, full_user, password, auto_bind=True)
        except Exception as e:
            messagebox.showerror(title='Error', message=str(e))
        else:
            conn.search(search_base='ou=users,ou=gdl,ou=mx,dc=americas,dc=ad,dc=flextronics,dc=com',
                         search_filter=f"""(&(objectClass=user)(sAMAccountname={user}))""",
                         search_scope=SUBTREE,
                         attributes=['displayname', 'title', 'sAMAccountname', 'employeeNumber', 'mail', 'personaltitle'])
            for entry in conn.response:
                attributes = entry['attributes']
            if attributes.get('title') in ['Debug Technician', 'Student'] or attributes.get('employeeNumber') == 'WD911888':
                login_successful = True
                self.master.destroy()
                self.show_next_station(user)

    def show_next_station(self, username):
        if login_successful:
            app = QApplication(sys.argv)
            file_dialog_window = FileDialogWindow(self)
            controlador = Controlador(self.combo_box.get(),username,self.json_path,self.directory_path)
            
            #window = GitViewer(username=username)
            #window.show()
            sys.exit(app.exec_())

    def loguearse_sin_validar(self, username=None):
            
            app = QApplication(sys.argv)
            #file_dialog_window = FileDialogWindow(self)
            print("en el metodo loguearse sin las variables son:")
            print(self.json_path)
            print(self.directory_path)
            controlador = Controlador(self.combo_box.get(),username,self.json_path,self.directory_path)
            self.master.destroy()
            # Crear una instancia de la clase CreateRepoDialog y pasar el valor seleccionado del combobox
            #create_dialog = CreateRepoDialog(self.combo_box.get(), self.github_manager)
            #create_dialog = CreateRepoDialog(self.combo_box.get())
            #print(self.combo_box.get())
            #window = GitViewer(username=username)
            #window.show()
            sys.exit(app.exec_())
            
            
            

def main():
    #comentar para deshabilitar login
    root = tk.Tk()
    root.title("Aplicación")
    login_window = LoginWindow_supervisor(root)
    login_window.pack(side='left', fill='both', expand=1)
    root.mainloop()

     #inicializar primera vez el token para guardarlo en el config.ini---------

    #config_manager = ConfigRead()
    #config_manager.set_token('colocar el token')

    #-------------apartir de aqui- inicio directo sin login ------

    #descomentar para iniciar directamente

    #app = QApplication(sys.argv)

    #window = GitViewer()
    #window.show()
    
    #controlador = Controlador(username=None)
    #sys.exit(app.exec_())


if __name__ == '__main__':
    main()




