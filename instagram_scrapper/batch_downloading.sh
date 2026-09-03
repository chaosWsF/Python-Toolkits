#!/bin/bash
cd ~/Pictures || exit 1

codes=(
  "DcneDecEu9s"
  "Dcle75vIxgF"
  "Dcx8JADCVAR"
  "DcnpTEjEWt1"
  "DcnDbvCDzFL"
)

for code in "${codes[@]}"; do
  instaloader --no-videos --no-captions --no-metadata-json -- -"$code"
done