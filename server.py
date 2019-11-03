from flask import Flask, render_template
import models
app = Flask(__name__,template_folder=root_path,root_path=root_path)

@app.route("/")
def home():
    obj=models.Models()
    

if __name__ == "__main__":
    app.run(debug=True)