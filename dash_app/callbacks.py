import os
from dash import Input, Output

PROCESSED_FOLDER = "processed"


def register_callbacks(app):

    @app.callback(
        Output("output-div", "children"),
        Input("load-btn", "n_clicks")
    )
    def load_latest_result(n_clicks):

        if not n_clicks:
            return "Click the button to load OCR results."

        if not os.path.exists(PROCESSED_FOLDER):
            return "Processed folder not found."

        # Only keep real TXT files (ignore directories)
        txt_files = [
            f for f in os.listdir(PROCESSED_FOLDER)
            if f.endswith(".txt")
            and os.path.isfile(os.path.join(PROCESSED_FOLDER, f))
        ]

        if not txt_files:
            return "No OCR results found."

        # Get most recent OCR file
        latest_file = max(
            txt_files,
            key=lambda f: os.path.getmtime(
                os.path.join(PROCESSED_FOLDER, f)
            )
        )

        latest_path = os.path.join(PROCESSED_FOLDER, latest_file)

        with open(latest_path, "r", encoding="utf-8") as f:
            return f.read()
