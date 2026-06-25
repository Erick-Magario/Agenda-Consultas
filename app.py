from datetime import datetime, date, timedelta
from tkinter import messagebox, END, Listbox
import customtkinter as ctk

from banco import (
    criar_tabela,
    adicionar_consulta,
    listar_consultas,
    excluir_consulta,
    editar_consulta
)

id_selecionado = None


def carregar_consultas():
    lista.delete(0, END)

    consultas = listar_consultas()

    for consulta in consultas:
        id_consulta = consulta[0]
        funcionario = consulta[1]
        data_consulta = consulta[2]

        data_formatada = datetime.strptime(data_consulta, "%Y-%m-%d").strftime("%d/%m/%Y")

        lista.insert(
            END,
            f"{id_consulta} | {funcionario} - {data_formatada}"
        )


def limpar_campos():
    global id_selecionado

    entrada_funcionario.delete(0, END)
    entrada_consulta.delete(0, END)
    id_selecionado = None
    botao_salvar.configure(text="Salvar Consulta")


def salvar_consulta():
    global id_selecionado

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

    if id_selecionado is None:
        adicionar_consulta(funcionario, consulta)
        messagebox.showinfo("Sucesso", "Consulta cadastrada com sucesso!")
    else:
        editar_consulta(id_selecionado, funcionario, consulta)
        messagebox.showinfo("Sucesso", "Consulta editada com sucesso!")

    limpar_campos()
    carregar_consultas()


def selecionar_para_editar():
    global id_selecionado

    selecionado = lista.curselection()

    if not selecionado:
        messagebox.showerror("Erro", "Selecione uma consulta para editar.")
        return

    texto = lista.get(selecionado[0])

    id_consulta = int(texto.split("|")[0].strip())

    consultas = listar_consultas()

    for consulta in consultas:
        if consulta[0] == id_consulta:
            id_selecionado = consulta[0]
            funcionario = consulta[1]
            data_consulta = consulta[2]

            entrada_funcionario.delete(0, END)
            entrada_funcionario.insert(0, funcionario)

            entrada_consulta.delete(0, END)
            entrada_consulta.insert(0, data_consulta)

            botao_salvar.configure(text="Salvar Alterações")
            return


def excluir_selecionada():
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

    texto = lista.get(selecionado[0])
    id_consulta = int(texto.split("|")[0].strip())

    excluir_consulta(id_consulta)

    limpar_campos()
    carregar_consultas()

    messagebox.showinfo("Sucesso", "Consulta excluída com sucesso!")


def verificar_alertas():
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
        mensagem = "Consultas próximas:\n\n" + "\n".join(avisos)
        messagebox.showwarning("Aviso de consulta médica", mensagem)


criar_tabela()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Agenda de Consultas")
janela.geometry("650x700")
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
    width=430,
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
    width=430,
    placeholder_text="Ex: 2026-08-25"
)
entrada_consulta.pack(pady=5)

botao_salvar = ctk.CTkButton(
    frame_formulario,
    text="Salvar Consulta",
    command=salvar_consulta,
    width=220
)
botao_salvar.pack(pady=(15, 8))

botao_limpar = ctk.CTkButton(
    frame_formulario,
    text="Limpar Campos",
    command=limpar_campos,
    width=220,
    fg_color="#7f8c8d",
    hover_color="#626567"
)
botao_limpar.pack(pady=(0, 15))

label_lista = ctk.CTkLabel(
    janela,
    text="Consultas cadastradas:",
    font=("Arial", 15, "bold")
)
label_lista.pack(pady=(15, 5))

lista = Listbox(
    janela,
    width=75,
    height=6
)
lista.pack(pady=5)

frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
frame_botoes.pack(fill="x", padx=40, pady=15)

botao_editar = ctk.CTkButton(
    frame_botoes,
    text="✏ Editar",
    command=selecionar_para_editar,
    width=180,
    height=40
)
botao_editar.pack(side="left", expand=True, padx=15)

botao_excluir = ctk.CTkButton(
    frame_botoes,
    text="🗑 Excluir",
    command=excluir_selecionada,
    width=180,
    height=40,
    fg_color="#c0392b",
    hover_color="#922b21"
)
botao_excluir.pack(side="right", expand=True, padx=15)

carregar_consultas()
verificar_alertas()

janela.mainloop()