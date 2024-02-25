from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

if TYPE_CHECKING:
    pass

from apps import init_app

app = init_app()

if __name__ == "__main__":
    app.run()
