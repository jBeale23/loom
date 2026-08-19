# Loom

A POSIX compliant pipeline for designing consensus proteins, automatically weaving them from input FASTA files.

This pipeline follows the methodology outlined in [Sternke et. al., 2019](https://www.pnas.org/doi/full/10.1073/pnas.1816707116).

# Installation

## Dependencies

1. Python >= 3.12
2. Numpy >= 2.0.0
3. cd-hit
4. mafft
5. gzip (If using .gz compressed input files)

Install the required dependencies, then clone the repository and run `sudo make install` to install `loom` and its completions for all users.

Alternatively, put `loom` anywhere on your $PATH and make sure it's executable, and everything will function once the dependencies are installed.
You can manually install tab completions for Bash and Zsh by sourcing the included `loom-completion` file in your corresponding shell rc file.

# Usage

Coming soon

# Uninstallation

If you installed with `sudo make install`, you can remove `loom` and its completions with `sudo make uninstall`.

Alternatively, just delete `loom` and its completion files if you installed it manually.

# License

Loom is licensed under the terms of the [GNU GPL v3.0 License](LICENSE).
