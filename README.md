# GRN_algorithm

This repository contain 2 python files: `grnboost2.py` and `network_visualization.py`

## `grnboost2.py`
```
usage: grnboost2.py [-h] expression_file tf_file output_file

Run GRNBoost2 on expression data

positional arguments:
  expression_file  Path to the expression data file (TSV format)
  tf_file          Path to the transcription factors list (TSV format)
  output_file      Name of the output file (TSV format)

optional arguments:
  -h, --help       show this help message and exit
```

## `network_visualization.py`
```
usage: network_visualization.py [-h] network_file output_html

Visualize network data and export to HTML

positional arguments:
  network_file  Path to the network file (TSV format)
  output_html   Name of the output HTML file

optional arguments:
  -h, --help    show this help message and exit
```

