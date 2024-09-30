REM Активация виртуального окружения
call venv\Scripts\activate

REM Установка зависимостей (или проверка их наличия)
echo Установка зависимостей...
pip install -r requirements.txt

REM Запуск приложения Flask
echo Запуск Flask-приложения...
python app.py

REM Отображение ссылки для входа
echo Приложение запущено. Откройте браузер и введите адрес: http://127.0.0.1:5000
pause