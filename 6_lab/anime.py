from flask import Flask
from jikanpy import Jikan

app = Flask(__name__)
jikan = Jikan()

@app.route('/')
def home():
    anime = jikan.anime(1)  
    data = anime['data']
    return f"Назва аніме: {data['title']}<br>Тип: {data['type']}<br>Епізоди: {data['episodes']}"


if __name__ == '__main__':
    app.run(debug=True)