import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
import pymysql
from pymysql import OperationalError, IntegrityError, MySQLError
pymysql.install_as_MySQLdb()
import csv
from datetime import datetime
import os
from PIL import Image

# Variable global para los intentos restantes
intentos_restantes = 3

def validar_login():
    global intentos_restantes  # Usamos la variable global para contar intentos
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Credenciales predefinidas
    usuario_correcto = "admin"
    contrasena_correcta = "1234"

    if usuario == usuario_correcto and contrasena == contrasena_correcta:
        messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
        ventana_login.destroy()  # Cierra la ventana de inicio de sesión
        iniciar_aplicacion()     # Inicia la aplicación principal
    else:
        intentos_restantes -= 1  # Reduce el contador de intentos
        if intentos_restantes > 0:
            messagebox.showerror("Error", f"Usuario o contraseña incorrectos. Te quedan {intentos_restantes} intentos.")
            entry_usuario.delete(0, tk.END)  # Limpia la caja de texto de usuario
            entry_contrasena.delete(0, tk.END)  # Limpia la caja de texto de contraseña
            

        else:
            messagebox.showerror("Error", "Demasiados intentos fallidos. El programa se cerrará.")
            ventana_login.destroy()  # Cierra la ventana de inicio de sesión y termina el programa
            exit()  # Asegura que el programa se detenga por completo

def cerrar_login():
    """Cierra el programa si el usuario presiona la X del login."""
    if messagebox.askyesno("Salir", "¿Estás seguro de que quieres cerrar la aplicación?"):
        ventana_login.destroy()
        exit()  # Detiene el programa por completo

def mostrar_login():
    global ventana_login, entry_usuario, entry_contrasena

    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.state("zoomed")
    ventana_login.configure(bg="#ADD8E6")

        # Frame principal para centrar los widgets
    frame_central = tk.Frame(ventana_login, bg="#ADD8E6")
  # Colocar el frame central sobre el Canvas
    frame_central.pack(expand=True, pady=50)

    # Configurar el evento de cierre de ventana
    ventana_login.protocol("WM_DELETE_WINDOW", cerrar_login)

        # Título principal
    ttk.Label(frame_central, text="Detección de Cáncer de Piel", font=("Helvetica", 20, "bold"), foreground="#2d6187",background="#ADD8E6").pack(pady=10)
    ttk.Label(frame_central, text="Por favor, inicia sesión para continuar", font=("Helvetica", 12), foreground="#555",background="#ADD8E6").pack(pady=5)

    # Logo o imagen decorativa
    try:
        # Obtener la ruta absoluta del script actual
        directorio_base = os.path.dirname(os.path.abspath(__file__))

        # Construir la ruta a la imagen en la carpeta ImagenFronted
        ruta_imagen = os.path.join(directorio_base, "ImagenFronted", "2.jpg")
        img_logo = Image.open(ruta_imagen)
        img_logo = img_logo.resize((210, 210), Image.LANCZOS)
        img_logo = ImageTk.PhotoImage(img_logo)
        logo_label = ttk.Label(frame_central, image=img_logo, background="#ADD8E6")
        logo_label.image = img_logo
        logo_label.pack(pady=12)
    except Exception as e:
        print(f"Error cargando la imagen: {e}")

    # Etiqueta y caja de entrada "Usuario"
    ttk.Label(ventana_login, font=("Helvetica", 19), background="#ADD8E6").pack(pady=10)
    entry_usuario = ttk.Entry(frame_central, font=("Helvetica", 14), width=30, foreground="grey")
    entry_usuario.insert(0, "Usuario")
    entry_usuario.bind("<FocusIn>", lambda event: (entry_usuario.delete(0, tk.END), entry_usuario.config(foreground="black")) if entry_usuario.get() == "Usuario" else None)
    entry_usuario.bind("<FocusOut>", lambda event: (entry_usuario.insert(0, "Usuario"), entry_usuario.config(foreground="grey")) if entry_usuario.get() == "" else None)
    entry_usuario.pack(pady=10)

    # Etiqueta y caja de entrada "Contraseña"
    ttk.Label(ventana_login, font=("Helvetica", 2), background="#ADD8E6").pack(pady=10)
    entry_contrasena = ttk.Entry(frame_central, font=("Helvetica", 14), width=30, foreground="grey", show="")
    entry_contrasena.insert(0, "Contraseña")
    entry_contrasena.bind("<FocusIn>", lambda event: (entry_contrasena.delete(0, tk.END), entry_contrasena.config(foreground="black", show="*")) if entry_contrasena.get() == "Contraseña" else None)
    entry_contrasena.bind("<FocusOut>", lambda event: (entry_contrasena.insert(0, "Contraseña"), entry_contrasena.config(foreground="grey", show="")) if entry_contrasena.get() == "" else None)
    entry_contrasena.pack(pady=10)

    btn_login = tk.Button(frame_central, text="Iniciar Sesión", 
                      command=validar_login, 
                      bg="#1E90FF",  # Color azul (DodgerBlue)
                      fg="white",    # Color del texto en blanco
                      font=("Helvetica", 15, "bold"), 
                      activebackground="#104E8B",  # Color al presionar
                      activeforeground="white")
    btn_login.pack(pady=20)


    ventana_login.mainloop()

