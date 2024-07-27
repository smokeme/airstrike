from flask import Flask, request, make_response, render_template, send_from_directory


app = Flask(__name__, static_url_path='', static_folder="static")

@app.route("/")
def index():
    # Serve the files from the build folder
    return send_from_directory("build", "index.html")

# static files
@app.route("/static/<path:path>")
def static_file(path):
    return send_from_directory("build/static", path)

# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory("build", "404.html")

if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0", port=23001)