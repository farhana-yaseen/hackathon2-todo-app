param(
    [switch]$Json
)

# Get the current git branch
$branch = $(git branch --show-current)

# Find the spec file for the current feature
$specDir = "specs/$branch"
$featureSpec = "$specDir/spec.md"

# Set the implementation plan file path
$implPlan = ".spec-kit/plan_$branch.md"

# If Json switch is used, output JSON format
if ($Json) {
    $output = @{
        FEATURE_SPEC = $featureSpec
        IMPL_PLAN = $implPlan
        SPECS_DIR = $specDir
        BRANCH = $branch
    } | ConvertTo-Json

    Write-Output $output
} else {
    Write-Host "Feature Spec: $featureSpec"
    Write-Host "Impl Plan: $implPlan"
    Write-Host "Specs Dir: $specDir"
    Write-Host "Branch: $branch"
}