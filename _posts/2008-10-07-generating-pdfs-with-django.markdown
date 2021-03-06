---
layout: post
comments: true
title:  "Generating PDFs with Django "
date:   2008-10-07 23:01:17+05:30
categories: tips
author: shabda
---
If your web app creates report chances are you also want this report in PDF form. The Django docs describe a way to generate PDFs using ReportLab. Here is some code from there.

	from reportlab.pdfgen import canvas
	from django.http import HttpResponse

	def some_view(request):
	    # Create the HttpResponse object with the appropriate PDF headers.
	    response = HttpResponse(mimetype='application/pdf')
	    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

	    # Create the PDF object, using the response object as its "file."
	    p = canvas.Canvas(response)

	    # Draw things on the PDF. Here's where the PDF generation happens.
	    # See the ReportLab documentation for the full list of functionality.
	    p.drawString(100, 100, "Hello world.")

	    # Close the PDF object cleanly, and we're done.
	    p.showPage()
	    p.save()
	    return response

This suffers from two problems,

1. You are laying out your PDF using Python, which means if you later want to change the design of the PDF you need to change the Python code.
2. Most of the time you already have the report in Html, form, writing the same PDF via ReportLab is error prone.

Both these problems can be cleanly solved using Pisa, a Html2Pdf library. We proceed as,

1. Generate a Html representation of Pdf using normal Django macienry.
2. Convert to Pdf using Pisa.
3. Return PDF.

This solves both our problems as,

1. Designers can edit the template to change the layout of Pdf.
2. The code to generate the Html and Pdf views can share code.

Here is some example code.

	def html_view(request, as_pdf = False):
		#Get varaibles to populate the template
		payload = {'data':data, ....}
		if as_pdf:
			return payload
		return render_to_response('app/template.html', payload, RequestContext(request))

	def pdf_view(request):
		payload = html_view(request, as_pdf = True)
		file_data = render_to_string('app/template.pdf', payload, RequestContext(request))
		myfile = StringIO.StringIO()
		pisa.CreatePDF(file_data, myfile)
		myfile.seek(0)
		response =  HttpResponse(myfile, mimetype='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=coupon.pdf'
		return response





