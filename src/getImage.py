from flask import Flask, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os



# Changed file path to diff folder with ai
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, '../RecipeAWaste', 'public')
# end of ai


#rest was aided with youtube tutorial for flask
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'buns'



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# checks allowed files and only allows photos to be uploaded for the ai to process
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# html sends either get or post command to this backend code.
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    file_url = None
    if request.method == 'POST':
        if 'photo' not in request.files:
            return render_template('uploadDish.html', error="No file part")
        file = request.files['photo']
        if file.filename == '':
            return render_template('uploadDish.html', error="No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_url = url_for('uploaded_file', filename=filename)
        else:
            return render_template('uploadDish.html', error="File type not allowed")
    return render_template('uploadDish.html', file_url=file_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
