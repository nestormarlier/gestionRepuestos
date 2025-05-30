from django.contrib import admin
from django.utils.html import format_html
from django.db import models 
from .models import Grupo_Asociado, Stock,StockAudit
from django.core.exceptions import ValidationError
from django.contrib import messages
from import_export.admin import ImportExportModelAdmin

################################ FILTRO POR STOCK BAJO ################################

class StockBajoListFilter(admin.SimpleListFilter):
    title = 'Stock Bajo'
    parameter_name = 'stock_bajo'

    def lookups(self, request, model_admin):
        return (
            ('bajo', 'Por debajo del stock mínimo'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'bajo':
            return queryset.filter(stock_real__lt=models.F('stock_minimo'))
        return queryset
################################ FIN FILTRO POR STOCK BAJO ################################


################################ FILTRO POR PLANTA ################################

class PlantaListFilter(admin.SimpleListFilter):
    title = 'Planta'
    parameter_name = 'planta'

    def lookups(self, request, model_admin):
        return Grupo_Asociado.LOCACION_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(grupo_asociado__planta=self.value())
        return queryset

################################ FIN FILTRO POR PLANTA ################################

class StockAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('repuesto_id_css','descripcion', 'grupo_asociado', 'stock_status_css','stock_minimo','mostrar_imagen','ubicacion_fisica')
    readonly_fields = ('modified_by',)
    search_fields = ('repuesto_id', 'grupo_asociado__nombre')
    list_filter = (PlantaListFilter,'grupo_asociado__nombre','repuesto_id',) #filtro por planta
    list_filter = (StockBajoListFilter, 'grupo_asociado__nombre', 'repuesto_id',) #filtro por stock bajo
        # Usar fields para definir el orden de los campos
    fieldsets = (
        ('Información del repuesto', {
            'fields': ('repuesto_id', 'descripcion','grupo_asociado','stock_real', 'imagen')
        }),
        ('Niveles de stock', {
            'fields': ('stock_minimo', 'stock_maximo', 'punto_de_reposicion'),
            'classes': ('collapse',), 
        }),
        ('Otros datos', {
            'fields': ('ubicacion_fisica',),
            'classes': ('collapse',), 
        }),
    )
####################### INGRESO STOCK NEGATIVO ##########################
    def save_model(self, request, obj, form, change):
        try:
            # Validar que el valor de stock_real sea positivo
            if obj.stock_real < 0:
                raise ValidationError("El stock real no puede ser negativo. NO SE MODIFICÓ EL STOCK")
            # Si pasa la validación, llamamos al método save() del modelo para guardar
            else:
                 # Verificar si el repuesto_id ya existe en la misma planta
                existing_stock = Stock.objects.filter(repuesto_id=obj.repuesto_id, grupo_asociado=obj.grupo_asociado).exclude(pk=obj.pk)
                if existing_stock.exists() and not change:
                    messages.warning(request, 'Este repuesto ya existe en la misma planta. No será registrado guarde nuevamente.')
                    return
                  # No guardar el objeto en la primera instancia
                else:
                    # Si pasa la validación, llamamos al método save() del modelo para guardar
                    obj.save()
                    messages.success(request, '')
        except ValidationError as e:
            messages.error(request, f'Error al guardar el stock: {", ".join(e.messages)}')

####################### color Stock Real  #########################
    def stock_status(self, obj):
        if obj.stock_real < obj.stock_minimo:
            return 'stock-bajo'
        elif obj.stock_real >= obj.stock_minimo:
            return 'stock-suficiente'
            
    # stock_status.short_description = 'Stock Real'
    
    def stock_status_css(self,obj):
        return format_html('<span class="{}">{}</span>', self.stock_status(obj), obj.stock_real)

    stock_status_css.allow_tags = True
    stock_status_css.short_description = 'Stock Real'
    stock_status_css.admin_order_field = 'stock_real'

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.imagen.url)
        return "Sin imagen"

    mostrar_imagen.short_description = 'Imagen Adjunta'

###################### color Repuesto ID ###########################

    def repuesto_id(self, obj):
        if obj.stock_real < obj.stock_minimo:
            return 'stock-bajo'
        elif obj.stock_real >= obj.stock_minimo:
            return 'stock-suficiente'
        
    def repuesto_id_css(self,obj):
        return format_html('<span class="{}">{}</span>', self.repuesto_id(obj), obj)
    
    repuesto_id_css.allow_tags = True
    repuesto_id_css.short_description = 'Repuesto'

################################ fin color ################################

class Grupo_AsociadoAdmin(admin.ModelAdmin):
    search_fields = ('nombre','activo','planta')
    list_filter= ('planta',)

class StockAuditAdmin(admin.ModelAdmin):
    # search_fields = ('stock',)
    list_display = ('stock','user', 'cantidad','diferencia_cantidad', 'timestamp')
    readonly_fields = ('stock', 'user', 'action', 'cantidad', 'timestamp')
    list_filter = ('stock',)

    def diferencia_cantidad(self, obj):
        anterior = StockAudit.objects.filter(stock=obj.stock, timestamp__lt=obj.timestamp).order_by('-timestamp').first()
        if anterior != None:
            diferencia = obj.cantidad - anterior.cantidad
            if obj.cantidad != anterior.cantidad:
                return f'+{diferencia}' if diferencia > 0 else diferencia
        else:
            return "-"

    diferencia_cantidad.short_description = 'MOVIMIENTO'
    
admin.site.site_header = 'Sistema de gestión de repuestos'
admin.site.index_title = 'Área de características' # default:
admin.site.site_title = 'Sistema de gestión' # default: "Django site admin"

admin.site.register(Stock, StockAdmin)
admin.site.register(Grupo_Asociado,Grupo_AsociadoAdmin)
admin.site.register(StockAudit,StockAuditAdmin)