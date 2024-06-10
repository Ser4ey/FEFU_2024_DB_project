from flask import Flask, render_template
from repository import Repository

app = Flask(__name__)

repo = Repository()


@app.route('/')
def index():
    insects = repo.get_all_insects()
    return render_template('insects_catalog.html', insects=insects)


@app.route('/insect/<int:id_>')
def insect(id_):
    insect = repo.get_insect(id_)
    return render_template('insect_page.html', insect=insect)


if __name__ == '__main__':
    app.run(debug=True)

