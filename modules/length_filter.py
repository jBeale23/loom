#!/usr/bin/env python3
"""Applies length filtering and gap stripping to the input FASTA file, removing sequences which deviate from the median sequence length by more than the specified threshold."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .helpers import calculate_lengths, read_fasta


def main() -> None:
    """CLI for length filtering script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, metavar="Input FASTA file", help="Input FASTA file.", required=True)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        metavar="Output FASTA file",
        default=None,
        help="Output FASTA filename. Defaults to {INPUT_FILE}_lf.fasta",
    )
    parser.add_argument(
        "-d",
        "--outdir",
        type=Path,
        metavar="Output directory",
        default=None,
        help="Output directory path. Defaults to current working directory.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        metavar="Length filtering threshold",
        default=0.3,
        help="Sequence length filtering threshold value. Defaults to 0.3, removing sequences that deviate +/- 30%% from median sequence length of set. Must be a value between 0 and 1.",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        metavar="Quality Control log path",
        default=None,
        help="Log file used to record quality control metrics. Defaults to {INPUT_FILE}_lf.log.",
    )
    args = parser.parse_args()

    if args.threshold > 1 or args.threshold < 0:
        msg = f"Filtering threshold: {args.threshold} was not in range [0...1]."
        raise ValueError(msg)

    output_directory = args.outdir if args.outdir is not None else Path.cwd()
    output_fasta = (
        output_directory.joinpath(args.output)
        if args.output is not None
        else output_directory.joinpath(Path(f"{args.input.stem}_lf.fasta"))
    )
    log_file = args.log if args.log is not None else Path(f"{args.input.stem}_lf.log")

    try:
        with args.input.open("r") as fasta:
            seqs, ids = read_fasta(fasta, strip_gaps=True)

    except PermissionError as err:
        msg = f"Input file: {args.input} was not readable."
        raise PermissionError(msg) from err
    except FileNotFoundError as err:
        msg = f"Input file: {args.input} does not exist."
        raise FileNotFoundError(msg) from err

    num_seqs = len(seqs)
    if num_seqs == 0:
        msg = f"Input file: {args.input} was not in FASTA format."
        raise ValueError(msg)

    lengths = calculate_lengths(seqs)

    med_length = int(np.median(lengths))
    lower_threshold = round(med_length - med_length * args.threshold)
    upper_threshold = round(med_length + med_length * args.threshold)

    out_fasta = []
    for length, identifier, sequence in zip(lengths, ids, seqs, strict=True):
        if length >= lower_threshold and length <= upper_threshold:
            out_fasta.append(f"{identifier}\n{sequence}\n")

    num_seqs_out = len(out_fasta)

    with output_fasta.open("w") as outfile:
        outfile.writelines(out_fasta)

    with log_file.open("w") as log:
        log.write(f"Filtered sequence set: {args.input}\n")
        log.write(f"Sequence length filtering threshold: {args.threshold}\n")
        log.write(f"Number of sequences in initial alignment: {num_seqs}\n")
        log.write(f"Median sequence length: {med_length} residues\n")
        log.write(f"Sequence length lower boundary: {lower_threshold} residues\n")
        log.write(f"Sequence length upper boundary: {upper_threshold} residues\n")
        log.write(f"Number of sequences in final alignment: {num_seqs_out}\n")
        log.write(f"Wrote length filtered sequence set to: {output_fasta}\n")


if __name__ == "__main__":
    main()
