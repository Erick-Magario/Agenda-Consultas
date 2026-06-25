import csv
from tkinter import Tk, Label, Entry, Button, messagebox, END

ARQUIVO = "consultas.csv"

def salvar_consulta():
    funcionario = entrada_funcionario.get()
    consulta = entrada_consulta.get()

    if funcionario == "" or consulta == "":
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"\n{funcionario},{consulta}")

    messagebox.showinfo("Sucesso", "Consulta cadastrada com sucesso!")

    entrada_funcionario.delete(0, END)
    entrada_consulta.delete(0, END)


janela = Tk()
janela.title("Cadastro de Consultas")
janela.geometry("350x200")

Label(janela, text="Nome do funcionário:").pack(pady=5)
entrada_funcionario = Entry(janela, width=35)
entrada_funcionario.pack()

Label(janela, text="Data da consulta (AAAA-MM-DD):").pack(pady=5)
entrada_consulta = Entry(janela, width=35)
entrada_consulta.pack()

Button(janela, text="Salvar Consulta", command=salvar_consulta).pack(pady=20)

janela.mainloop()