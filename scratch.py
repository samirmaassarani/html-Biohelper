from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import time

app = Flask(__name__)


class Biohelper:
    def __init__(self, sequence):
        self.sequence = sequence.upper()

    def check_seq(self):
        return self.sequence

    def get_complement(self):
        complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        try:
            return ''.join(complement_dict[base] for base in self.sequence)
        except KeyError:
            return None

    def validate_sequence(self):
        valid_bases = set('ATCG')
        return all(base in valid_bases for base in self.sequence)

    def genome_stats(self):
        stats = {}
        stats['length'] = len(self.sequence)
        stats['g_count'] = self.sequence.count("G")
        stats['c_count'] = self.sequence.count("C")
        stats['gc_count'] = stats['g_count'] + stats['c_count']

        if stats['length'] > 0:
            stats['gc_percent'] = (stats['gc_count'] / stats['length']) * 100
        else:
            stats['gc_percent'] = 0

        # Generate GC plot
        plt.figure(figsize=(8, 4))
        plt.plot([i for i in range(stats['length'])],
                 [self.sequence[:i + 1].count('G') + self.sequence[:i + 1].count('C')
                  for i in range(stats['length'])],
                 color='blue')
        plt.title('GC Content Accumulation')
        plt.xlabel('Position in Sequence')
        plt.ylabel('GC Count')
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        stats['gc_plot'] = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

        return stats

    def fasta_format(self, file_name):
        fasta = f">{file_name}\n"
        for i in range(0, len(self.sequence), 60):
            fasta += self.sequence[i:i + 60] + "\n"
        return fasta


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sequence = request.form['sequence'].strip().upper()

        if not sequence:
            return render_template('index.html', error='Please enter a sequence')

        bio = Biohelper(sequence)

        if not bio.validate_sequence():
            return render_template('index.html',
                                   error='Invalid sequence - use only A, T, C, G')

        # Determine which analyses were requested
        do_complement = 'complement' in request.form
        do_fasta = 'fasta' in request.form
        do_gc = 'gc_content' in request.form

        results = {
            'sequence': sequence,
            'do_complement': do_complement,
            'do_fasta': do_fasta,
            'do_gc': do_gc
        }

        if do_complement:
            results['complement'] = bio.get_complement()

        if do_gc:
            results.update(bio.genome_stats())

        if do_fasta:
            results['fasta'] = bio.fasta_format("user_sequence")

        return render_template('index.html', **results)

    return render_template('index.html')


@app.route('/download')
def download():
    fasta = request.args.get('fasta')
    return send_file(
        BytesIO(fasta.encode()),
        mimetype='text/plain',
        as_attachment=True,
        download_name=f'sequence_{int(time.time())}.fasta'
    )


if __name__ == '__main__':
    app.run(debug=True)