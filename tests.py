import requests
import json
import time
import config


def send(text):
    data = {
        "link": text,
        }
    answer = requests.post(config.url+'links/add/', data=json.dumps(data), headers=config.headers)
    print(answer)


if __name__ == "__main__":
    send("https://www.ozon.ru/product/izuchaem-python-programmirovanie-igr-vizualizatsiya-dannyh-veb-prilozheniya-metiz-erik-metiz-erik-211432437/?asb=%252Bx87qAkdRA3D4q%252BKBMQxZ%252FyCQEsNOj8pJVOkYQ9atws%253D&asb2=wV5BTt5JOS7sFrT2ZHsiBCGm0wlrRZ42z3elfT6OGOQ&keywords=python")
    send("https://www.wildberries.ru/catalog/16023993/detail.aspx?targetUrl=XS")
    time.sleep(90)
    send("https://www.ozon.ru/product/15-6-noutbuk-lenovo-ideapad-l340-15api-amd-ryzen-3-3200u-2-6-ggts-ram-8-gb-256-gb-amd-radeon-vega-266944297/")
    send("https://www.wildberries.ru/catalog/16865233/detail.aspx")
