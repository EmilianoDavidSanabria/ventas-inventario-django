from django.shortcuts import render, redirect
from .forms import ProductoForm, VentaForm, FiltroVentasForm
from .models import Producto, Venta
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncQuarter
import plotly.express as px
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
import openpyxl
from django.contrib import messages

# Vista para agregar productos

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

# Vista para agregar ventas

@login_required
def agregar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto = venta.producto
            venta.total = producto.precio * venta.cantidad
            venta.save()
            # Invalida el caché de la lista de ventas
            cache.delete('ventas_list')
            return redirect('lista_ventas')
    else:
        form = VentaForm()
    
    return render(request, 'agregar_venta.html', {'form': form})

# Vista para generar gráficos de ventas con Matplotlib

@login_required
def graficos_ventas(request):
    import matplotlib
    matplotlib.use('Agg')  # Cambiar el backend a uno sin GUI
    import matplotlib.pyplot as plt
    import pandas as pd
    from io import BytesIO
    from django.http import HttpResponse

    try:
        # Obtener datos de ventas
        ventas = Venta.objects.all().values('fecha', 'total')
        df = pd.DataFrame(ventas)

        plt.figure(figsize=(10, 6))
        plt.plot(df['fecha'], df['total'], marker='o', linestyle='-', color='b')
        plt.title('Ventas Totales por Fecha')
        plt.xlabel('Fecha')
        plt.ylabel('Total')

        # Guardar el gráfico en memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')
    except Exception as e:
        return HttpResponse(f'Error al generar el gráfico: {e}', status=500)


# Vista para estadísticas de ventas mensuales y trimestrales

@login_required
def estadisticas_ventas(request):
    ventas = Venta.objects.all()
    
    # Usamos TruncMonth y TruncQuarter para agrupar
    total_mensual = ventas.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total=Sum('total'))
    total_trimestral = ventas.annotate(trimestre=TruncQuarter('fecha')).values('trimestre').annotate(total=Sum('total'))

    contexto = {
        'total_mensual': total_mensual,
        'total_trimestral': total_trimestral,
    }
    return render(request, 'estadisticas.html', contexto)

# Vista para filtrar ventas

@login_required
def ventas_filtradas(request):
    form = FiltroVentasForm(request.GET or None)  # Recoge los datos del formulario
    ventas = Venta.objects.all()  # Consulta base sin filtros

    if form.is_valid():
        # Recoge los valores del formulario
        producto = form.cleaned_data.get('producto')
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        precio_minimo = form.cleaned_data.get('precio_minimo')
        precio_maximo = form.cleaned_data.get('precio_maximo')
        estado = form.cleaned_data.get('estado')

        # Aplica filtros solo si los datos existen
        if producto:
            ventas = ventas.filter(producto=producto)  # Usa directamente el objeto producto
        if fecha_inicio:
            ventas = ventas.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            ventas = ventas.filter(fecha__lte=fecha_fin)
        if precio_minimo is not None:
            ventas = ventas.filter(total__gte=precio_minimo)
        if precio_maximo is not None:
            ventas = ventas.filter(total__lte=precio_maximo)
        if estado:
            ventas = ventas.filter(estado=estado)

    # Calcula el total de ventas después de los filtros
    total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0

    contexto = {
        'form': form,
        'ventas': ventas,
        'total_ventas': total_ventas,
    }
    return render(request, 'ventas_filtradas.html', contexto)




# Vista para generar gráficos interactivos con Plotly
@login_required
def graficos_interactivos(request):
    ventas = Venta.objects.all().values('fecha', 'total')
    df = pd.DataFrame(ventas)

    fig = px.line(df, x='fecha', y='total', title='Ventas Totales por Fecha')

    # Convertir el gráfico en HTML
    grafico = fig.to_html(full_html=False)

    contexto = {'grafico': grafico}
    return render(request, 'graficos_interactivos.html', contexto)

# Vista para estadísticas avanzadas
@login_required
def estadisticas_avanzadas(request):
    ventas = Venta.objects.all().values('fecha', 'total')
    df = pd.DataFrame(ventas)

    # Agrupar por mes
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.to_period('M')
    ventas_mensuales = df.groupby('mes')['total'].sum().reset_index()

    # Agrupar por trimestre
    df['trimestre'] = df['fecha'].dt.to_period('Q')
    ventas_trimestrales = df.groupby('trimestre')['total'].sum().reset_index()

    contexto = {
        'ventas_mensuales': ventas_mensuales.to_dict('records'),
        'ventas_trimestrales': ventas_trimestrales.to_dict('records'),
    }
    return render(request, 'estadisticas_avanzadas.html', contexto)

# Vista para productos más vendidos
@login_required
def productos_mas_vendidos(request):
    # Consultar las ventas agrupadas por producto y sumar la cantidad vendida
    ventas = Venta.objects.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')
    df = pd.DataFrame(ventas)

    # Crear gráfico de barras
    fig = px.bar(df, x='producto__nombre', y='total_vendido', title='Productos más vendidos')

    # Convertir el gráfico en HTML
    grafico = fig.to_html(full_html=False)

    contexto = {'grafico': grafico}
    return render(request, 'productos_mas_vendidos.html', contexto)

# Vista para registro de usuario

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Vista para login de usuario

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("inicio")
    else:
        form = AuthenticationForm()
        if request.GET.get('next'):
            messages.warning(request, "Debés iniciar sesión para acceder a esa página.")

    return render(request, 'login.html', {'form': form})

# Vista para logout de usuario
def logout_usuario(request):
    logout(request)  # Esto elimina la sesión activa del usuario
    return redirect("inicio")

def inicio(request):
    return render(request, "inicio.html")

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

@login_required
def lista_ventas(request):
    # Intentar obtener las ventas desde el caché
    ventas_list = cache.get('ventas_list')
    if not ventas_list:
        # Obtener todas las ventas con select_related para evitar consultas adicionales
        ventas_list = Venta.objects.select_related('producto').only('producto', 'cantidad', 'total', 'fecha')
        # Almacenar en caché por 15 minutos
        cache.set('ventas_list', ventas_list, timeout=60*15)

    # Configurar la paginación
    paginator = Paginator(ventas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'lista_ventas.html', {'page_obj': page_obj})

@login_required
def exportar_ventas_excel(request):
    try:
        ventas = Venta.objects.all()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Ventas'

        # Encabezados
        headers = ['Producto', 'Cantidad', 'Total', 'Fecha']
        ws.append(headers)

        # Datos
        for venta in ventas:
            ws.append([venta.producto.nombre, venta.cantidad, venta.total, venta.fecha])

        # Guardar en memoria
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="ventas.xlsx"'
        return response
    except Exception as e:
        return HttpResponse(f'Error al exportar los datos: {e}', status=500)
