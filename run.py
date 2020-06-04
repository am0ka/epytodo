#!/usr/bin/env python3

from app import views
from app import app


if __name__ == "__main__":
    app.secret_key = "secret_unique_key"
    app.run(host='0.0.0.0')
