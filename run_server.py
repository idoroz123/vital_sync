import os
from app import app


PORT = os.environ.get("PORT", 9090)


def run_server_flask():
    app.run(host="0.0.0.0", port=PORT, debug=True)


if __name__ == "__main__":
    run_server_flask()