def iniciar_aplicacion():
    root.mainloop()

# Llamada inicial para mostrar la ventana de inicio de sesión
mostrar_login()


# Cargar el modelo automáticamente al iniciar la aplicación
def cargar_modelo():
    global model
    try:
        # Obtener la ruta absoluta del directorio actual del script
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Construir la ruta al modelo en la carpeta "Model"
        ruta_modelo = os.path.join(directorio_base, "Model", "modelo_cancer_piel.keras")

        # Cargar el modelo de Keras
        #model = tf.keras.models.load_model(r'C:\Users\elias\Downloads\CANCER DE PIEL\Grupo3_IA_CancerPiel\Model\modelo_cancer_piel.keras')
        model = tf.keras.models.load_model(ruta_modelo)
        messagebox.showinfo("Información", "Modelo cargado exitosamente")  
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el modelo: {str(e)}")
        root.quit()
        
        

def listar_registros():
    try:
        db = pymysql.connect(host="localhost", user="root", passwd="", db="predicciones")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM predicciones")
        registros = cursor.fetchall()

        # Limpiar la tabla antes de listar registros
        for row in tree.get_children():
            tree.delete(row)

        # Insertar los registros en la tabla
    # Insertar datos en la tabla con filas alternas
        for index, registro in enumerate(registros):
            if index % 2 == 0:  # Filas pares
                tree.insert("", "end", values=registro, tags=("evenrow",))
            else:               # Filas impares
                tree.insert("", "end", values=registro, tags=("oddrow",))

        # Configurar colores de las filas alternas
        tree.tag_configure("evenrow", background="white")       # Fondo blanco para filas pares
        tree.tag_configure("oddrow", background="#F0F8FF")      # Fondo celeste claro para filas impares


        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron listar los registros: {str(e)}")


def eliminar_registro():
    try:
        # Solicitar el DNI del registro a eliminar
        dni_registro = simpledialog.askstring("Eliminar Registro", "Ingrese el DNI del registro a eliminar:")
        if not dni_registro:  # Verificar si se ingresó algo
            return

        # Conexión a la base de datos
        db = pymysql.connect(host="localhost", user="root", passwd="", db="predicciones")
        cursor = db.cursor()

        # Ejecutar la eliminación por DNI
        cursor.execute("DELETE FROM predicciones WHERE dni = %s", (dni_registro,))
        db.commit()

        # Verificar si se eliminó algún registro
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", f"Registro con DNI {dni_registro} eliminado exitosamente")
        else:
            messagebox.showwarning("Advertencia", f"No se encontró ningún registro con DNI {dni_registro}")

        # Refrescar la tabla después de eliminar
        listar_registros()

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el registro: {str(e)}")



from tkinter import simpledialog

def actualizar_registro():
    try:
        # Conectar a la base de datos
        db = pymysql.connect(host="localhost", user="root", passwd="", db="predicciones")
        cursor = db.cursor()

        # Actualizar un campo genérico si hubo cambios en la tabla
        # Aquí hacemos una actualización en todos los registros existentes como prueba
        cursor.execute("""
            UPDATE predicciones 
            SET prediccion = prediccion  -- Simula una actualización
        """)
        db.commit()

        # Verificar si hubo algún cambio (solo cuenta cuando se insertó o eliminó algo)
        if cursor.rowcount >= 0:
            messagebox.showinfo("Éxito", "Actualizado exitosamente")
        else:
            messagebox.showwarning("Advertencia", "No se detectaron cambios para actualizar")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar la tabla: {str(e)}")
    finally:
        # Cerrar la conexión a la base de datos
        if cursor:
            cursor.close()
        if db:
            db.close()

        
