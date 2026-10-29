import sys
from .app import DlssSwapperApp


def main() -> int:
    app = DlssSwapperApp()
    return app.run(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())