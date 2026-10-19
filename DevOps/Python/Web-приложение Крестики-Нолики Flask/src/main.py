from __future__ import annotations

from di import Container


def build_app() -> Flask:  # type: ignore[name-defined]
    container = Container()
    return container.build_app()


if __name__ == "__main__":
    app = build_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