# Función para preprocesar la imagen
def preprocesar_imagen(imagen_path):
    imagen = tf.keras.preprocessing.image.load_img(imagen_path, target_size=(128, 128))
    imagen_array = tf.keras.preprocessing.image.img_to_array(imagen)
    imagen_array = np.expand_dims(imagen_array, axis=0)
    imagen_array /= 255.0
    return imagen_array

def guardar_en_db(nombre, dni, fecha, prediccion, imagen_path):
    try:
        # Establecer la conexión a la base de datos
        db = pymysql.connect(host="localhost", user="root", passwd="", db="predicciones")
        cursor = db.cursor()
        
        # Comando SQL para insertar los datos en la tabla 'predicciones'
        sql = "INSERT INTO predicciones (nombre, dni, fecha, prediccion, imagen_path) VALUES (%s, %s, %s, %s, %s)"
        
        # Ejecutar el comando SQL con los valores correspondientes
        cursor.execute(sql, (nombre, dni, fecha, prediccion, imagen_path))
        
        # Confirmar los cambios en la base de datos
        db.commit()
        
    except OperationalError as e:
        # Error relacionado con la conexión a la base de datos
        messagebox.showerror("Error", f"Error de conexión a la base de datos: {str(e)}")
    except IntegrityError as e:
        # Error relacionado con la integridad de los datos
        messagebox.showerror("Error", f"Error de integridad de los datos: {str(e)}")
    except MySQLError as e:
        # Otros errores de pymysql
        messagebox.showerror("Error", f"Error al guardar en la base de datos: {str(e)}")
    except Exception as e:
        # Otros errores generales
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        if cursor:
            cursor.close()
        if db:
            db.close()

# Función para seleccionar la imagen
def seleccionar_imagen():
    global imagen_path, imagen_tk
    try:
        imagen_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
        if imagen_path:
            imagen = Image.open(imagen_path)
            imagen = imagen.resize((250, 250), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)

            label_imagen.config(image=imagen_tk)
            label_imagen.image = imagen_tk
            messagebox.showinfo("Información", "Imagen seleccionada correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al cargar la imagen: {str(e)}")
# Función para hacer la predicción
def predecir():
    nombre = entry_nombre.get()
    dni = entry_dni.get()
    fecha = entry_fecha.get()
    
    if not nombre or not dni or not fecha:
        resultado_label.config(text="Error: Todos los campos son obligatorios", foreground="red", font=("Helvetica", 12, "bold"))
        return
    
    if not imagen_path:
        resultado_label.config(text="Error: Debe seleccionar una imagen", foreground="red", font=("Helvetica", 12, "bold"))
        return
    
    imagen_array = preprocesar_imagen(imagen_path)
    prediccion = model.predict(imagen_array)
    porcentaje = prediccion[0][0] * 100
    if prediccion[0][0] > 0.5:
        resultado = f"La imagen tiene una probabilidad de {prediccion[0][0] * 100:.2f}% de ser maligna."
    else:
        resultado = f"La imagen tiene una probabilidad de {(1 - prediccion[0][0]) * 100:.2f}% de ser benigna."

    # Mostrar resultado en un cuadro en la interfaz
    resultado_label.config(text=resultado, foreground="black",background="#E6F7FF", font=("Helvetica", 12, "bold"))
    
    # Guardar en base de datos
    guardar_en_db(nombre, dni, fecha, resultado, imagen_path)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Predicción de Cáncer de Piel")
root.state("zoomed")  # Maximiza la ventana automáticamente
root.configure(bg="#E6F7FF")  # Celeste claro
# Franja superior
franja_superior = tk.Frame(root, bg="#2d6187", height=70)  # Fondo azul oscuro, altura fija
franja_superior.place(relx=0, rely=0, relwidth=1.0)  # Ocupar todo el ancho en la parte superior

# Título centrado dentro de la franja
titulo_label = tk.Label(franja_superior, text="Gestión de Predicciones de Cáncer de Piel", 
                        font=("Helvetica", 20, "bold"), 
                        fg="white", bg="#2d6187")  # Texto blanco y fondo igual al de la franja
