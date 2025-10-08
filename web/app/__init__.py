from flask import Flask, request, render_template

app = Flask(__name__)

from app import routes

app.config.from_object('config')