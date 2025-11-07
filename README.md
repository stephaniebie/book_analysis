# Book Analysis
CU Boulder DTSC 5501 Group Project #2: Data Structures in Action Table of Contents & Text Analysis

## Roles & Responsibilities

# TODO

Written and maintained by Group 11:
- **Abhinav Mehrotra**:
- **Atharva Zodpe**:
- **Karan Cheemalapati**: Q1 traversal method implementation
- **Stephanie Bie**: Q1 data structure design, packaging

## Install

```bash
git clone git@github.com:stephaniebie/book_analysis.git
```

Create and enter a virtual environment (Windows):

```bash
python -m venv venv
source venv/Scripts/activate
```

Once in the environment, install the package:

```bash
pip install .
```

### For Developers

Install the package in editable mode:

```bash
pip install -e .[dev]
```

Install a kernel for use with Jupyter notebooks:

```bash
python -m ipykernel install --user --name=book_analysis
```

Optionally, run `black .` prior to pushing to ensure uniform formatting.

## Testing

Use the following command to run the unit tests:

```bash
pytest tests
```

## References & Sources
- <a href="https://aima.cs.berkeley.edu/contents.html"><i>Artificial Intelligence: A Modern Approach</i></a> by Stuart Russell and Peter Norvig
- <i>Notre-Dame de Paris</i> by Victor Hugo, translated by Isabel F. Hapgood (via <a href="https://www.gutenberg.org/files/2610/2610-h/2610-h.htm">Project Gutenberg</a>)