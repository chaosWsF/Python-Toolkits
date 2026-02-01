Set-Location ~
Set-Location '.\Pictures\Saved Pictures'

$codes = @(
    "DUOCKDAkrvj"
    "DUNxe_vgVkI"
)

foreach ($code in $codes) {
    instaloader -- -$code
}