import sys
import os

path = os.path.abspath(__file__)
path = os.path.abspath(os.path.join(path, os.pardir))
path = os.path.abspath(os.path.join(path, os.pardir))
path = os.path.abspath(os.path.join(path, os.pardir))
sys.path.append(path)

from Backend.server.app import app
