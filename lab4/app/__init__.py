from flask import Flask

app = Flask(__name__)
app.secret_key="djlsaghladshgkdashkgldsh"

from app import views