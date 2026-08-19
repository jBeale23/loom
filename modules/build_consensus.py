#!/usr/bin/env python3
"""Builds a consensus protein from an aligned FASTA file, removing positions with gap frequency above a user defined value."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .constants import AMINO_ACID_ALPHABET_WITH_GAPS_L
from .helpers import is_fasta_aligned, marginal_frequencies, read_fasta


def main() -> None:
    """CLI for consensus building script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, metavar="Input FASTA file", help="Input FASTA file.", required=True)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        metavar="Output FASTA file",
        default=None,
        help="Output consensus FASTA filename. Defaults to {INPUT_FILE}_consensus.fasta",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        metavar="Gap frequency threshold",
        default=0.5,
        help="Gap frequecy threshold used to define a consensus position. Defaults to 0.5, removing positions with higher gap frequency. Must be a value between 0 and 1.",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        metavar="Quality Control log path",
        default=None,
        help="Log file used to record quality control metrics. Defaults to {INPUT_FILE}_consensus.log.",
    )
    args = parser.parse_args()

    if args.threshold > 1 or args.threshold < 0:
        msg = f"Filtering threshold: {args.threshold} was not in range [0...1]."
        raise ValueError(msg)

    output_fasta = args.output if args.output is not None else Path(f"{args.input.stem}_consensus.fasta")
    log_file = args.log if args.log is not None else Path(f"{args.input.stem}_consensus.log")

    try:
        with args.input.open("r") as fasta:
            seqs, __ = read_fasta(fasta, strip_gaps=False)

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

    if not is_fasta_aligned(seqs):
        msg = f"Input file: {args.input} contains unaligned sequences."
        raise ValueError(msg)

    marginals = marginal_frequencies(seqs)

    consensus_sequence = "".join(
        [
            AMINO_ACID_ALPHABET_WITH_GAPS_L[np.argmax(position[:-1])]
            for position in marginals
            if position[-1] < args.threshold
        ]
    )

    with output_fasta.open("a") as outfile:
        outfile.write(f">{output_fasta.stem}\n{consensus_sequence}\n")

    with log_file.open("w") as log:
        log.write(f"Determined consensus sequence for: {args.input}\n")
        log.write(f"Gap frequency threshold: {args.threshold}\n")
        log.write(f"Wrote consensus sequence to: {output_fasta}\n")


if __name__ == "__main__":
    main()
