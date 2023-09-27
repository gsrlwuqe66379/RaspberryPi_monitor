import json
import requests


def t_1():
    url = 'http://localhost:5392/data'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        json_data = json.loads(data)
        try:
            print(json_data['data'][0])
        except AttributeError:
            print('data属性')
    else:
        print('请求失败，状态码为', response.status_code)


def t_2():
    url = 'http://localhost:5393/get-data'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        record_str = json.dumps(data)
        record = json.loads(record_str)
        print(record['data'][0])
    else:
        print('请求失败，状态码为', response.status_code)


if __name__ == '__main__':
    t_2()