#!/bin/bash
codes=(
  "Ddfjals"
  "aBcDeFg"
  "XyZ1234"
)

for code in "${codes[@]}"; do
  instaloader -- -"$code"
done