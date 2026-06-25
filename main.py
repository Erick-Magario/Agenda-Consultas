import csv
from datetime import datetime, date, timedelta
from tkinter import Tk, messagebox

ARQUIVO = "consultas.csv"

hoje = date.today()
avisos = []

with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        funcionario = linha["funcionario"]
        consulta_texto = linha["consulta"]

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

# teste