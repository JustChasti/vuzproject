
"""     Настройки:
            headers - заголовки
            url - сервер flask
            base name pass user - настройки подключения к postgres
            delay - задержка парсинга (для теста - 60 секунд, для работы 3600)
        Инструкция:
            1) запустить app (flask)
            2) запустить parser
            3) можно запустить тесты
"""


headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
delay = 3600
url = 'https://chastyescape.site/'
base_user = "postgres"
base_pass = "qm7hFSIW"
base_name = "finaltest2"

