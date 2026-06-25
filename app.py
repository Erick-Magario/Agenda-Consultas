import csv
import os
from datetime import datetime, date, timedelta
from tkinter import messagebox, END, Listbox
import customtkinter as ctk

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
    messagebox.showinfo("Sucesso", "Consulta salva com sucesso!")


def editar_consulta():
    selecionado = lista.curselection()

    if not selecionado:
        messagebox.showerror("Erro", "Selecione uma consulta para editar.")
        return

    indice = selecionado[0]

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))

    funcionario = linhas[indice]["funcionario"]
    consulta = linhas[indice]["consulta"]

    entrada_funcionario.delete(0, END)
    entrada_funcionario.insert(0, funcionario)

    entrada_consulta.delete(0, END)
    entrada_consulta.insert(0, consulta)

    del linhas[indice]

    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["funcionario", "consulta"])

        for linha in linhas:
            escritor.writerow([linha["funcionario"], linha["consulta"]])

    carregar_consultas()


def excluir_consulta():
    selecionado = lista.curselection()

    if not selecionado:
        messagebox.showerror("Erro", "Selecione uma consulta para excluir.")
        return

    confirmar = messagebox.askyesno(
        "Confirmar exclusão",
        "Tem certeza que deseja excluir esta consulta?"
    )

    if not confirmar:
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

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Agenda de Consultas")
janela.geometry("600x560")
janela.resizable(False, False)

titulo = ctk.CTkLabel(
    janela,
    text="Agenda de Consultas",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=20)

frame_formulario = ctk.CTkFrame(janela)
frame_formulario.pack(pady=10, padx=30, fill="x")

label_funcionario = ctk.CTkLabel(
    frame_formulario,
    text="Nome do funcionário:"
)
label_funcionario.pack(pady=(15, 5))

entrada_funcionario = ctk.CTkEntry(
    frame_formulario,
    width=400,
    placeholder_text="Ex: João Silva"
)
entrada_funcionario.pack(pady=5)

label_consulta = ctk.CTkLabel(
    frame_formulario,
    text="Data da consulta (AAAA-MM-DD):"
)
label_consulta.pack(pady=(10, 5))

entrada_consulta = ctk.CTkEntry(
    frame_formulario,
    width=400,
    placeholder_text="Ex: 2026-08-25"
)
entrada_consulta.pack(pady=5)

botao_salvar = ctk.CTkButton(
    frame_formulario,
    text="Salvar Consulta",
    command=salvar_consulta,
    width=200
)
botao_salvar.pack(pady=20)

label_lista = ctk.CTkLabel(
    janela,
    text="Consultas cadastradas:",
    font=("Arial", 15, "bold")
)
label_lista.pack(pady=(15, 5))

lista = Listbox(
    janela,
    width=65,
    height=8
)
lista.pack(pady=5)

frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
frame_botoes.pack(pady=15)

botao_editar = ctk.CTkButton(
    frame_botoes,
    text="✏ Editar",
    command=editar_consulta,
    width=120
)
botao_editar.pack(side="left", padx=10)

botao_excluir = ctk.CTkButton(
    frame_botoes,
    text="🗑 Excluir",
    command=excluir_consulta,
    width=120,
    fg_color="#c0392b",
    hover_color="#922b21"
)
botao_excluir.pack(side="left", padx=10)

carregar_consultas()
verificar_alertas()

janela.mainloop()