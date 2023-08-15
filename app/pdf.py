# from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
# import pandas as pd
# import openai
# import os

# pdf = Blueprint('pdf', __name__)

# # ... (rest of your existing code)

# @pdf.route('/pdf')
# def generate_pdf():

#     # Move your PDF generation code here
#     # ...
#     pdf_filename = 'staticoutput.pdf'
#     image_path = 'image.png'

#     create_pdf_with_template_and_image(excelFile, AiReport, image_path, pdf_filename)
#     return render_template('download.html', pdf_filename=pdf_filename)

# @pdf.route('/download/<pdf_filename>')
# def download_pdf(pdf_filename):
#     return send_from_directory('static', pdf_filename, as_attachment=True)
