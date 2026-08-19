"""Assorted helper functions for building consensus proteins."""

from __future__ import annotations

import collections
import re
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from io import StringIO

    from numpy.typing import NDArray

from .constants import (
    AMINO_ACID_ALPHABET,
    AMINO_ACID_ALPHABET_WITH_GAPS,
    AMINO_ACID_ALPHABET_WITH_GAPS_L,
)


def _clean_sequence(sequence: str, *, strip_gaps: bool = True) -> str:
    """Cleans a sequence so it only contains canonical amino acids.

    Arguments:
        sequence: A string representing an amino acid sequence.
        strip_gaps: If true, remove gaps from the amino acid sequence.

    Returns:
        A string containing only canonical amino acids. Gaps are included if strip_gaps is not true.
    """
    if strip_gaps:
        return re.sub(rf"[^{AMINO_ACID_ALPHABET}]", "", sequence.upper())
    return re.sub(rf"[^{AMINO_ACID_ALPHABET_WITH_GAPS}]", "-", sequence.upper())


def read_fasta(fasta: StringIO, *, strip_gaps: bool = True) -> tuple[list[str], list[str]]:
    """Reads a FASTA file and returns a list of sequences and a list of ids from the file.

    Arguments:
        fasta: A StringIO object from which to read FASTA format identifiers and sequences.
        strip_gaps: If true, remove gaps from the read FASTA sequences.

    Returns:
        fasta_seqs: A list of sequences in the input FASTA file
        fasta_ids: A list of ids in the input FASTA file
    """
    fasta_seqs = []
    fasta_ids = []
    test_seq = ""
    for line in fasta:
        if line.startswith(">"):
            fasta_ids.append(line.rstrip())
            if len(test_seq) > 0:
                fasta_seqs.append(_clean_sequence(test_seq, strip_gaps=strip_gaps))
            test_seq = ""
        else:
            test_seq += line.rstrip()
    fasta_seqs.append(_clean_sequence(test_seq, strip_gaps=strip_gaps))
    return (fasta_seqs, fasta_ids)


def calculate_lengths(sequences: list[str]) -> list[int]:
    """Calculates the lengths of all sequences in a list and returns a list of all lengths."""
    return [len(i) for i in sequences]


def is_fasta_aligned(sequences: list[str]) -> bool:
    """Tests if FASTA file is aligned by determining if all sequences have the same length. Returns True or False."""
    lengths = calculate_lengths(sequences)
    return lengths.count(lengths[0]) == len(lengths)


def marginal_frequencies(sequences: list[str]) -> NDArray:
    """Determines the residue frequencies at each position in the alignment.

    Arguments:
        sequences: A list of sequences in the alignment

    Returns:
        matrix: A l by 21 matrix of amino acid frequencies, where l is the length of each sequence in the alignment.
    """
    len_seqs = len(sequences[0])
    matrix = np.zeros((len_seqs, len(AMINO_ACID_ALPHABET_WITH_GAPS_L)))
    for sequence_position in range(len_seqs):
        frequencies = collections.Counter(sequence[sequence_position] for sequence in sequences)
        for amino_acid in frequencies:
            residue_index = AMINO_ACID_ALPHABET_WITH_GAPS_L.index(amino_acid)
            matrix[sequence_position][residue_index] = frequencies[amino_acid] / sum(frequencies.values())
    return matrix
