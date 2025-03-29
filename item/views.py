from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Stock, Grupo_Asociado

def grafico(request):
    repuestos = Stock.objects.all()
    item = Stock.objects.all()
    total_repuestos=repuestos.count()

    totales_plantaA = Stock.objects.filter(grupo_asociado__planta='PLANTA A', stock_real__lt=F('stock_minimo')).count()
    totales_plantaB = Stock.objects.filter(grupo_asociado__planta='PLANTA B', stock_real__lt=F('stock_minimo')).count()
    totales_plantaC = Stock.objects.filter(grupo_asociado__planta='PLANTA C', stock_real__lt=F('stock_minimo')).count()
    
    repuestos_plantaA = repuestos.filter(grupo_asociado__planta='PLANTA A')
    # totales_cambaceres = repuestos.filter(grupo_asociado__planta='CAMBACERES').count()
    repuestos_plantaB = repuestos.filter(grupo_asociado__planta='PLANTA B')
    # totales_quilmes = repuestos.filter(grupo_asociado__planta='QUILMES').count()
    repuestos_PlantaC = repuestos.filter(grupo_asociado__planta='PLANTA C')
    # totales_rivadavia = repuestos.filter(grupo_asociado__planta='RIVADAVIA').count()
    
    return render(request, 'item/graficos.html', {
        'total_repuestos': total_repuestos,
        'repuestos_plantaA': repuestos_plantaA,
        'totales_plantaA': totales_plantaA,
        'repuestos_plantaB': repuestos_plantaB,
        'totales_plantaB': totales_plantaB,
        'repuestos_plantaC': repuestos_PlantaC,
        'totales_plantaC': totales_plantaC,
        'item': item,
    })
