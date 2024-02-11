from flask import Flask, render_template, request

app = Flask(__name__)

submitted_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_form():
    text_input = request.form.get('text_input')
    file_input = request.files.get('file_input')

    submitted_data.append({
        'text_input': text_input,
        'file_input_filename': file_input.filename if file_input else None,
    })


if __name__ == '__main__':
    app.run(debug=True)

