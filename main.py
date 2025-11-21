import os
import smtplib
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfdoc
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
# Registrar fontes Poppins
pdfmetrics.registerFont(TTFont('Poppins', 'fonts/Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Bold', 'fonts/Poppins-Bold.ttf'))
from reportlab.rl_config import defaultPageSize
pdfdoc.PDFImageCompression = False


# =====================================================
# FUNÇÃO AUXILIAR PARA QUEBRA AUTOMÁTICA DE TEXTO
# =====================================================
def split_text(texto, canvas_obj, max_width, font="Poppins", size=9):
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for p in palavras:
        teste = linha_atual + " " + p if linha_atual else p
        if canvas_obj.stringWidth(teste, font, size) <= max_width:
            linha_atual = teste
        else:
            linhas.append(linha_atual)
            linha_atual = p

    if linha_atual:
        linhas.append(linha_atual)

    return linhas


# =====================================================
# 1 — GERAR CERTIFICADO PDF (HORIZONTAL COM 2 COLUNAS)
# =====================================================
def generate_certificate(name, output_path):
    background_path = "assets/background.png"

    # Página A4 horizontal (landscape)
    w, h = landscape(A4)
    c = canvas.Canvas(output_path, pagesize=(w, h))

    bg = ImageReader(background_path)
    c.drawImage(bg, 0, 0, width=w, height=h)

    largura_coluna = w / 2

    # Coluna da direita → início
    margem_x = largura_coluna + 60
    texto_largura = largura_coluna - 95
    y_start = h - 200

    texto = (
        f"This certifies that {name} has successfully participated in the "
        f"Example Conference on Advanced Topics, held at an unspecified location "
        f"on a sample date, with a total duration of X hours."
    )

    c.setFont("Poppins", 9)
    c.setFillColorRGB(0.121, 0.298, 0.368)  # #1f4c5e
    y = y_start - 50

    for linha in split_text(texto, c, texto_largura):
        c.drawString(margem_x, y, linha)
        y -= 18

    c.showPage()
    c.save()

    print(f"PDF gerado: {output_path}")


# =====================================================
# 2 — ENVIO DO CERTIFICADO POR EMAIL
# =====================================================
def send_certificate(to_email, pdf_path):
    SMTP_HOST = "mail.example.pt"
    SMTP_PORT = 465
    SMTP_USER = "no-reply@example.pt"
    SMTP_PASS = "myPassword"

    subject = (
        "Your Certificate – Demo Event Notification"
    )
    body = (
        "Hello,\n\n"
        "Please find attached your participation certificate for the Sample Event. "
        "This is placeholder text intended for demonstration in a public repository.\n\n"
        "If you need any additional information, feel free to contact our support inbox "
        "at example@example.com.\n\n"
        "Best regards,\n\n"
        "The Demo Event Team"
    )

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    from email.mime.text import MIMEText
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "pdf")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(pdf_path)}"'
        )
        msg.attach(part)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print(f"Email enviado para: {to_email}")


# =====================================================
# 3 — SCRIPT PRINCIPAL
# =====================================================
if __name__ == "__main__":
    pessoas = [
        {"nome": "Example 1", "email": "exa1@example.com"},
        {"nome": "Example 2", "email": "exa2@example.com"},

    ]

    os.makedirs("output", exist_ok=True)

    for pessoa in pessoas:
        nome = pessoa["nome"]
        email = pessoa["email"]

        pdf_path = f"output/certificado_{nome.replace(' ', '_')}.pdf"

        generate_certificate(nome, pdf_path)
        send_certificate(email, pdf_path)
        print("Waiting before processing the next item...")
        time.sleep(15)