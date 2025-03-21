from flask import Flask, request, jsonify

import sqlite3


app = Flask(__name__)


@app.route("/pague")
def exiba_mensagem():
    return "<h2>Pagar as pessoas, faz bem as pessoas! </h2>"


# @app.route("/devedora")
# def mensagem_do_calote():
#     return "<h3>Pessoas que não pagam, é triste viu...</h3>"


# se o app.py foro arquivo principal da API:
# Execute o app.run com o modo de debug ativado


# iniciar o banco de dados
def init_db():
    # Conecte o sqlite3 no arquivo database.db com a variável conn(connection)
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
        """)


init_db()


@app.route("/doar", methods=["POST"])
def doar():

    dados = request.get_json()

    # print(f" AQUI ESTÃO OS DADOS RETORNADOS DO CLIENTE {dados}")

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"Erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo,categoria,autor,image_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
""")

    conn.commit()  # ele salva toda e qualquer alteração feita no banco de dados

    return jsonify({"mensagem": "Livro Cadastrado com sucesso"}), 201
    # jsonify ele pega a mensagem e retorna em json pro usuário

# agora a parte que o cliente puxa os livros


@app.route("/livros", methods=["GET"])
def listar_livros():

    with sqlite3.connect("database.db") as conn:
        # SELECT lista os livros, fetchall converte informações do banco d dados de sql pra python
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

        livros_formatados = []

        for item in livros:
            dicionario_livros = {
                "id": item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor": item[3],
                "image_url": item[4]
            }
            livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados), 200


if __name__ == "__main__":
    app.run(debug=True)
