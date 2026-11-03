# waves installer for Windows
#   powershell -ExecutionPolicy Bypass -File install.ps1             install the waves command
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Startup    + show waves when PowerShell opens
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Uninstall  remove everything
param([switch]$Startup, [switch]$Uninstall)
$ErrorActionPreference = "Stop"

$Dest = Join-Path $env:LOCALAPPDATA "Programs\waves"
$Mark = "# >>> waves >>>"
$End = "# <<< waves <<<"
$Profiles = @(
    (Join-Path ([Environment]::GetFolderPath("MyDocuments")) "PowerShell\Microsoft.PowerShell_profile.ps1"),
    (Join-Path ([Environment]::GetFolderPath("MyDocuments")) "WindowsPowerShell\Microsoft.PowerShell_profile.ps1")
)

function Remove-Block([string]$File) {
    if (-not (Test-Path $File)) { return }
    $text = Get-Content $File -Raw
    if ($text -notmatch [regex]::Escape($Mark)) { return }
    $pattern = "(?s)\r?\n?" + [regex]::Escape($Mark) + ".*?" + [regex]::Escape($End) + "\r?\n?"
    Set-Content -Path $File -Value ([regex]::Replace($text, $pattern, "`r`n").TrimEnd()) -Encoding UTF8
    Write-Host "  removed : $File"
}

function Get-UserPath { [Environment]::GetEnvironmentVariable("Path", "User") }

if ($Uninstall) {
    if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
    $parts = (Get-UserPath) -split ";" | Where-Object { $_ -and ($_ -ne $Dest) }
    [Environment]::SetEnvironmentVariable("Path", ($parts -join ";"), "User")
    foreach ($p in $Profiles) { Remove-Block $p }
    Write-Host "waves uninstalled (config kept in $env:APPDATA\waves)"
    exit 0
}

# find a real Python 3 (the Microsoft Store alias does not count)
$Python = $null
foreach ($cand in @("py -3", "python", "python3")) {
    $parts = $cand -split " "
    $exe = $parts[0]
    if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
    $args_ = @($parts | Select-Object -Skip 1) + @("-c", "import sys; print(sys.version_info[0])")
    try { $v = & $exe @args_ 2>$null } catch { $v = $null }
    if ("$v".Trim() -eq "3") { $Python = $cand; break }
}
if (-not $Python) {
    Write-Host "Python 3 was not found. Install it, then run this script again:" -ForegroundColor Yellow
    Write-Host "  winget install Python.Python.3.12"
    exit 1
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Copy-Item (Join-Path $PSScriptRoot "waves.py") (Join-Path $Dest "waves.py") -Force
Set-Content -Path (Join-Path $Dest "waves.cmd") -Value "@$Python `"%~dp0waves.py`" %*" -Encoding ASCII
Write-Host "waves installed to $Dest (using: $Python)"

if (((Get-UserPath) -split ";") -notcontains $Dest) {
    $current = Get-UserPath
    $new = if ($current) { "$current;$Dest" } else { $Dest }
    [Environment]::SetEnvironmentVariable("Path", $new, "User")
    Write-Host "  added to your PATH (open a new terminal)"
}

if ($Startup) {
    $block = @"
$Mark
if (`$Host.Name -eq 'ConsoleHost' -and (Get-Command waves -ErrorAction SilentlyContinue)) { waves }
$End
"@
    foreach ($p in $Profiles) {
        $dir = Split-Path $p
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
        Remove-Block $p
        Add-Content -Path $p -Value "`r`n$block" -Encoding UTF8
        Write-Host "  startup : $p"
    }
}

Write-Host "open a new terminal and type: waves"
Write-Host "tip: use Windows Terminal with a font that has braille glyphs (Cascadia Mono, JetBrains Mono)."
