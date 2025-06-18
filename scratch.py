from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/input', methods=['GET', 'POST'])
def get_input():
    if request.method == 'POST':
        seq = request.form['sequence']
        return redirect(url_for('print_sequence', seq=seq))
    return render_template('input.html')

@app.route('/display/<seq>')
def print_sequence(seq):
    return render_template('display.html', sequence=seq)

if __name__ == '__main__':
    app.run(debug=True)