from flask import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def landing():
    return render_template('landing.html')


if __name__ == '__main__':
    app.run(debug=True)
