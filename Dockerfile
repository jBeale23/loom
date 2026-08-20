FROM python:3.14.7-slim AS builder
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /build

RUN <<EOF
	set -e
	apt-get update
	apt-get install -y --no-install-recommends ca-certificates wget build-essential
	rm -rf /var/lib/apt/lists/*
	wget -O mafft.deb https://mafft.cbrc.jp/alignment/software/mafft_7.526-1_amd64.deb
	wget -O cd-hit.tar.gz https://github.com/weizhongli/cdhit/releases/download/V4.8.1/cd-hit-v4.8.1-2019-0228.tar.gz
	tar -xvf cd-hit.tar.gz
	mv cd-hit-*/* .
	make zlib=no
EOF

FROM python:3.14.7-slim AS runtime

WORKDIR /build

COPY --from=builder /build/mafft.deb .
COPY --from=builder /build/cd-hit /usr/local/bin

RUN <<EOF
	set -e
	apt-get update
	apt-get install -y --no-install-recommends libgomp1
	dpkg -i /build/mafft.deb
	rm -rf /var/lib/apt/lists/*
EOF

COPY . .

RUN <<EOF
	set -e
	pip install --no-cache-dir .
	mv loom /usr/local/bin/
EOF

WORKDIR /data
