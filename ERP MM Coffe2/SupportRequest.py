import smtplib
from email.mime.text import MIMEText

def enviar_email(msg, messagebox):
    # Configurações do e-mail
    sender_email = "oenhacker123@gmail.com"  # Substitua pelo seu email
    receiver_email = "gabrielpadawan912@gmail.com"  # Substitua pelo email do destinatário
    password = "uxvw jhij gdxa ryxz"  # Substitua pela sua senha
    subject = "Reuqisição de Suporte Técnico do ERP MM Coffe"
    body = msg

    # Cria a mensagem
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    try:
        # Conecta ao servidor SMTP do Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        messagebox.showinfo("Sucesso",
                            "E-mail enviado com sucesso!")
    except:
        messagebox.showerror("Erro",
        "Falha ao conectar ao servidor. Por favor, cheque sua conexão à rede!")