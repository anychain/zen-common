"""compatiblity extensions for SQLAlchemy versions.

Elements within this module provide SQLAlchemy features that have been
added at some point but for which oslo.db provides a compatible versions
for previous SQLAlchemy versions.

"""
from common.db.sqlalchemy.compat import handle_error as _h_err

# trying to get: "from common.db.sqlalchemy import compat; compat.handle_error"
# flake8 won't let me import handle_error directly
handle_error = _h_err.handle_error

__all__ = ['handle_error']
