import csv
import os
from datetime import datetime, date, timedelta
from tkinter import Tk, Label, Entry, Button, messagebox, END, Listbox

ARQUIVO = "consultas.csv"


def garantir_arquivo():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            arquivo.write("funcionario,consulta\n")


def carregar_consultas():
    lista.delete(0, END)

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            funcionario = linha["funcionario"]
            consulta = linha["consulta"]

            data_formatada = datetime.strptime(consulta, "%Y-%m-%d").strftime("%d/%m/%Y")
            lista.insert(END, f"{funcionario} - {data_formatada}")


def salvar_consulta():
    funcionario = entrada_funcionario.get().strip()
    consulta = entrada_consulta.get().strip()

    if funcionario == "" or consulta == "":
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    try:
        datetime.strptime(consulta, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Erro", "Digite a data no formato AAAA-MM-DD.")
        return

    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{funcionario},{consulta}\n")

    entrada_funcionario.delete(0, END)
    entrada_consulta.delete(0, END)

    carregar_consultas()
    messagebox.showinfo("Sucesso", "Consulta cadastrada com sucesso!")


def excluir_consulta():
    selecionado = lista.curselection()

    if not selecionado:
        messagebox.showerror("Erro", "Selecione uma consulta para excluir.")
        return

    indice = selecionado[0]

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    del linhas[indice + 1]

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(linhas)

    carregar_consultas()
    messagebox.showinfo("Sucesso", "Consulta excluída com sucesso!")


def verificar_alertas():
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
        mensagem = "Consultas próximas:\n\n" + "\n".join(avisos)
        messagebox.showwarning("Aviso de consulta médica", mensagem)


garantir_arquivo()

janela = Tk()
janela.title("Agenda de Consultas")
janela.geometry("500x450")

Label(janela, text="Agenda de Consultas", font=("Arial", 16, "bold")).pack(pady=10)

Label(janela, text="Nome do funcionário:").pack()
entrada_funcionario = Entry(janela, width=40)
entrada_funcionario.pack(pady=5)

Label(janela, text="Data da consulta (AAAA-MM-DD):").pack()
entrada_consulta = Entry(janela, width=40)
entrada_consulta.pack(pady=5)

Button(janela, text="Salvar Consulta", command=salvar_consulta).pack(pady=10)

Label(janela, text="Consultas cadastradas:").pack(pady=5)

lista = Listbox(janela, width=55, height=10)
lista.pack(pady=5)

Button(janela, text="Excluir Consulta Selecionada", command=excluir_consulta).pack(pady=10)

carregar_consultas()
verificar_alertas()

janela.mainloop()