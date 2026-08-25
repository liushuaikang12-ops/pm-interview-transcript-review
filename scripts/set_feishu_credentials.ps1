[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^cli_[A-Za-z0-9]+$')]
    [string]$AppId
)

$ErrorActionPreference = 'Stop'
$secretValue = $null
$secretPointer = [IntPtr]::Zero

try {
    Write-Host "Configuring Feishu credentials for App ID: $AppId"
    Write-Host 'Paste the App Secret below. The input is hidden.'
    $secureSecret = Read-Host 'App Secret' -AsSecureString
    $secretPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureSecret)
    $secretValue = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($secretPointer)

    if ([string]::IsNullOrWhiteSpace($secretValue)) {
        throw 'App Secret cannot be empty.'
    }

    [Environment]::SetEnvironmentVariable('FEISHU_APP_ID', $AppId, 'User')
    [Environment]::SetEnvironmentVariable('FEISHU_APP_SECRET', $secretValue, 'User')

    Write-Host ''
    Write-Host 'Feishu credentials were saved to the current Windows user environment.' -ForegroundColor Green
    Write-Host 'The secret was not written to a config file or command history.'
}
finally {
    if ($secretPointer -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($secretPointer)
    }
    $secretValue = $null
    Remove-Variable secureSecret -ErrorAction SilentlyContinue
}

Write-Host ''
Read-Host 'Press Enter to close this window'
