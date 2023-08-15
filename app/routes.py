#all the routes should be here 

from flask import render_template, request, redirect, url_for
from app import app
from werkzeug.utils import secure_filename
import hashlib
import os

from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
import pandas as pd
import openai
import os


# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Define allowed file extensions and upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/") # مسؤول عن كل backend
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/Sign") 
def Sign(): #اسم الصفحات
    return render_template('sign.html')


@app.route("/profile") 
def profile(): #اسم الصفحات
    return render_template('profile.html')

@app.route("/upload") 
def upload(): #اسم الصفحات
    return render_template('upload.html')

@app.route("/about") 
def about(): #اسم الصفحات
    return render_template('about.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform validation and authentication here
        username_error = validate_username(username)
        password_error = validate_password(password)

        if username_error or password_error:
            return render_template('login.html', username_error=username_error, password_error=password_error)

        # Hash the password before storing it (use a more secure hashing method in production)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Perform user authentication and redirection here
        # For this example, just redirect to a welcome page
        return redirect(url_for('home'))

    return render_template('login.html')

def validate_username(username):
    if not (1 <= len(username) <= 50):
        return "Username/ID must be between 1 and 50 characters"
    if username.startswith('E') and not username.isnumeric():
        return "Employee ID must start with 'E'"
    return None

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return "Password must contain an uppercase letter"
    if not any(c.islower() for c in password):
        return "Password must contain a lowercase letter"
    if not any(c.isdigit() for c in password):
        return "Password must contain a number"
    return None


def create_pdf_with_template_and_image(data, completion_response, image_path, output_file):
     # Define page border
    page_border = 19

    # Styles and formatting
    title_style = ParagraphStyle(
        name='TitleStyle',
        fontSize=18,
        textColor=colors.black,
        spaceAfter=40,
        alignment=1,
        fontName='Times-Bold'
    )

    #style the sub title to bold 
    title_style2 = ParagraphStyle(
        topMargin=30,
        name='TitleStyle',
        fontSize=14,
        textColor=colors.black,
        spaceAfter=12,
        #leftIndent=20,
        #rightIndent=30,
        #backColor=colors.yellow,
       fontName='Times-Bold'    
    )
    # style the data extracted from the excel file 
    main_style1 = ParagraphStyle(
        name='MainStyle',
        fontSize=12,
        leading=14,
         leftIndent=15,
        # rightIndent=50,
        spaceAfter=6,
        fontName='Times' 
        
     )
    
    # style the summry report written by the ai
    main_style2 = ParagraphStyle(
        name='MainStyle2',
        fontSize=12,
        leading=14,
        textColor=colors.black,
        leftIndent=15,
        #rightIndent=50,
        spaceAfter=6,
        fontName='Times'
    )

    # Create a PDF document using the custom template
    doc = SimpleDocTemplate(output_file, pagesize=letter, leftMargin=page_border, rightMargin=page_border, topMargin=page_border, bottomMargin=page_border)

    # Construct the content
    content = []

    # Add title 
    content.append(Paragraph("Reserach Closing Form", title_style))

    # # Add image
    
    # content.append(Image(image_path, width=125, height=125))  
    # Add image
    img = Image(image_path, width=125, height=125)
    img.hAlign = 'CENTER'  # Center the image horizontally
    content.append(img)

  
    # Add a section for the  excel data
      # Add space under the image
    content.append(Paragraph("<br/><br/><br/>", main_style1))  # Add empty paragraphs for space
    content.append(Paragraph("Resercher information: ", title_style2))
    content.append(Paragraph("",main_style1))
 
    for element in data:
        content.append(Paragraph(str(element), main_style1))
 
    # Add a section for the completion response (AI )
    content.append(Paragraph("<br/><br/><br/><br/><br/><br/>", main_style1))
    content.append(Paragraph("Report Summary generated using AI: ", title_style2))
    content.append(Paragraph("", main_style2))
    content.append(Paragraph(completion_response, main_style2))
    
    # Build the PDF document
    doc.build(content)

# Function to validate uploaded file's extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Read and process Excel data
            data = pd.read_excel(filepath)
        
            numofrows = len(data.index)
            excelFile = []

            for i in range(numofrows):
                Authors = data["Authors"].loc[i]
                Affiliations = data["Affiliations"].loc[i]
                Email = data["Email Addresses"].loc[i]
                Article_Title = data["Article Title"].loc[i]
                Publication_Year = data["Publication Year"].loc[i]
                Abstract = data["Abstract"].loc[i]
                Funding_Orgs = data["Funding Orgs"].loc[i]
                Author_Keywords = data["Author Keywords"].loc[i]

                excelFile.append("-Author Name: " + Authors,
                                "-Affiliations: " + Affiliations,
                                "-Email: " + Email,
                                "-Article Title: " + Article_Title,
                                "-Date: " + Publication_Year,
                                "-Abstract: " + Abstract,
                                "-Funding Orgs: " + Funding_Orgs,
                                "-Author keyword: " + Author_Keywords)


        openai.api_key = os.getenv("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")
        openai.api_key="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"

        completion=openai.Completion.create(engine="text-davinci-003",prompt="Write a closing report for a research with the title " + Article_Title + " with an abstract " + Abstract + " The authors name "  + Authors + "and the Author keyword "+Author_Keywords+ " on this date " ,max_tokens=1000)


        AiReport=completion.choices[0]["text"]  

        pdf_filename = "staticoutput.pdf" 

         # Save the PDF file in the static folder
        output_file_path = "/Users/WIN/Downloads/flask project/app/static" + pdf_filename
     
        image_path= '/Users/WIN/Downloads/flask project/app/static/image.png'

        create_pdf_with_template_and_image(excelFile ,AiReport,image_path, output_file_path)  
        return render_template ('download.html', pdf_filename=pdf_filename) 
    return render_template('upload.html')



@app.route('/download/<pdf_filename>')
def download(pdf_filename):
    return send_from_directory('static', pdf_filename, as_attachment=True)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'The file "{filename}" has been uploaded.'
