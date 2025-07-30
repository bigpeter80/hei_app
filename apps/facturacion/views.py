# apps/facturacion/views.py
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from apps.facturacion.models import Factura
from apps.reservas.models import Reserva

def factura_detalle(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    factura = get_object_or_404(Factura, reserva=reserva)
    return render(request, 'facturacion/detalle.html', {'factura': factura})


def factura_pdf(request, reserva_id):
    factura = get_object_or_404(Factura, reserva_id=reserva_id)
    template = get_template('facturacion/pdf.html')

    # Si usas logo desde static:
    logo_url = request.build_absolute_uri('/static/images/hei_logo.png')

    context = {
        'factura': factura,
        'logo_url': logo_url,
    }

    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"factura_{factura.id}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    else:
        return HttpResponse("Error al generar el PDF", status=500)
    
def factura_imprimir(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, 'facturacion/imprimir.html', {'factura': factura})