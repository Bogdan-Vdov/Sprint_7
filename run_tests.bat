@echo off
echo Запуск тестов...
pytest tests/ -v --alluredir=allure-results
echo.
echo Тесты завершены!
echo Для просмотра отчета выполните: allure serve allure-results
pause