titulo_label.place(relx=0.5, rely=0.5, anchor="center")  # Centrado en la franja


# Usar ttk para widgets más modernos y bien proporcionados
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 14, "bold"), foreground="black")
style.configure("TButton", font=("Helvetica", 14, "bold"), foreground="black", background="gray")
style.configure("TEntry", font=("Helvetica", 14))
style.configure("TFrame", background="lightgray")
# Configurar estilo para los botones
style.configure("Custom.TButton", 
                font=("Helvetica", 14, "bold"), 
                background="#005499",  # Azul intenso
                foreground="white",    # Letras blancas
                borderwidth=2)


style.map("Custom.TButton", 
          background=[("active", "#3399FF")],  # Azul más claro al pasar el mouse
          foreground=[("active", "white")])



# Widgets colocados con place() para posicionarlos libremente
# Nombre Completo
ttk.Label(root, text="Nombre Completo",background="#E6F7FF").place(x=50, y=100)
entry_nombre = ttk.Entry(root, width=40)
entry_nombre.place(x=50, y=140)

# DNI
ttk.Label(root, text="DNI",background="#E6F7FF").place(x=320, y=100)
entry_dni = ttk.Entry(root, width=40)
entry_dni.place(x=320, y=140)

# Fecha de la Imagen
ttk.Label(root, text="Fecha de la Imagen",background="#E6F7FF").place(x=590, y=100)
entry_fecha = DateEntry(root, date_pattern='yyyy-mm-dd', width=35)
entry_fecha.place(x=590, y=140)

# Botón para seleccionar la imagen
# Función para cambiar el color al pasar el mouse
def on_enter(e):
    e.widget.config(bg="#3399FF")  # Azul más claro

def on_leave(e):
    e.widget.config(bg="#005499")  # Azul intenso

# Botón con color azul y letras blancas
btn_seleccionar_imagen = tk.Button(root, text="Seleccionar Imagen", 
                                   font=("Helvetica", 14, "bold"), 
                                   bg="#005499",        # Azul intenso
                                   fg="white",          # Letras blancas
                                   activebackground="#3399FF",  # Azul más claro al hacer clic
                                   activeforeground="white",    # Letras blancas al clic
                                   borderwidth=2, relief="raised",
                                   command=seleccionar_imagen)

# Eventos para efecto hover
btn_seleccionar_imagen.bind("<Enter>", on_enter)  # Mouse entra
btn_seleccionar_imagen.bind("<Leave>", on_leave)  # Mouse sale
btn_seleccionar_imagen.place(x=50, y=195)  # Posición original

# Botón para predecir (Debajo de la imagen)
btn_predecir = tk.Button(root, text="Predecir", 
                         font=("Helvetica", 14, "bold"), 
                         bg="#005499", fg="white", 
                         activebackground="#3399FF", activeforeground="white", 
                         borderwidth=2, relief="raised",
                         command=predecir)
btn_predecir.bind("<Enter>", on_enter)
btn_predecir.bind("<Leave>", on_leave)
btn_predecir.place(x=50, y=250)

def limpiarImagen():
    global imagen_path, imagen_tk
    # Verificar si la imagen está cargada
    if imagen_tk:
        print("Limpiando la imagen...")  # Mensaje de depuración
        # Volver al color base de la interfaz (celeste claro)
        label_imagen.config(image=None, background="#E6F7FF")  # Eliminar imagen y cambiar el fondo a celeste claro
        imagen_tk = None  # Liberar la referencia de la imagen
    else:
        print("No hay imagen cargada para limpiar.")  # Mensaje de depuración

    # Limpiar el resultado de la predicción
    resultado_label.config(text="")  # Eliminar el texto de predicción

# Botón "Nuevo Registro"
btn_nuevo = tk.Button(root, text="Nuevo Registro",
                      font=("Helvetica", 14, "bold"),
                      bg="#005499", fg="white",
                      activebackground="#3399FF", activeforeground="white",
                      borderwidth=2, relief="raised",
                      command=limpiarImagen)
btn_nuevo.bind("<Enter>", on_enter)
btn_nuevo.bind("<Leave>", on_leave)
btn_nuevo.place(x=50, y=450)

