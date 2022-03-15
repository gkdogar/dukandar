
from django.http import HttpResponse
from django.views.generic import View

from django.template.loader import get_template
from io import BytesIO


from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
  
#         carts = [{
#             "id": 123,
#             "title": "Transport",
#             "unit_price": 1399.99,
#             "quantity": 5,
#             "commission":10,
#             "amount":1520,
#         }]
#         pdf = render_to_pdf('fimbay/Products/pdf.html', {'carts':carts})
#         response = HttpResponse(pdf,content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
       
#         return response
        
# from io import BytesIO #A stream implementation using an in-memory bytes buffer
#                        # It inherits BufferIOBase
# from django.http import HttpResponse
# from django.template.loader import get_template
 
# #pisa is a html2pdf converter using the ReportLab Toolkit,
# #the HTML5lib and pyPdf.
 
# from xhtml2pdf import pisa  
# #difine render_to_pdf() function
 
# def render_to_pdf(template_src, context_dict={}):
#      template = get_template(template_src)
#      html  = template.render(context_dict)
#      result = BytesIO()
 
#      #This part will create the pdf.
#      pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#      if not pdf.err:
#          return HttpResponse(result.getvalue(), content_type='application/pdf')
#      return None

