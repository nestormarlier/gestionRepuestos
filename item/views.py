from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Stock, Grupo_Asociado

def grafico(request):
    repuestos = Stock.objects.all()
    item = Stock.objects.all()
    total_repuestos=repuestos.count()

    totales_cambaceres = Stock.objects.filter(grupo_asociado__planta='CAMBACERES', stock_real__lt=F('stock_minimo')).count()
    totales_quilmes = Stock.objects.filter(grupo_asociado__planta='QUILMES', stock_real__lt=F('stock_minimo')).count()
    totales_rivadavia = Stock.objects.filter(grupo_asociado__planta='RIVADAVIA', stock_real__lt=F('stock_minimo')).count()
    
    repuestos_cambaceres = repuestos.filter(grupo_asociado__planta='CAMBACERES')
    # totales_cambaceres = repuestos.filter(grupo_asociado__planta='CAMBACERES').count()
    repuestos_quilmes = repuestos.filter(grupo_asociado__planta='QUILMES')
    # totales_quilmes = repuestos.filter(grupo_asociado__planta='QUILMES').count()
    repuestos_rivadavia = repuestos.filter(grupo_asociado__planta='RIVADAVIA')
    # totales_rivadavia = repuestos.filter(grupo_asociado__planta='RIVADAVIA').count()
    
    return render(request, 'item/graficos.html', {
        'total_repuestos': total_repuestos,
        'repuestos_cambaceres': repuestos_cambaceres,
        'totales_cambaceres': totales_cambaceres,
        'repuestos_quilmes': repuestos_quilmes,
        'totales_quilmes': totales_quilmes,
        'repuestos_rivadavia': repuestos_rivadavia,
        'totales_rivadavia': totales_rivadavia,
        'item': item,
    })
