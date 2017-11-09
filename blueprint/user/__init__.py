from flask import Blueprint

user=Blueprint('user',__name__)

from user_views import user_tom,user_lucy