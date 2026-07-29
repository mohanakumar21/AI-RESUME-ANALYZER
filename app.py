from flask import Flask, render_template
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)
print("Root Path:", app.root_path)
print("Template Folder:", app.template_folder)
print("Template Exists:", (BASE_DIR / "templates" / "index.html").exists())

print("Current Working Directory:", os.getcwd())
print("App Root:", app.root_path)
print("Template Folder:", os.path.join(app.root_path, "templates"))

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)