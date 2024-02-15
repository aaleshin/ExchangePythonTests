import pytest
import json
from hamcrest import *
from misc.common_methods import ws_request, generate_random_string


@pytest.mark.usefixtures("service_url")
class TestAddMethod:
    """
    Check Add Method
    """
    @pytest.mark.parametrize("id, name, surname, phone, age, status_in_response",
                             [
                                 ('123', 'CHUCK1',  'dorris1', generate_random_string(), 100500, 'success'),  #добавление в разном регистре  ** Баг №1
                                 ('123', 'Chuck1', 'Dorris1', generate_random_string(), 100500, 'success'),  # другой номер но данные теже
                                 ('', 'chuck', 'DORRIS', generate_random_string(), 100500, 'success'),  # пустой id
                                 ('123', '', 'Dorris1', generate_random_string(), 100500, 'success'),  # пустое name
                                 ('123', 'Chuck1', '', generate_random_string(), 100500, 'success'),  # пустая surname
                                 ('123', 'Chuck1', 'Dorris1', '', 100500, 'success'),  # пустая phone
                                 ('', '', '', '', 100500, 'success'),  # 4 пустых значения
                                 (' 12 3 ', ' Chu ck1 ', ' Dorr is1 ', ' 12345 4545 ', 100500, 'success'),  # пробелы в начале, в середине и в конце
                                 (' 12 3 ', 'Тестер', 'ТЕстерВИЧ', ' 12345 4545 ', 100500, 'success'),  # имя и фамилия на кирилицу
                             ])
    @pytest.mark.asyncio
    async def test_check_add_positive_functionality(self, service_url, id, name, surname, phone, age, status_in_response):
        request_text = json.dumps({
            'id': id,
            'method': 'add',
            'name': name,
            'surname': surname,
            'phone': phone,
            'age': age
        })
        repl = await ws_request(service_url, request_text)
        assert_that(json.loads(repl)['id'], equal_to(id), 'ID')
        assert_that(json.loads(repl)['method'], equal_to('add'), 'Method')
        assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')

        delete_text = json.dumps({'id': id, 'method': "delete", 'phone': phone})
        await ws_request(service_url, delete_text)

    @pytest.mark.parametrize(
        'id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response',
        [
          ('id', '1234', 'method', 'add', 'name', 'Chuck', 'surname', 'Dorris', 'phone', '1', 'age', 10050, 'failure'),  # то же номер(проверка уникальности)
          ('id', None, 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # отсутствующий id
          ('id', '1234', 'method', None, 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500,'failure'),  # отсутствующий method
          ('id', '123', 'method', 'add', 'name', None, 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # отсутствующий name
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', None, 'phone', generate_random_string(), 'age', 100500, 'failure'),  # отсутствующий surname
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', None, 'age', 100500, 'failure'),  # отсутствующий phone
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', None, 'failure'),  # отсутствующий age
          ('test', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля id
          ('id', '123', 'test', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля method
          ('id', '123', 'method', 'add', 'test', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля name
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'test', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # нет поля surname
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'test', 100500, 'failure'),  # нет поля age
          ('id', '1235', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'test', generate_random_string(), 'age', 100500, 'failure'),  # нет поля phone
          ('id', 1236, 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # не верный тип данных для id
          ('id', '123', 'method', 123, 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(),'age', 100500, 'failure'),  # не верный тип данных для method
          ('id', '123', 'method', 'delete', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # не верный метод
          ('id', '123', 'method', 'add', 'name', 111, 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 100500, 'failure'),  # не верный тип данных для name
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 111, 'phone', generate_random_string(), 'age', 100500, 'failure'),  # не верный тип данных для surname
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', 111, 'age', 100500, 'failure'),  # не верный тип данных для phone
          ('id', '123', 'method', 'add', 'name', 'Chuck1', 'surname', 'Dorris1', 'phone', generate_random_string(), 'age', 'test', 'failure'),  # не верный тип данных для age
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

        assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')

        if id_key == 'id' and id is isinstance(id, str):
            assert_that(json.loads(repl)['id'], equal_to(id), 'ID')

        if age and not isinstance(age, int):
            assert_that(json.loads(repl)['reason'], contains_string('[json.exception.type_error.302] type must be number, but '), 'Reason')

        for key, value in zip((id_key, method_key, name_key, surname_key, phone_key, age_key), ('id', 'method', "name", "surname", 'phone', "age")):
            if key != value:
                assert_that(json.loads(repl)['reason'], contains_string('[json.exception.out_of_range.403] key '), 'Reason')
                break

        variables = {'id': id, 'method': method, 'name': name, 'surname': surname, 'phone': phone}
        keys = {'id': id_key, 'method': method_key, 'name': name_key, 'surname': surname_key, 'phone': phone_key}
        for variable_name, variable in variables.items():
            key = keys[variable_name]
            if key and not isinstance(variable, str):
                assert_that(json.loads(repl)['reason'], contains_string(f'[json.exception.type_error.302] type must be string'), 'Reason')

        if phone == '1' or age == 0 or age == -1:
            delete_text = json.dumps({'id': id, 'method': "delete", 'phone': phone})
            await ws_request(service_url, delete_text)



