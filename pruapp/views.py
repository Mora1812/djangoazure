from django.shortcuts import render, redirect, get_object_or_404
from .models import Practica
from django.http import HttpResponse
# Create your views here.
def saludo(request):
    return HttpResponse("Hola mundo")

def despedida(request):
    return HttpResponse("Hasta luego")

def anime(request):
    return render(request, "./1/anime.html")
def mundo(request):
    return render(request, "./plantilla.html")

# =====================================================================
# VISTA DE LOGIN
# Esta función valida las credenciales del usuario contra la base de datos
# Si son correctas, guarda la sesión y redirige a la lista de usuarios
# =====================================================================
def login(request):
    if request.method == "POST":  # Si el usuario envió el formulario
        usern = request.POST.get("username")  # Obtener el usuario del formulario
        passw = request.POST.get("password")  # Obtener la contraseña del formulario
        
        try:
            # Buscar el usuario en la base de datos
            usuario = Practica.objects.get(username=usern)
            
            # Verificar si la contraseña es correcta
            if usuario.password == passw:
                # Guardar datos en la sesión para mantener al usuario logueado
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.username
                return redirect("usuarios")  # Redirigir a la lista de usuarios
            else:
                return render(request, "login.html", {"error": "Contraseña incorrecta"})
        except Practica.DoesNotExist:
            # El usuario no existe en la base de datos
            return render(request, "login.html", {"error": "El usuario no existe"})
    
    return render(request, "login.html")  # Mostrar el formulario de login

# =====================================================================
# VISTA DE USUARIOS
# Muestra la lista de todos los usuarios registrados en la base de datos
# Solo se puede acceder si el usuario está logueado (tiene sesión activa)
# =====================================================================
def usuarios(request):
    # Verificar si el usuario está logueado
    if 'usuario_id' not in request.session:
        return redirect("login")  # Si no está logueado, redirigir al login
    
    # Obtener todos los usuarios de la base de datos
    lista_usuarios = Practica.objects.all()
    
    # Obtener el nombre del usuario logueado desde la sesión
    usuario_actual = request.session.get('usuario_nombre')
    
    # Enviar los datos al template
    return render(request, "usuarios.html", {
        "usuarios": lista_usuarios,
        "usuario_actual": usuario_actual
    })

# =====================================================================
# ELIMINAR USUARIO
# Recibe el ID del usuario a eliminar desde la URL
# Busca el usuario y lo elimina de la base de datos
# =====================================================================
def eliminar_usuario(request, id):
    # Verificar si el usuario está logueado
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    # Buscar el usuario por ID (si no existe, devuelve error 404)
    usuario = get_object_or_404(Practica, id=id)
    
    # Eliminar el usuario de la base de datos
    usuario.delete()
    
    return redirect("usuarios")  # Volver a la lista de usuarios

# =====================================================================
# CERRAR SESIÓN (LOGOUT)
# Elimina todos los datos de la sesión del usuario
# El usuario queda deslogueado y debe iniciar sesión nuevamente
# =====================================================================
def logout(request):
    request.session.flush()  # Eliminar todos los datos de la sesión
    return redirect("login")  # Redirigir al login

# =====================================================================
# FORMULARIO DE REGISTRO
# Permite crear un nuevo usuario con username, password e imagen URL
# =====================================================================
def formulario(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        usern = request.POST.get("username")
        passw1 = request.POST.get("password1")
        passw2 = request.POST.get("password2")
        imagen = request.POST.get("imagen_url")  # Campo de imagen URL

        # Verificar si el usuario ya existe
        if Practica.objects.filter(username=usern).exists():
            sms = "El nombre de usuario ya existe"
            sms2 = "Segundo mensaje"
            
            info = {
                  'infosms':sms,
                  'infosms2':sms2
            }
            return render(request, "formulario.html", info)
        
        # Verificar que las contraseñas coincidan
        if passw1 == passw2:
            # Crear el nuevo usuario en la base de datos
            Practica.objects.create(
                username=usern,
                password=passw2,
                imagen_url=imagen if imagen else None  # Guardar imagen si existe
            )
            return redirect("login")  # Redirigir al login
    return render(request, "formulario.html")

# =====================================================================
# ACTUALIZAR USUARIO
# Permite modificar los datos de un usuario existente
# Recibe el ID del usuario desde la URL
# Muestra un formulario con los datos actuales para editarlos
# =====================================================================
def actualizar_usuario(request, id):
    # Verificar si el usuario está logueado
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    # Buscar el usuario por ID
    usuario = get_object_or_404(Practica, id=id)
    
    if request.method == "POST":  # Si se envió el formulario de actualización
        # Obtener los nuevos datos del formulario
        usern = request.POST.get("username")
        passw = request.POST.get("password")
        imagen = request.POST.get("imagen_url")
        
        # Actualizar los datos del usuario
        usuario.username = usern
        usuario.password = passw
        usuario.imagen_url = imagen if imagen else None
        
        # Guardar los cambios en la base de datos
        usuario.save()
        
        return redirect("usuarios")  # Volver a la lista de usuarios
    
    # Mostrar el formulario con los datos actuales del usuario
    return render(request, "actualizar.html", {"usuario": usuario})