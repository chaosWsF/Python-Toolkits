Set-Location ~
Set-Location '.\Pictures\Saved Pictures'

$codes = @(
    "DXzNMZhk3Wl"
    "DX1cbH1GMSR"
)

foreach ($code in $codes) {
    instaloader --no-videos --no-captions --no-metadata-json -- -$code
}