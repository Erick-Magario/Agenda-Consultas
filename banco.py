import sqlite3

BANCO = "consultas.db"


def conectar():
    return sqlite3.connect(BANCO)


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario TEXT NOT NULL,
            consulta TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def adicionar_consulta(funcionario, consulta):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO consultas (funcionario, consulta) VALUES (?, ?)",
        (funcionario, consulta)
    )

    conexao.commit()
    conexao.close()


def listar_consultas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, funcionario, consulta
        FROM consultas
        ORDER BY consulta
    """)

    dados = cursor.fetchall()

    conexao.close()

    return dados


def excluir_consulta(id_consulta):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM consultas WHERE id = ?",
        (id_consulta,)
    )

    conexao.commit()
    conexao.close()


def editar_consulta(id_consulta, funcionario, consulta):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE consultas
        SET funcionario = ?, consulta = ?
        WHERE id = ?
    """, (funcionario, consulta, id_consulta))

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabela()
    print("Banco pronto!")