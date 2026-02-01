$codes = @(
    "Ddfjals"
    "aBcDeFg"
    "XyZ1234"
)

foreach ($code in $codes) {
    instaloader -- -$code
}