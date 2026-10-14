#!/bin/bash
cd ~/Pictures || exit 1

codes=(
  "Da__IucD5R3"
  "DapwUH9yGQf"
  "Dal0tx-E_Kx"
  "DF4J7WrMSjELg3SxuCqXCduk-ImTAngDG1gLn00"
  "DYUHMEytljO"
  "DYJKBzmnVj0"
)

for code in "${codes[@]}"; do
  instaloader --no-videos --no-captions --no-metadata-json -- -"$code"
done