# Botón para listar registros
btn_listar = tk.Button(root, text="Listar Registros", 
                       font=("Helvetica", 14, "bold"), 
                       bg="#005499", fg="white", 
                       activebackground="#3399FF", activeforeground="white", 
                       borderwidth=2, relief="raised",
                       command=listar_registros)
btn_listar.bind("<Enter>", on_enter)
btn_listar.bind("<Leave>", on_leave)
btn_listar.place(x=50, y=500)

# Botón para eliminar registros
btn_eliminar = tk.Button(root, text="Eliminar Registro", 
                         font=("Helvetica", 14, "bold"), 
                         bg="#005499", fg="white", 
                         activebackground="#3399FF", activeforeground="white", 
                         borderwidth=2, relief="raised",
                         command=eliminar_registro)
btn_eliminar.bind("<Enter>", on_enter)
btn_eliminar.bind("<Leave>", on_leave)
btn_eliminar.place(x=50, y=550)

# Botón para actualizar registros
btn_actualizar = tk.Button(root, text="Actualizar Registro", 
                           font=("Helvetica", 14, "bold"), 
                           bg="#005499", fg="white", 
                           activebackground="#3399FF", activeforeground="white", 
                           borderwidth=2, relief="raised",
                           command=actualizar_registro)
btn_actualizar.bind("<Enter>", on_enter)
btn_actualizar.bind("<Leave>", on_leave)
btn_actualizar.place(x=50, y=600)

# Estilo para el Treeview
style.configure("Treeview", 
                background="white", 
                fieldbackground="white", 
                rowheight=25,  # Altura de las filas
                borderwidth=1)

                
style.configure("Treeview.Heading", 
                background="#B0C4DE",  # Fondo azul claro en encabezados
                foreground="black",    # Texto negro
                font=("Helvetica", 12, "bold"))

# Filas alternas (colores de fondo para las filas)
style.map("Treeview", 
          background=[("selected", "#3399FF")],  # Color al seleccionar una fila
          foreground=[("selected", "white")])   # Letras blancas al seleccionar


# Crear la tabla (Treeview) para mostrar registros
tree = ttk.Treeview(root, columns=("ID", "Nombre", "DNI", "Fecha", "Predicción"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("DNI", text="DNI")
tree.heading("Fecha", text="Fecha")
tree.heading("Predicción", text="Predicción")

# Configuración de tamaño de columnas
tree.column("ID", width=50, anchor="center")
tree.column("Nombre", width=150, anchor="center")
tree.column("DNI", width=100, anchor="center")
tree.column("Fecha", width=100, anchor="center")
tree.column("Predicción", width=300, anchor="center")

# Colocar la tabla en la interfaz principal
tree.place(x=320, y=460, width=1000, height=300)
# Logo en la parte superior derecha
try:
    # Obtener la ruta absoluta del script actual
    directorio_base = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta a la imagen en la carpeta ImagenFronted
    ruta_imagen = os.path.join(directorio_base, "ImagenFronted", "1.jpg")
    img_logo = Image.open(ruta_imagen)
    img_logo = img_logo.resize((90, 90), Image.LANCZOS)  # Tamaño del logo (ajústalo si es necesario)
    img_logo_tk = ImageTk.PhotoImage(img_logo)
    logo_label = ttk.Label(root, image=img_logo_tk, background="#E6F7FF")  # Fondo celeste claro
    logo_label.image = img_logo_tk  # Evita que la imagen sea eliminada por el garbage collector
    logo_label.place(x=1315, y=79)  # Coordenadas para colocar el logo
except Exception as e:
    print(f"Error al cargar el logo: {e}")
# Texto descriptivo debajo del logo
texto_descriptivo = ttk.Label(root, text="Detección Asistida - IA Médica", 
                              font=("Helvetica", 12, "italic"), foreground="#555555",background="#E6F7FF")
texto_descriptivo.place(x=1250, y=185)  # Ajusta las coordenadas según la posición del logo


# Label para mostrar la imagen (mantén su posición actual)
label_imagen = ttk.Label(root)
label_imagen.place(x=320, y=195)  # Coordenada y ajustada correctamente

# Cargar el modelo al iniciar la aplicación
cargar_modelo()
# Label para mostrar el resultado de la predicción
resultado_label = ttk.Label(root, text="", font=("Helvetica", 12), foreground="black")
resultado_label.place(x=590, y=210)  # Ajusta x, y según dónde quieras el resultado

# Ejecutar la aplicación
root.mainloop()

