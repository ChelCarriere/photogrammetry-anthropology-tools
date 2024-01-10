@echo off
@setlocal
@setlocal ENABLEEXTENSIONS
@setlocal ENABLEDELAYEDEXPANSION

set MESHROOM="D:\Program Files\Meshroom-2021.1.0-win64\Meshroom-2021.1.0\meshroom_batch.exe"
set THISDIR=%CD%

echo THISDIR = %THISDIR%

set SAMPLESFILE=samples-to-run.txt

if not exist %SAMPLESFILE% goto NOFILE

for /f %%s in (%SAMPLESFILE%) do (
  echo !!!=== %%s - Processing begins ===
  set IMAGESDIR=%THISDIR%\%%s
  cd "!IMAGESDIR!"
  if not exist model\MeshroomCache mkdir model\MeshroomCache
  cd model
  cd
  echo %MESHROOM% -p photogrammetry -i "!IMAGESDIR!" --save "%%s.mg" --cache "!IMAGESDIR!\model\MeshroomCache"
  %MESHROOM% -p photogrammetry -i "!IMAGESDIR!" --save "%%s.mg" --cache "!IMAGESDIR!\model\MeshroomCache"
)

goto :EOF

:NOFILE
echo.
echo ERROR can't find file samples-to-run.txt
echo.
echo aborting!
