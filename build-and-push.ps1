# Docker Hub repository
$DOCKER_REPO = "drefault/radio_player"
$VERSION = "latest"

Write-Host "Building Docker image..." -ForegroundColor Cyan
docker build -t ${DOCKER_REPO}:${VERSION} .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Build successful!" -ForegroundColor Green
    
    Write-Host "`nLogging in to Docker Hub..." -ForegroundColor Cyan
    docker login
    
    Write-Host "`nPushing image to Docker Hub..." -ForegroundColor Cyan
    docker push ${DOCKER_REPO}:${VERSION}
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Successfully pushed to Docker Hub!" -ForegroundColor Green
        Write-Host "Image available at: https://hub.docker.com/r/${DOCKER_REPO}" -ForegroundColor Yellow
    } else {
        Write-Host "✗ Failed to push image" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ Build failed" -ForegroundColor Red
    exit 1
}
