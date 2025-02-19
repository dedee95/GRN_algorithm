import pandas as pd
import argparse
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

def main(expression_file, tf_file, output_file):
    # load data
    mtx = pd.read_csv(expression_file, sep="\t")
    tf_list = load_tf_names(tf_file)

    # Run GRNBoost2
    network = grnboost2(expression_data=mtx, tf_names=tf_list, seed=123)

    # Save the output file
    network.to_csv(output_file, sep='\t', header=False, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GRNBoost2 on expression data")
    parser.add_argument("expression_file", help="Path to the expression data file (TSV format)")
    parser.add_argument("tf_file", help="Path to the transcription factors list (TSV format)")
    parser.add_argument("output_file", help="Name of the output file (TSV format)")
    args = parser.parse_args()
    main(args.expression_file, args.tf_file, args.output_file)