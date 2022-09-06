from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
from shogi_lib import shogi





def index(request, htmlname):
    return render(request, f"jobstatic/{htmlname}")



