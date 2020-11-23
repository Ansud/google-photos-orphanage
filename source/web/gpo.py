"""
Copyright: Copyright 2020 Anton Zelenov

This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
"""

from web.app import create_application
from web.api import api_blueprint


def main():
    application = create_application()
    application.register_blueprint(api_blueprint)
    application.run()


if __name__ == '__main__':
    main()
