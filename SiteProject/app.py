from flask import Flask, render_template, request
from repository import Repository

app = Flask(__name__)

# Initialize the repository
repo = Repository()


@app.route('/')
def index():
    insects = repo.get_all_insects()
    return render_template('insects_catalog.html', insects=insects)


@app.route('/insect/<int:id_>')
def insect(id_):
    insect = repo.get_insect(id_)
    return render_template('insect_page.html', insect=insect)
#
#
# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         squad_id = request.form.get('squad_id')
#         family_id = request.form.get('family_id')
#         insects = repo.search_insects(squad_id, family_id)
#         return render_template('index.html', insects=insects)
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
