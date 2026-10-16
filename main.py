from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "credmais_chave_local"

taxa_atual = {
    "ano": "",
    "juros": ""
}

taxas_cadastradas = []

@app.route("/")
def inicio():
    return redirect(url_for("editar_taxa"))

@app.route("/taxas/editar", methods=["GET", "POST"])
def editar_taxa():
    global taxa_atual

    if request.method == "POST":
        ano = request.form.get("ano")
        juros = request.form.get("juros")

        try:
            ano = int(ano)
            juros = float(juros)

            if ano < 1980 or ano > 2050 or juros < 0:
                flash("Confira o ano e o valor da taxa.", "erro")
                return redirect(url_for("editar_taxa"))

            taxa_atual = {
                "ano": ano,
                "juros": juros
            }

            flash("Taxa atualizada com sucesso!", "sucesso")

        except ValueError:
            flash("Informe um ano e uma taxa válidos.", "erro")

        return redirect(url_for("editar_taxa"))

    return render_template("editar_taxas.html", taxa=taxa_atual)

@app.route("/taxas/cadastrar", methods=["GET", "POST"])
def cadastrar_taxa():
    taxa = {
        "ano": "",
        "juros": ""
    }

    if request.method == "POST":
        ano = request.form.get("ano")
        juros = request.form.get("juros")

        try:
            ano = int(ano)
            juros = float(juros)

            if ano < 1980 or ano > 2050 or juros < 0:
                flash("Informe um ano entre 1980 e 2050 e uma taxa válida.", "erro")
                return redirect(url_for("cadastrar_taxa"))

            ano_existente = False

            for taxa in taxas_cadastradas:
                if taxa["ano"] == ano:
                    ano_existente = True

            if ano_existente:
                flash("Já existe uma taxa cadastrada para esse ano.", "erro")
                return redirect(url_for("cadastrar_taxa"))

            nova_taxa = {
                "ano": ano,
                "juros": juros
            }

            taxas_cadastradas.append(nova_taxa)

            flash("Taxa cadastrada com sucesso!", "sucesso")
            return redirect(url_for("cadastrar_taxa"))

        except ValueError:
            flash("Informe um ano e uma taxa válidos.", "erro")
            return redirect(url_for("cadastrar_taxa"))

    return render_template("cadastrar_taxas.html", taxa=taxa)

@app.route("/taxas")
def listar_taxas():
    return render_template("listar_taxas.html", taxas=taxas_cadastradas)

if __name__ == "__main__":
    app.run(debug=True)