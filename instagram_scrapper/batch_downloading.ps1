Set-Location "$HOME\Pictures\Saved Pictures"

$codes = @(
    "DY8xgiYEeMo"
    "DZAXMTwkzW2"
)

foreach ($code in $codes) {
    instaloader --no-videos --no-captions --no-metadata-json -- -$code
}