#!/bin/bash
set -e

# 1. node_exporter 다운로드 및 배치
export VERSION="1.7.0"
wget https://github.com/prometheus/node_exporter/releases/download/v${VERSION}/node_exporter-${VERSION}.linux-amd64.tar.gz
tar xvfz node_exporter-${VERSION}.linux-amd64.tar.gz
sudo mv node_exporter-${VERSION}.linux-amd64/node_exporter /usr/local/bin/

# 2. systemd 서비스 파일 생성 (인스턴스 시작 시 자동 실행 설정)
sudo tee /etc/systemd/system/node_exporter.service <<EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=root
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# 3. 서비스 활성화
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
