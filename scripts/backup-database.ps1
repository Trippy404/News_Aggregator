# backup-database.ps1
Write-Host "Creating database backup..." -ForegroundColor Cyan
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = ".\backups"

New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

docker exec news_mysql mysqldump -u news_user -pSecureNewsPass456! news_aggregator > "$backupDir\backup_$timestamp.sql"

Write-Host " Backup created: $backupDir\backup_$timestamp.sql" -ForegroundColor Green