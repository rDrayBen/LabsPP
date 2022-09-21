Lab4
1. Для початку необхідно встановити virtualenv + requirements.txt, а також pyenv у пусту папку. Для цього необхідно відкрити WinowsPowerShell та за допомогою команди cd:\ваша\директорія перейти у задану директорію.
2. Для того, щоб встановити pyenv, необхідно вписати дану команду Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1" після чого, якщо у вас не з'явилися помилки, встановлення відбулося успішно. Якщо ж помилка все ж таки з'явилася, необхідно перезапустити консоль від імені адміністратора і спробувати знову.
3. Далі, за допомогою команди pip install virtualenv, ви встановите віртуальне середовище.
4. Для встановлення requirements.txt необхідно прописати в консолі наступну команду pip freeze #view requirements to be created (best done in virtual env)
                                                                                 >> pip freeze > requirements.txt #create requirements.txt (best done in virtual env)
                                                                                 >> pip install -r requirements.txt
5. Далі, за допомогою команди -p -3 -m virtualenv <назва проекту> створимо вірутальне середовище для проекту. Коли воно встворене, необхідно перейти в диверторію проекту.
6. Активуємо віртуальне середовище за допомогою команди <назва проекту>\Scripts\activate.
7. Далі необхідно встановити Flask, що виконується за допомогою команди pip install Flask.
8. Після цього, необхідно завантажити додаток для запуску WSGI сервера. Робиться це в тій же директорії за допогою команди pip install waitress.
9. Для запуску сервера необхідно прописати в тій же директорії в консолі команду waitress-serve --host 127.0.0.1 --port 10000 server:app
10. Це запустить нам сервер за допомогою фреймворка Flask, де роль сервера буде відвгравати файл server.py, а сам сайт буде виконуватись у файлі hello.py.
11. Перевірити роботу сайту можна за допомогою утиліти Git Bash вставивши і її консоль це посилання curl -v -XGET http://localhost:10000/api/v1/hello-world-6
