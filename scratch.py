from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seq = request.form['sequence'].upper()  # Get and uppercase the sequence
        complement = get_complement(seq)  # Generate complement
        return render_template('result.html',
                            sequence=seq,
                            complement=complement)
    return render_template('index.html')

@app.route('/display/<seq>')
def print_sequence(seq):
    return render_template('display.html', sequence=seq)

def check_seq():
    seq= get_input
    seq= seq.upper()
    return seq

def get_complement():
    seq=get_input
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement_dict[base] for base in seq)


if __name__ == '__main__':
    app.run(debug=True)