param(
    [Parameter(Mandatory=$true)]
    [string]$Description,

    [Parameter(Mandatory=$true)]
    [int]$Number,

    [Parameter(Mandatory=$true)]
    [string]$ShortName,

    [switch]$Json
)

# Create branch name
$branchName = "${Number}-${ShortName}"

# Create spec directory if it doesn't exist
$specDir = "specs/${Number}-${ShortName}"
if (!(Test-Path $specDir)) {
    New-Item -ItemType Directory -Path $specDir -Force | Out-Null
}

# Create the spec file
$specFile = "${specDir}/spec.md"

# If Json switch is used, output JSON format
if ($Json) {
    $output = @{
        BRANCH_NAME = $branchName
        SPEC_FILE = $specFile
        FEATURE_NUMBER = $Number
        SHORT_NAME = $ShortName
        DESCRIPTION = $Description
    } | ConvertTo-Json

    Write-Output $output
} else {
    Write-Host "Created branch: $branchName"
    Write-Host "Created spec file: $specFile"
    Write-Host "Feature: $Description"
}

# Checkout the new branch (create if doesn't exist)
git checkout -b $branchName 2>$null || git checkout $branchName