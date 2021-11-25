#
# cronWebJob.ps1
#

$cronFile = "$($env:HOME)\site\wwwroot\redcap\cron.php"

$phpExe = "${env:ProgramFiles(x86)}\PHP\v7.4\php.exe"
Start-Process -NoNewWindow -FilePath $phpExe -ArgumentList @($cronFile)