

@echo off
rem
rem Bitte Pfad zu Blender.exe eintragen!
rem
SET BLENDER="C:\Program Files\Blender Foundation\Blender\blender.exe"
SET PYSCRIPT=%~dp0convert_split.py
SET EXTSCRIPT=%~dp0extract.py

SET ARGS=

if not exist %BLENDER% GOTO :NOBLENDER


for %%i in (inputFiles\*.fbx*) do call :Foo %%i
for %%i in (outputFiles\*.obj*) do call :Del %%i
for %%i in (outputFiles\*.mtl*) do call :Del %%i

GOTO: End

:FOO
	SET name=%1
	SET outputPath=outputFiles\%name:~11,-3%obj rem 11 stands for the length of the path before the file name
	SET finalPath=outputFiles\final_%name:~11,-3%fbx
	compression.exe %1 %outputPath% 
	call %BLENDER% -b -P %PYSCRIPT% -- --Inobj %outputPath% --Outfbx %finalPath% --Infbx %1 %ARGS%
	
GOTO :End


:DEL
	SET file=%1
	del "%file%"
GOTO :End

:NOBLENDER
ECHO.
ECHO "Blender.exe nicht gefunden!"
ECHO.
GOTO :END


:End