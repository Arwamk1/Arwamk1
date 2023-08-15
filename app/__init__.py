#import the flask here and the routes file to link between the eoutes 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configure your app here (database, secret key, etc.)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)


from app import pdf
from app import routes  # Import your routes
from app.models import User  # Import your models

# Rest of your code...
from flask import Flask, render_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
import os

@app.route('/generate_pdf')
def generate_pdf():
    pdf_filename = 'example.pdf'
    output_file_path = os.path.join(app.root_path, 'static', pdf_filename)
    
    c = canvas.Canvas(output_file_path, pagesize=letter)
    
    # Load image from the static folder
    image_path = os.path.join(app.root_path, 'static', 'image.png')
    
    # Create an Image element
    img = Image(image_path)
    
    # Draw the image on the canvas
    img.drawOn(c, 100, 600)  # Adjust coordinates as needed
    
    c.save()
    
    return f'PDF generated: <a href="/static/{pdf_filename}">{pdf_filename}</a>'
