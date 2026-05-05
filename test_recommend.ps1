$queries = @("gold price volatility", "system outage risk", "cybersecurity threats in trading")

foreach ($q in $queries) {
    Write-Host "Testing query: $q"
    $result = Invoke-RestMethod -Uri "http://127.0.0.1:5000/recommend/" `
        -Method POST `
        -Body (@{query=$q} | ConvertTo-Json) `
        -ContentType "application/json"
    $result | ConvertTo-Json -Depth 5
    Write-Host "`n"
}
