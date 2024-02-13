import pytest
import json
from hamcrest import *
from misc.common_methods import ws_request, generate_random_string

@pytest.mark.usefixtures("service_url")
class TestUpdateMethod:
    """
    Check Add Method
    """

    @pytest.mark.parametrize("id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response",
                             [
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '1', 'age', 100500, 'success'),
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '2','age', 100500, 'success'), # другой номер но данные теже
                                 ('id', '', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '3', 'age', 100500, 'success'),  # пустой id
                                 ('id', '123', 'method', '', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '4','age', 100500, 'success'),  # пустой метод
                                 ('id', '123', 'method', 'add', 'name', '', 'surname', 'Dorris1', 'phone', '5','age', 100500, 'success'),  # пустое имя
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', '', 'phone', '6', 'age' , 100500, 'success'),  # пустая фамилия
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '7', 'age', '', 'success'),  # пустой возраст
                                 ('test', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '8', 'age', 100500, 'success'),  # нет поля id
                                 ('id', '123', 'test', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone','9', 'age', 100500, 'success'),  # нет поля method
                                 ('id', '123', 'method', 'add', 'test', 'Chuck1', 'surname', 'Dorris1', 'phone', '10','age', 100500, 'success'),  # нет поля name
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'test', 'Dorris1', 'phone', '11','age', 100500, 'success'),  # нет поля surname
                                 ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '12','test', 100500, 'success'),  # нет поля age

                             ])
    @pytest.mark.asyncio
    async def test_add_positive_functionality(self, service_url, id_key, id, method_key, method, name_key, name,surname_key, surname, phone_key, phone, age_key, age, status_in_response):
        request_text = json.dumps({
            'id': id,
            'method': method,
            'name': name,
            'surname': surname,
            'phone': phone,
            'age': age
        })
        repl = await ws_request(service_url, request_text)
        assert_that(json.loads(repl)['id'], equal_to(id), 'ID')
        assert_that(json.loads(repl)['method'], equal_to(method), 'Method')
        assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')

    @pytest.mark.parametrize(
        'id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response',
        [
            ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '2222', 'age', 100500, 'failure'),  # то же номер(проверка уникальности)
            ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', '', 'age', 100500, 'failure'),  # пустой телефон
            ('id', '123', 'method', 'add', 'name', 'Chuck1', 'test', 'Dorris1', 'test', '11', 'age', 100500, 'failure'),  # нет поля phone

        ])
    @pytest.mark.asyncio
    async def test_add_negative_functionality(self, service_url, id_key, id, method_key, method, name_key, name,
                                              surname_key, surname, phone_key, phone, age_key, age, status_in_response):
        request_text = json.dumps({
            'id': id,
            'method': method,
            'name': name,
            'surname': surname,
            'phone': phone,
            'age': age
        })
        repl = await ws_request(service_url, request_text)
        assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')
