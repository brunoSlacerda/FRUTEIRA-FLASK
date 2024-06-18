from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '1234'

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/estoqueFruteira'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Frutas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque_atual = db.Column(db.Integer, nullable=False)
    estoque_minimo = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Fruta %r>' % self.nome

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        estoque_atual = request.form['estoque_atual']
        estoque_minimo = request.form['estoque_minimo']

        fruta = Frutas.query.filter_by(nome=nome).first()
        if fruta:
            flash('Fruta já cadastrada!')
            return redirect(url_for('index'))
        
        nova_fruta = Frutas(nome=nome, preco=preco,estoque_atual = estoque_atual,estoque_minimo=estoque_minimo)
        db.session.add(nova_fruta)
        db.session.commit()

        flash('Fruta cadastrada com sucesso!')
        return redirect(url_for('index'))

    # Se a requisição for GET, renderiza o formulário de cadastro
    return render_template('cadastrar_produto.html')

@app.route('/adicionar_estoque')
def adicionar_estoque():
    lista = Frutas.query.order_by(Frutas.id)
    return render_template('adicionar_estoque.html', frutas = lista)

@app.route('/remover_estoque')
def remover_estoque():
    return render_template('remover_estoque.html')

@app.route('/excluir_produto')
def excluir_produto():
    return render_template('excluir_produto.html')

@app.route('/mostrar_estoque')
def mostrar_estoque():
    lista = Frutas.query.order_by(Frutas.id)
    
    return render_template('mostrar_estoque.html', frutas = lista)

@app.route('/editar/<int:id>')
def editar(id):
    frutas = Frutas.query.filter_by(id=id).first()
    return render_template('editar.html', frutas = frutas)

@app.route('/atualizar')
def atualizar():
    pass


# ----- INSTANCIA O SERVIDOR FLASK -----
if __name__ == '__main__':
    app.run(debug=True)
