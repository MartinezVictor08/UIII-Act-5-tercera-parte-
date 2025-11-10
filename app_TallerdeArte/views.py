from django.shortcuts import render, redirect
from .models import Instructor

# Página de inicio
def inicio_TallerdeArte(request):
    return render(request, 'inicio.html')


# Agregar instructor
def agregar_instructor(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        especialidad = request.POST['especialidad']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        experiencia_anios = request.POST['experiencia_anios']
        sueldo = request.POST['sueldo']

        nuevo = Instructor(
            nombre=nombre,
            apellido=apellido,
            especialidad=especialidad,
            telefono=telefono,
            correo=correo,
            experiencia_anios=experiencia_anios,
            sueldo=sueldo
        )
        nuevo.save()
        return redirect('ver_instructor')
    return render(request, 'instructor/agregar_instructor.html')


# Ver instructores
def ver_instructor(request):
    instructores = Instructor.objects.all()
    return render(request, 'instructor/ver_instructor.html', {'instructores': instructores})


# Actualizar instructor
def actualizar_instructor(request, id):
    instructor = Instructor.objects.get(instructor_id=id)
    return render(request, 'instructor/actualizar_instructor.html', {'instructor': instructor})


# Realizar actualización
def realizar_actualizacion_instructor(request, id):
    instructor = Instructor.objects.get(instructor_id=id)
    if request.method == 'POST':
        instructor.nombre = request.POST['nombre']
        instructor.apellido = request.POST['apellido']
        instructor.especialidad = request.POST['especialidad']
        instructor.telefono = request.POST['telefono']
        instructor.correo = request.POST['correo']
        instructor.experiencia_anios = request.POST['experiencia_anios']
        instructor.sueldo = request.POST['sueldo']
        instructor.save()
        return redirect('ver_instructor')
    return redirect('ver_instructor')


# Borrar instructor
def borrar_instructor(request, id):
    instructor = Instructor.objects.get(instructor_id=id)
    instructor.delete()
    return redirect('ver_instructor')




from django.shortcuts import render, redirect, get_object_or_404
from .models import Material, Curso
# Si usas Curso luego, puedes importarlo: from .models import Curso

# Agregar material
def agregar_material(request):
    cursos = Curso.objects.all().order_by('nombre_curso')  # 🔹 Se obtienen todos los cursos para el combobox

    if request.method == 'POST':
        nombre_material = request.POST.get('nombre_material')
        tipo = request.POST.get('tipo')
        marca = request.POST.get('marca')
        cantidad_stock = request.POST.get('cantidad_stock') or 0
        costo_unitario = request.POST.get('costo_unitario') or 0
        nombre_proveedor = request.POST.get('nombre_proveedor')
        descripcion = request.POST.get('descripcion')

        curso_id = request.POST.get('curso')
        curso_obj = None
        if curso_id:
            try:
                curso_obj = Curso.objects.get(pk=curso_id)
            except Curso.DoesNotExist:
                curso_obj = None

        Material.objects.create(
            nombre_material=nombre_material,
            tipo=tipo,
            marca=marca,
            cantidad_stock=cantidad_stock,
            costo_unitario=costo_unitario,
            nombre_proveedor=nombre_proveedor,
            descripcion=descripcion,
            curso=curso_obj
        )

        return redirect('ver_material')

    # 🔹 Importante: enviar los cursos al HTML
    return render(request, 'material/agregar_material.html', {'cursos': cursos})


# Ver materiales (lista)
def ver_material(request):
    materiales = Material.objects.all().order_by('material_id')
    return render(request, 'material/ver_material.html', {'materiales': materiales})

# Mostrar formulario de actualización
def actualizar_material(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    return render(request, 'material/actualizar_material.html', {'material': material})

# Procesar actualización
def realizar_actualizacion_material(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    if request.method == 'POST':
        material.nombre_material = request.POST.get('nombre_material')
        material.tipo = request.POST.get('tipo')
        material.marca = request.POST.get('marca')
        material.cantidad_stock = request.POST.get('cantidad_stock') or 0
        material.costo_unitario = request.POST.get('costo_unitario') or 0
        material.nombre_proveedor = request.POST.get('nombre_proveedor')
        material.descripcion = request.POST.get('descripcion')
        # curso opcional
        curso_id = request.POST.get('curso')
        if curso_id:
            try:
                from .models import Curso
                material.curso = Curso.objects.get(pk=curso_id)
            except Exception:
                material.curso = None
        material.save()
        return redirect('ver_material')
    return redirect('ver_material')

# Borrar material (confirmación y borrado)
def borrar_material(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    if request.method == 'POST':
        material.delete()
        return redirect('ver_material')
    return render(request, 'material/borrar_material.html', {'material': material})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Instructor

# Agregar curso
def agregar_curso(request):
    instructores = Instructor.objects.all().order_by('nombre')
    if request.method == 'POST':
        nombre_curso = request.POST.get('nombre_curso')
        descripcion = request.POST.get('descripcion')
        salon_num = request.POST.get('salon_num') or 0
        duracion_semanas = request.POST.get('duracion_semanas') or 0
        costo = request.POST.get('costo') or 0
        fecha_inicio = request.POST.get('fecha_inicio')  # formato YYYY-MM-DD
        cupo_maximo = request.POST.get('cupo_maximo') or 0
        instructor_id = request.POST.get('instructor')  # id seleccionado del combobox

        instructor_obj = None
        if instructor_id:
            try:
                instructor_obj = Instructor.objects.get(pk=instructor_id)
            except Instructor.DoesNotExist:
                instructor_obj = None

        Curso.objects.create(
            nombre_curso=nombre_curso,
            descripcion=descripcion,
            salon_num=salon_num,
            duracion_semanas=duracion_semanas,
            costo=costo,
            fecha_inicio=fecha_inicio,
            cupo_maximo=cupo_maximo,
            instructor=instructor_obj
        )
        return redirect('ver_curso')

    return render(request, 'curso/agregar_curso.html', {'instructores': instructores})

# Ver lista de cursos
def ver_curso(request):
    cursos = Curso.objects.all().order_by('curso_id')
    return render(request, 'curso/ver_curso.html', {'cursos': cursos})

# Mostrar formulario de actualización
def actualizar_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    instructores = Instructor.objects.all().order_by('nombre')
    return render(request, 'curso/actualizar_curso.html', {'curso': curso, 'instructores': instructores})

# Procesar actualización
def realizar_actualizacion_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        curso.nombre_curso = request.POST.get('nombre_curso')
        curso.descripcion = request.POST.get('descripcion')
        curso.salon_num = request.POST.get('salon_num') or 0
        curso.duracion_semanas = request.POST.get('duracion_semanas') or 0
        curso.costo = request.POST.get('costo') or 0
        fecha_inicio = request.POST.get('fecha_inicio')
        if fecha_inicio:
           curso.fecha_inicio = fecha_inicio  # Solo si no está vacío


        curso.cupo_maximo = request.POST.get('cupo_maximo') or 0
        instructor_id = request.POST.get('instructor')
        if instructor_id:
            try:
                curso.instructor = Instructor.objects.get(pk=instructor_id)
            except Instructor.DoesNotExist:
                curso.instructor = None
        curso.save()
        return redirect('ver_curso')
    return redirect('ver_curso')

# Borrar curso (confirmación)
def borrar_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        curso.delete()
        return redirect('ver_curso')
    return render(request, 'curso/borrar_curso.html', {'curso': curso})