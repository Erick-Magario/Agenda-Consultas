from datetime import datetime, date, timedelta
from tkinter import Tk, Label, Button
import winsound

from banco import criar_tabela, listar_consultas


def verificar_alertas():
    criar_tabela()

    hoje = date.today()
    avisos = []

    consultas = listar_consultas()

    for consulta in consultas:
        funcionario = consulta[1]
        consulta_texto = consulta[2]

        data_consulta = datetime.strptime(consulta_texto, "%Y-%m-%d").date()
        data_aviso = data_consulta - timedelta(days=30)

        if hoje == data_aviso:
            avisos.append(
                f"{funcionario} tem consulta em {data_consulta.strftime('%d/%m/%Y')}"
            )

    if avisos:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

        janela = Tk()
        janela.title("Aviso de consulta médica")
        janela.geometry("450x250")
        janela.resizable(False, False)

        janela.attributes("-topmost", True)
        janela.lift()
        janela.focus_force()

        mensagem = "⚠️ Consultas próximas\n\n" + "\n".join(avisos)

        Label(
            janela,
            text=mensagem,
            font=("Arial", 12),
            wraplength=400,
            justify="center"
            ).pack(pady=35)

        Button(
            janela,
            text="OK",
            font=("Arial", 11),
            width=12,
            command=janela.destroy
        ).pack(pady=10)

        janela.mainloop()


verificar_alertas()