# Certificate Generator and Email Sender (Python)

A Python automation tool that generates personalized PDF certificates and sends them to participants via email.  
This project includes a customizable certificate layout, custom fonts, background images, batch processing, and rate limiting to avoid spam triggers.

---

## 🚀 Features

- Generate PDF certificates using **ReportLab**
- Custom font support (e.g., *Poppins*)
- Background image and layout configuration
- Two-column certificate layout (landscape mode)
- Automatic text wrapping
- Email sending via SMTP
- Rate limiting (4 emails per minute)
- Clean project structure
- Easy to integrate with CSV or database exports

---

## 🛠️ Technologies Used

- **Python 3.x**
- **ReportLab** (PDF generation)
- **smtplib** (email sending)
- **email.mime** (attachments)
- **Pillow** *(optional)* for image processing

---

## 📦 Installation

Clone the repository:

```bash
  git clone https://github.com/gushy/certificate-generator-python
```
 

Install the required dependencies:
```bash
  pip install reportlab pillow
```
You’re now ready to run the project.
---

 
 