activate_this = '/home/c/ci50266/regofapp/public_html/venv/bin/activate_this.py'
exec(open(activate_this).read())

import sys
sys.path.insert(0, '/home/c/ci50266/regofapp/public_html/regofapp/')
sys.path.insert(1, '/home/c/ci50266/regofapp/public_html/venv/lib/python3.10/site-packages/')
from app import app as application
