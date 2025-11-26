# Script để push code lên GitHub với authentication

Write-Host "=== Push Code lên GitHub ===" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra remote
$remote = git remote get-url origin
Write-Host "Remote: $remote" -ForegroundColor Yellow
Write-Host ""

Write-Host "Có 2 cách để push:" -ForegroundColor Green
Write-Host ""
Write-Host "CÁCH 1: Dùng Personal Access Token (Khuyến nghị)" -ForegroundColor Cyan
Write-Host "1. Tạo token tại: https://github.com/settings/tokens"
Write-Host "2. Chọn scope: repo (full control)"
Write-Host "3. Copy token và chạy lệnh sau:"
Write-Host ""
Write-Host "   git remote set-url origin https://YOUR_TOKEN@github.com/Darkcom18/clickai_test.git" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""

Write-Host "CÁCH 2: Nhập token khi được hỏi" -ForegroundColor Cyan
Write-Host "Khi chạy 'git push', nhập:" -ForegroundColor Yellow
Write-Host "  Username: Darkcom18" -ForegroundColor Yellow
Write-Host "  Password: YOUR_TOKEN (không phải password GitHub!)" -ForegroundColor Yellow
Write-Host ""

$choice = Read-Host "Bạn muốn thử push ngay? (y/n)"
if ($choice -eq 'y') {
    Write-Host ""
    Write-Host "Đang push..." -ForegroundColor Green
    git push -u origin main
} else {
    Write-Host ""
    Write-Host "Xem file PUSH_INSTRUCTIONS.md để biết chi tiết" -ForegroundColor Cyan
}

