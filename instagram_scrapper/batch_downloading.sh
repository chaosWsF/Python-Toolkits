#!/bin/bash
cd ~/Projects

codes=(
  "Ddfjals"
  "aBcDeFg"
  "XyZ1234"
)

for code in "${codes[@]}"; do
  instaloader -- -"$code"
done