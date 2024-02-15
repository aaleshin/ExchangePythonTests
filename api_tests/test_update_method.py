import pytest
import json
from hamcrest import *
from misc.common_methods import ws_request, generate_random_string


@pytest.mark.usefixtures("service_url")
class TestUpdateMethod:
    """
    Check Update Method
    """
    @pytest.mark.parametrize("id, name, surname, phone, age, status_in_response",
        [
            ('123', 'CHUCK1',  'dorris1', '987654321', 45609, 'success'),  #изменения в разном регистре
            ('12317987', 'Test1', 'Dorris13', '987654321', 45609, 'success'),  # редактирования id
            ('1237659', 'BlUCK25', 'Dorris13', '987654321', 45609, 'success'),  # редактирования name
            ('1237659', 'Test1', 'boris', '987654321', 45609, 'success'),  # редактирования surname
            ('1237659', 'Test1', 'Dorris13', '987654321', 99999, 'success'),  # редактирования age
            ('1237659', 'Test1', 'Dorris13', generate_random_string(), 45609, 'failure'),  # другой номер но данные теже
            ('', 'chuck', 'DORRIS', '987654321', 45609, 'success'),  # пустой id
            ('123', '', 'Dorris1', '987654321', 45609, 'success'),  # пустое name
            ('123', 'Chuck1', '', '987654321', 45609, 'success'),  # пустая surname
            ('123', 'Chuck1', 'Dorris1', '', 45609, 'failure'),  # пустая phone
            ('', '', '', '987654321', 45609, 'success'),  # 3 пустых значения
            (' 12 3 ', ' Chu Тестер ', ' ТЕстерВИЧ is1 ', '987654321', 45609, 'success'),  # пробелы в начале, в середине и в конце
        ])
    @pytest.mark.asyncio
    async def test_check_update_positive_functionality(self, service_url, id, name, surname, phone, age, status_in_response):
        request_text = json.dumps({
            'id': '1237659',
            'method': 'add',
            'name': 'Test1',
            'surname': 'Dorris13',
            'phone': '987654321',
            'age': 45609
        })
        await ws_request(service_url, request_text)

        request_updated_text = json.dumps({
            'id': id,
            'method': 'update',
            'name': name,
            'surname': surname,
            'phone': '987654321',
            'age': age
        })
        repl = await ws_request(service_url, request_updated_text)
        assert_that(json.loads(repl)['id'], equal_to(id), 'ID')
        assert_that(json.loads(repl)['method'], equal_to('update'), 'Method')
        assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')

        if status_in_response == 'success':
            select_text = json.dumps({'id': id, 'method': "select", 'phone': phone})
            selected_user = await ws_request(service_url, select_text)
            assert_that(json.loads(selected_user)['id'], equal_to(id), 'ID')
            assert_that(json.loads(selected_user)['method'], equal_to('select'), 'Method')
            assert_that(json.loads(selected_user)['status'], equal_to('failure'), 'Status')
            assert_that(json.loads(selected_user)['users'][0]['name'], equal_to(name), 'Name')
            assert_that(json.loads(selected_user)['users'][0]['surname'], equal_to(surname), 'Surname')
            assert_that(json.loads(selected_user)['users'][0]['age'], equal_to(age), 'Age')

            delete_text = json.dumps({'id': id, 'method': "delete", 'phone': phone})
            await ws_request(service_url, delete_text)

    @pytest.mark.asyncio
    async def test_check_update_after_update(self, service_url):
        request_text = json.dumps({
            'id': '1237659',
            'method': 'add',
            'name': 'Test',
            'surname': 'Dorris1',
            'phone': '987654321',
            'age': 45609
        })
        await ws_request(service_url, request_text)

        request_updated_text = json.dumps({
            'id': 'double',
            'method': 'update',
            'name': 'Test1',
            'surname': 'Dorris2',
            'phone': '987654321',
            'age': 45609
        })
        repl = await ws_request(service_url, request_updated_text)
        assert_that(json.loads(repl)['status'], equal_to("success"), 'Status')

        request_second_updated_text = json.dumps({
            'id': 'double2',
            'method': 'update',
            'name': 'Test2',
            'surname': 'Dorris3',
            'phone': '987654321',
            'age': 45609
        })

        repl_new = await ws_request(service_url, request_second_updated_text)
        assert_that(json.loads(repl_new)['status'], equal_to("success"), 'Status')

        select_text = json.dumps({'id': 'double2', 'method': 'select', 'phone': '987654321'})
        selected_user = await ws_request(service_url, select_text)
        assert_that(json.loads(selected_user)['id'], equal_to("double2"), 'ID')
        assert_that(json.loads(selected_user)['method'], equal_to('select'), 'Method')
        assert_that(json.loads(selected_user)['status'], equal_to('failure'), 'Status')
        assert_that(json.loads(selected_user)['users'][0]['name'], equal_to("Test2"), 'Name')
        assert_that(json.loads(selected_user)['users'][0]['surname'], equal_to("Dorris3"), 'Surname')

        delete_text = json.dumps({'id': 'double2', 'method': "delete", 'phone': '987654321'})
        await ws_request(service_url, delete_text)

    @pytest.mark.asyncio
    async def test_check_update_deleted(self, service_url):
        request_text = json.dumps({
            'id': '1237659',
            'method': 'add',
            'name': 'Test',
            'surname': 'Dorris1',
            'phone': '987654321',
            'age': 45609
        })
        await ws_request(service_url, request_text)

        request_updated_text = json.dumps({
            'id': 'double',
            'method': 'update',
            'name': 'Test1',
            'surname': 'Dorris2',
            'phone': '987654321',
            'age': 45609
        })
        repl = await ws_request(service_url, request_updated_text)
        assert_that(json.loads(repl)['status'], equal_to("success"), 'Status')

        delete_text = json.dumps({'id': 'double', 'method': "delete", 'phone': '987654321'})
        await ws_request(service_url, delete_text)

        request_second_updated_text = json.dumps({
            'id': 'double2',
            'method': 'update',
            'name': 'Test2',
            'surname': 'Dorris3',
            'phone': '987654321',
            'age': 45609
        })
        repl_new = await ws_request(service_url, request_second_updated_text)
        assert_that(json.loads(repl_new)['status'], equal_to("failure"), 'Status')

    @pytest.mark.parametrize(
        'id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response',
        [
          ('id', None, 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # отсутствующий id
          ('id', '123', 'method', 'update', 'name', None, 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # отсутствующий name
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', None, 'phone', '09876543', 'age', 9876540, 'failure'),  # отсутствующий surname
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', None, 'age', 9876540, 'failure'),  # отсутствующий phone
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', None, 'failure'),  # отсутствующий age
          ('test', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # нет поля id
          ('id', '123', 'test', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # нет поля method
          ('id', '123', 'method', 'update', 'test', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # нет поля name
          ('id', '123', 'method', 'update', 'name', 'Tester', 'test', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # нет поля surname
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'test', 9876540, 'failure'),  # нет поля age
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'test', '09876543', 'age', 9876540, 'failure'),  # нет поля phone
          ('id', 1236, 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # не верный тип данных для id
          ('id', '123', 'method', 123, 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543','age', 9876540, 'failure'),  # не верный тип данных для method
          ('id', '123', 'method', 'test', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # не верный метод
          ('id', '123', 'method', 'update', 'name', 111, 'surname', 'Testr2', 'phone', '09876543', 'age', 9876540, 'failure'),  # не верный тип данных для name
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 111, 'phone', '09876543', 'age', 9876540, 'failure'),  # не верный тип данных для surname
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', 111, 'age', 9876540, 'failure'),  # не верный тип данных для phone
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 'test', 'failure'),  # не верный тип данных для age
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', 0, 'failure'),  # возаст 0
          ('id', '123', 'method', 'update', 'name', 'Tester', 'surname', 'Testr2', 'phone', '09876543', 'age', -1, 'failure'),  # возаст -1
          ('id', '@«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂', 'method', 'update', 'name', '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >',
           'surname', "<script>alert('XSS1')</script>", 'phone', "SELECT * FROM Users", 'age', 9876540, 'failure'),  # нет обработки потенциально опасных символов
          ('id', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'method', 'update', 'name', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'surname', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'phone', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
           'age', 1, 'failure'),  # длинна строки - переполнение буфера ложит приложуху.
        ])
    @pytest.mark.asyncio
    async def test_check_update_negative_functionality(self, service_url, id_key, id, method_key, method, name_key, name, surname_key, surname, phone_key, phone, age_key, age, status_in_response):
        request_text = json.dumps({
            id_key: id,
            method_key: method,
            name_key: name,
            surname_key: surname,
            phone_key: phone,
            age_key: age
        })
        repl = await ws_request(service_url, request_text)
        assert_that(json.loads(repl)['status'], equal_to(status_in_response), 'Status')

        if id_key == 'id' and id is isinstance(id, str):
            assert_that(json.loads(repl)['id'], equal_to(id), 'ID')

        if age and not isinstance(age, int):
            assert_that(json.loads(repl)['reason'], contains_string('[json.exception.type_error.302] type must be number, but '), 'Reason')

        for key, value in zip((id_key, method_key, name_key, surname_key, phone_key, age_key),
                              ('id', 'method', "name", "surname", 'phone', "age")):
            if key != value:
                assert_that(json.loads(repl)['reason'], contains_string('[json.exception.out_of_range.403] key '), 'Reason')
                break

        variables = {'id': id, 'method': method, 'name': name, 'surname': surname, 'phone': phone}
        keys = {'id': id_key, 'method': method_key, 'name': name_key, 'surname': surname_key, 'phone': phone_key}
        for variable_name, variable in variables.items():
            key = keys[variable_name]
            if key and not isinstance(variable, str):
                assert_that(json.loads(repl)['reason'], contains_string(f'[json.exception.type_error.302] type must be string'), 'Reason')





