activate_this = '/home/u/user/regofapp/venv/bin/activate_this.py'
exec(open(activate_this).read())

import sys
sys.path.insert(0, '/home/u/user/regofapp/')
sys.path.insert(1, '/home/u/user/regofapp/venv/lib/python3.10/site-packages/')
from app import app as application