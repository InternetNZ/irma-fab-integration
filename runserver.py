#!/usr/bin/env python3
"""
Runs the application
"""

from fab.main import app

app.run('0.0.0.0', 5050, debug=True)
