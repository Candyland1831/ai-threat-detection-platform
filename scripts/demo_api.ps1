param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

Write-Host "Checking platform health..."
Invoke-RestMethod -Uri "$BaseUrl/health"

Write-Host "`nReading model metadata..."
Invoke-RestMethod -Uri "$BaseUrl/model-info"

Write-Host "`nLogging in..."
$login = Invoke-RestMethod `
    -Uri "$BaseUrl/login" `
    -Method Post `
    -ContentType "application/x-www-form-urlencoded" `
    -Body "username=admin&password=password123"

Write-Host "`nRunning prediction..."
$payload = Get-Content "sample_prediction_request.json" -Raw
$prediction = Invoke-RestMethod `
    -Uri "$BaseUrl/predict" `
    -Method Post `
    -ContentType "application/json" `
    -Headers @{ Authorization = "Bearer $($login.access_token)" } `
    -Body $payload

$prediction | ConvertTo-Json -Depth 10

Write-Host "`nListing generated alerts..."
Invoke-RestMethod `
    -Uri "$BaseUrl/alerts" `
    -Headers @{ Authorization = "Bearer $($login.access_token)" }
