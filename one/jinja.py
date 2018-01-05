from flask import Flask,render_template

app=Flask(__name__)

lists = [1,2,3]

@app.route("/<name>")
def index(name):
    return render_template("jinja_test.html", name=name, lists=lists)



@app.route("/if")
def ifdef():
    return render_template("jinja_test.html", lists=lists)


if __name__ == '__main__':
    app.run(debug=True)
