# waves installer for Windows
#
# From a clone or a download of the repo:
#   powershell -ExecutionPolicy Bypass -File install.ps1             install the waves command
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Startup    + show waves when PowerShell opens
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Uninstall  remove everything
#
# One-liner (downloads waves.py from GitHub):
#   irm https://raw.githubusercontent.com/tfem1/waves/main/install.ps1 | iex
#   $env:WAVES_STARTUP=1; irm https://raw.githubusercontent.com/tfem1/waves/main/install.ps1 | iex
#   $env:WAVES_UNINSTALL=1; irm https://raw.githubusercontent.com/tfem1/waves/main/install.ps1 | iex
param([switch]$Startup, [switch]$Uninstall)

function Install-Waves([bool]$Startup, [bool]$Uninstall, [string]$Here) {
    $ErrorActionPreference = "Stop"
    $Url = if ($env:WAVES_SRC) { $env:WAVES_SRC } else { "https://raw.githubusercontent.com/tfem1/waves/main/waves.py" }
    $Dest = Join-Path $env:LOCALAPPDATA "Programs\waves"
    $Mark = "# >>> waves >>>"
    $End = "# <<< waves <<<"
    $Docs = [Environment]::GetFolderPath("MyDocuments")
    $Profiles = @(
        (Join-Path $Docs "PowerShell\Microsoft.PowerShell_profile.ps1"),
        (Join-Path $Docs "WindowsPowerShell\Microsoft.PowerShell_profile.ps1")
    )

    function Remove-Block([string]$File) {
        if (-not (Test-Path $File)) { return }
        $text = Get-Content $File -Raw
        if (-not $text -or $text -notmatch [regex]::Escape($Mark)) { return }
        $pattern = "(?s)\r?\n?" + [regex]::Escape($Mark) + ".*?" + [regex]::Escape($End) + "\r?\n?"
        Set-Content -Path $File -Value ([regex]::Replace($text, $pattern, "`r`n").TrimEnd()) -Encoding UTF8
        Write-Host "  removed : $File"
    }

    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")

    if ($Uninstall) {
        if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
        $parts = "$userPath" -split ";" | Where-Object { $_ -and ($_ -ne $Dest) }
        [Environment]::SetEnvironmentVariable("Path", ($parts -join ";"), "User")
        foreach ($p in $Profiles) { Remove-Block $p }
        Write-Host "waves uninstalled (config kept in $env:APPDATA\waves)"
        return
    }

    # find a real Python 3 (the Microsoft Store alias does not count)
    $Python = $null
    foreach ($cand in @("py -3", "python", "python3")) {
        $parts = $cand -split " "
        $exe = $parts[0]
        if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
        $pyArgs = @($parts | Select-Object -Skip 1) + @("-c", "import sys; print(sys.version_info[0])")
        try { $v = & $exe @pyArgs 2>$null } catch { $v = $null }
        if ("$v".Trim() -eq "3") { $Python = $cand; break }
    }
    if (-not $Python) {
        Write-Host "Python 3 was not found. Install it, then run this again:" -ForegroundColor Yellow
        Write-Host "  winget install Python.Python.3.12"
        return
    }

    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    $target = Join-Path $Dest "waves.py"
    $local = if ($Here) { Join-Path $Here "waves.py" } else { $null }
    if ($local -and (Test-Path $local)) {
        Copy-Item $local $target -Force
    } else {
        Write-Host "downloading waves..."
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $Url -OutFile $target -UseBasicParsing
    }
    Set-Content -Path (Join-Path $Dest "waves.cmd") -Value "@$Python `"%~dp0waves.py`" %*" -Encoding ASCII
    Write-Host "waves installed to $Dest (using: $Python)"

    if (("$userPath" -split ";") -notcontains $Dest) {
        $new = if ($userPath) { "$userPath;$Dest" } else { $Dest }
        [Environment]::SetEnvironmentVariable("Path", $new, "User")
        Write-Host "  added to your PATH"
    }
    if (($env:Path -split ";") -notcontains $Dest) { $env:Path = "$env:Path;$Dest" }  # usable right away

    if ($Startup) {
        $block = "$Mark`r`nif (`$Host.Name -eq 'ConsoleHost' -and (Get-Command waves -ErrorAction SilentlyContinue)) { waves }`r`n$End"
        foreach ($p in $Profiles) {
            $dir = Split-Path $p
            if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
            Remove-Block $p
            Add-Content -Path $p -Value "`r`n$block" -Encoding UTF8
            Write-Host "  startup : $p"
        }
    }

    Write-Host "done! type: waves"
    Write-Host "tip: use Windows Terminal with a font that has braille glyphs (Cascadia Mono, JetBrains Mono)."
}

Install-Waves -Startup ($Startup -or [bool]$env:WAVES_STARTUP) `
              -Uninstall ($Uninstall -or [bool]$env:WAVES_UNINSTALL) `
              -Here $PSScriptRoot
Remove-Item Env:WAVES_STARTUP, Env:WAVES_UNINSTALL -ErrorAction SilentlyContinue
