import jinja2, os, pdfkit, ssl, smtplib
from decouple import config
from email.message import EmailMessage

def get_pdf(n_taula, n_check, productes):
    if not os.path.exists('pdfs/'):
        os.mkdir('pdfs/')
    dir_output = os.path.abspath('pdfs/')
    dir_plantilla = os.path.join(os.path.dirname(__file__), 'plantilla/')

    img = os.path.abspath('img/logo.png')
    subtotal = 0
    impostos = 0
    total = 0
    llista_articles = []
    for producte in productes:
        article = []
        article.append(producte[0])
        article.append(producte[1])
        article.append(f"{round(producte[0]*producte[2],2):.2f}")
        subtotal += float(producte[0]*producte[2])
        llista_articles.append(article)

    impostos += subtotal*0.21
    total += subtotal + impostos

    datos = {
        'n_taula': n_taula,
        'n_check': n_check,
        'productes': llista_articles,
        'subtotal': f"{round(subtotal,2):.2f}",
        'impostos': f"{round(impostos,2):.2f}",
        'total': f"{round(total,2):.2f}",
        'image': img,
        }

    template_loader = jinja2.FileSystemLoader(dir_plantilla)
    template_env = jinja2.Environment(loader=template_loader)
    plantilla_html = template_env.get_template('plantilla.html')
    output_text = plantilla_html.render(datos)

    config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_string(output_text, os.path.join(dir_output,'factura.pdf'), configuration=config,options={"enable-local-file-access": ""}, css=os.path.join(dir_plantilla, 'plantilla.css'))
    
def send_pdf(email_receptor):
    email_emisor = 'pdf.qwikorder@gmail.com'
    password = config('MAIL_KEY')
    asunto = "Factura QwikOrder"
    cuerpo = "Factura de prova generada per l'aplicació QwikOrder"

    em = EmailMessage()
    em['From'] = email_emisor
    em['To'] = email_receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)

    context = ssl.create_default_context()

    with open('./pdfs/factura.pdf', 'rb') as file:
        file_data = file.read()
        em.add_attachment(file_data, maintype='application', subtype = 'octet-stream', filename="Factura QwikOrder.pdf")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email_emisor, password)
        server.sendmail(email_emisor, email_receptor, em.as_string())