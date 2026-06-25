from datetime import datetime, date, timedelta
from tkinter import Tk, messagebox

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
        janela = Tk()
        janela.withdraw()

        mensagem = "Consultas próximas:\n\n" + "\n".join(avisos)

        messagebox.showwarning("Aviso de consulta médica", mensagem)

        janela.destroy()


verificar_alertas()