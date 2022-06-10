@echo OFF
set CONDAPATH=C:\Users\user\Anaconda3
set ENVNAME=motion
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python d:\program\first-order-model\demodir.py --config d:\program\first-order-model\config\vox-256.yaml --checkpoint d:\program\first-order-model\vox-cpk.pth.tar --source_image D:/program/ui/pics/kid6withback.png --driving_dir D:/program/ui/focus03 --relative --output_dir D:/program/ui/output\ --find_best_frame --start 150 --end 170
call conda deactivate
timeout /t 5
