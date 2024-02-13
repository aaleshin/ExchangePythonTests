import pytest
import json
from hamcrest import *
from misc.common_methods import ws_request, generate_random_string


@pytest.mark.usefixtures("service_url")
class TestAddMethod:
    """
    Check Add Method
    """
    @pytest.mark.parametrize("id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response",
                             [
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'success'), # ** Баг №1
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(),'age', 100500, 'success'), # другой номер но данные теже
                                 ('id', '', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'success'),  # пустой id
                                 ('id', '123', 'method', 'add', 'name', '', 'surname', 'Dorris1', 'phone', generate_random_string(),'age', 100500, 'success'),  # пустое name
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', '', 'phone', generate_random_string(), 'age' , 100500, 'success'),  # пустая surname
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', '', 'phone', '', 'age', 100500, 'success'),  # пустая phone
                                 ('id', '', 'method', 'add', 'name', '', 'surname', '', 'phone', '', 'age', 100500, 'success'),  # 4 пустых значения
                                 ('id', ' 12 3 ', 'method', ' add ', 'name', ' Chu ck1 ', 'surname', ' Dorr is1 ', 'phone', ' fg f1h ', 'age', 100500, 'failure'),# пробелы в начале, в середине и в конце
                             ])
    @pytest.mark.asyncio
    async def test_check_add_positive_functionality(self, service_url, id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response):
        request_text = json.dumps({
            id_key: id,
            method_key: method,
            name_key: name,
            surname_key: surname,
            phone_key: phone,
            age_key: age
        })
        repl = await ws_request(service_url, request_text)
        assert_that(json.loads(repl)['id'], equal_to(id), 'ID')
        assert_that(json.loads(repl)['method'], equal_to(method), 'Method')
        assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')

        delete_text = json.dumps({'id': id, 'method': "delete", 'phone': phone})
        await ws_request(service_url, delete_text)

    @pytest.mark.parametrize(
        'id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response',
        [
          ('id', '1234', 'method', 'add', 'name', 'Chuck', 'surname', 'Dorris', 'phone', '1', 'age', 10050, 'failure'), # то же номер(проверка уникальности)
          ('id', None, 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # отсутствующий id
          ('id', '1234', 'method', None, 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500,'failure'),  # отсутствующий method
          ('id', '123', 'method', 'add', 'name', None, 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'), # отсутствующий name
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', None, 'phone', generate_random_string(), 'age', 100500, 'failure'), # отсутствующий surname
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', None, 'age', 100500, 'failure'),  # отсутствующий phone
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', None, 'failure'), # отсутствующий age
          ('test', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля id
          ('id', '123', 'test', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля method
          ('id', '123', 'method', 'add', 'test', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля name
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'test', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля surname
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'test', 100500, 'failure'),  # нет поля age
          ('id', '1235', 'method', 'add', 'name', 'Chuck1', 'test', 'Dorris1', 'test', generate_random_string(), 'age', 100500, 'failure'), # нет поля phone
          ('id', 1236, 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),# не верный тип данных для id
          ('id', '123', 'method', 123, 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(),'age', 100500, 'failure'),  # не верный тип данных для method
          ('id', '123', 'method', 'delete', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),# не верный метод
          ('id', '123', 'method', 'add', 'name', 111, 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'), # не верный тип данных для name
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 111, 'phone', generate_random_string(), 'age', 100500, 'failure'), # не верный тип данных для surname
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', 111, 'age', 100500, 'failure'),# не верный тип данных для phone
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 'test', 'failure'),# не верный тип данных для age
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 0, 'failure'),  # возаст 0
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', -1, 'failure'),  # возаст -1
          ('id', '@«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂', 'method', 'add', 'name', '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >',
           'surname', "<script>alert('XSS1')</script>", 'phone', "SELECT * FROM Users", 'age', 100500, 'failure'),  # нет обработки потенциально опасных символов
          ('id', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'method', 'add', 'name', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'surname', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'phone', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'age', 1, 'failure'),  # длинна строки - переполнение буфера ложит приложуху.
        ])
    @pytest.mark.asyncio
    async def test_check_add_negative_functionality(self, service_url, id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response):
        request_text = json.dumps({
            id_key: id,
            method_key: method,
            name_key: name,
            surname_key: surname,
            phone_key: phone,
            age_key: age
        })
        repl = await ws_request(service_url, request_text)
        if phone == '1':
            repl = await ws_request(service_url, request_text)

        if id is not str or method is not str:
            assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')
        else:
            assert_that(json.loads(repl)['id'], equal_to(id), 'ID')
            assert_that(json.loads(repl)['method'], equal_to(method), 'Method')
            assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')

        if phone == '1':
            delete_text = json.dumps({'id': id, 'method': "delete", 'phone': phone})
            await ws_request(service_url, delete_text)



