@echo off
rem Set Python Interpreter for script usage
set python_interpreter = C:\Python\Python_3.11.1\python.exe

rem Extract Python Interpreter Version
for /f "tokens=2 delims= " %%a in ('C:\Python\Python_3.11.1\python.exe --version') do set "py_version=%%a"

echo Server is on using Python %py_version%...
echo.

rem Execute server.py which is server combined with Cloud App
C:\Python\Python_3.11.1\python.exe %USERPROFILE%\Desktop\my_cloud\app\server.py
pause