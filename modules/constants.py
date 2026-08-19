"""Amino acid alphabets for use in consensus protein design."""

from typing import LiteralString

AMINO_ACID_ALPHABET: LiteralString = "ACDEFGHIKLMNPQRSTVWY"
AMINO_ACID_ALPHABET_WITH_GAPS: LiteralString = "ACDEFGHIKLMNPQRSTVWY-"
AMINO_ACID_ALPHABET_L: list[LiteralString] = list(AMINO_ACID_ALPHABET)
AMINO_ACID_ALPHABET_WITH_GAPS_L: list[LiteralString] = list(AMINO_ACID_ALPHABET_WITH_GAPS)
