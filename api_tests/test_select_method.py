import pytest
import json
from hamcrest import *
from misc.common_methods import ws_request, generate_random_string


@pytest.mark.usefixtures("service_url")
class TestSelectMethod:
    """
    Check Select Method
    """
    @pytest.mark.parametrize("id, changed_field, changed_value, status_in_response",
     [
         ('12313', 'phone', '12345671', 'success'),
         ('', 'phone', '12345671', 'success'),  # пустой id
         ('125631987', 'phone', '12345671', 'success'),  # другой id
         ('double', 'phone', '12345671', 'success'),  # поиск уже найденного
         ('12313', 'phone', '', 'failure'),  # пустое phone
         ('12313', 'phone', generate_random_string(), 'failure'),  # другой номер но id тот же
         ('12313', 'name', 'Chuck1', 'success'),
         ('', 'name', 'Chuck1', 'success'),  # пустой id
         ('125631987', 'name', 'Chuck1', 'success'),  # другой id
         ('double', 'name', 'Chuck1', 'success'),  # поиск уже найденного
         ('12313', 'name', '', 'failure'),  # пустое name
         ('12313', 'name', generate_random_string(), 'failure'),  # другое name но id тот же
         ('12313', 'surname', 'Dorris1', 'success'),
         ('', 'surname', 'Dorris1', 'success'),  # пустой id
         ('125631987', 'surname', 'Dorris1', 'success'),  # другой id
         ('double', 'surname', 'Dorris1', 'success'),  # поиск уже найденного
         ('12313', 'surname', '', 'failure'),  # пустое surname
         ('12313', 'surname', generate_random_string(), 'failure'),  # другое surname но id тот же
         ('123 13 ', 'phone', ' 1234 5671 ', 'failure'),  # пробелы в начале, в середине и в конце
         (' 12 313 ', 'phone', ' 12345671 ', 'failure'),  # пробелы в начале и в конце
     ])
    @pytest.mark.asyncio
    async def test_check_select(self, service_url, id, changed_field, changed_value, status_in_response):
        request_text = json.dumps({
            'id': '12313',
            'method': 'add',
            'name': 'Chuck1',
            'surname': 'Dorris1',
            'phone': '12345671',
            'age': 12345
        })
        await ws_request(service_url, request_text)
        if changed_field in ("name", "surname"):
            request_text2 = json.dumps({
                'id': '12313',
                'method': 'add',
                'name': 'Chuck1',
                'surname': 'Dorris1',
                'phone': '12345672',
                'age': 12345
            })
            await ws_request(service_url, request_text2)

        selected_user = json.dumps({'id': id, 'method': 'select', changed_field: changed_value})
        repl_sel = await ws_request(service_url, selected_user)
        if id == 'double':
            repl_sel = await ws_request(service_url, selected_user)

        if status_in_response == 'failure':
            assert_that(json.loads(repl_sel)['status'], equal_to(status_in_response), 'Status')
            assert_that(json.loads(repl_sel)['id'], equal_to(id), 'ID')
            assert_that(json.loads(repl_sel)['method'], equal_to('select'), 'Method')
        elif changed_field in ("name", "surname"):
            assert_that(json.loads(repl_sel)['id'], equal_to(id), 'ID')
            assert_that(json.loads(repl_sel)['method'], equal_to('select'), 'Method')
            assert_that(json.loads(repl_sel)['status'], equal_to('failure'), 'Status')  # баг 13 - заменить на success
            assert_that(json.loads(repl_sel)['users'][0]['name'], equal_to('Chuck1'), 'Name')
            assert_that(json.loads(repl_sel)['users'][0]['surname'], equal_to('Dorris1'), 'Surname')
            assert_that(json.loads(repl_sel)['users'][0]['age'], equal_to(12345), 'Age')
            assert_that(json.loads(repl_sel)['users'][0]['phone'], equal_to('12345671'), 'Phone')
            assert_that(json.loads(repl_sel)['users'][1]['name'], equal_to('Chuck1'), 'Name')
            assert_that(json.loads(repl_sel)['users'][1]['surname'], equal_to('Dorris1'), 'Surname')
            assert_that(json.loads(repl_sel)['users'][1]['age'], equal_to(12345), 'Age')
            assert_that(json.loads(repl_sel)['users'][1]['phone'], equal_to('12345672'), 'Phone')

            delete_after2 = json.dumps({'id': '12313', 'method': 'delete', 'phone': '12345672'})
            await ws_request(service_url, delete_after2)
        else:
            assert_that(json.loads(repl_sel)['id'], equal_to(id), 'ID')
            assert_that(json.loads(repl_sel)['method'], equal_to('select'), 'Method')
            assert_that(json.loads(repl_sel)['status'], equal_to('failure'), 'Status')  # баг 13 - заменить на success
            assert_that(json.loads(repl_sel)['users'][0]['name'], equal_to('Chuck1'), 'Name')
            assert_that(json.loads(repl_sel)['users'][0]['surname'], equal_to('Dorris1'), 'Surname')
            assert_that(json.loads(repl_sel)['users'][0]['age'], equal_to(12345), 'Age')
            assert_that(json.loads(repl_sel)['users'][0]['phone'], equal_to('12345671'), 'Phone')

        delete_after1 = json.dumps({'id': '12313', 'method': 'delete', 'phone': '12345671'})
        await ws_request(service_url, delete_after1)

    @pytest.mark.parametrize("first_changed_field, first_value, second_changed_field, second_value,  status_in_response",
     [
         ('phone', '12345671', 'name', 'Chuck1', 'success'),  # поиск по phone и name
         ('surname', 'Dorris1', 'phone', '12345671', 'success'),  # поиск по phone и surname
         ('name', 'Chuck1', 'surname', 'Dorris1', 'success'),  # поиск по surname и name
         ('surname', 'Chuck1', 'name', 'Dorris1', 'success'),  # поиск по name и name surname
     ])
    @pytest.mark.asyncio
    async def test_check_two_fields(self, service_url, first_changed_field, first_value, second_changed_field, second_value,  status_in_response):
        request_text = json.dumps({
            'id': '12313',
            'method': 'add',
            'name': 'Chuck1',
            'surname': 'Dorris1',
            'phone': '12345671',
            'age': 12345
        })
        await ws_request(service_url, request_text)
        request_text2 = json.dumps({
            'id': '12313',
            'method': 'add',
            'name': 'Chuck1',
            'surname': 'Dorris1',
            'phone': '12345672',
            'age': 12345
        })
        await ws_request(service_url, request_text2)

        selected_user = json.dumps({'id': '12313', 'method': 'select', first_changed_field: first_value, second_changed_field: second_value})
        repl_sel = await ws_request(service_url, selected_user)

        if first_changed_field in ("name", "surname") and second_changed_field in ("name", "surname"):
            assert_that(json.loads(repl_sel)['id'], equal_to('12313'), 'ID')
            assert_that(json.loads(repl_sel)['method'], equal_to('select'), 'Method')
            assert_that(json.loads(repl_sel)['status'], equal_to('failure'), 'Status')  # баг 13 - заменить на success
            assert_that(json.loads(repl_sel)['users'][0]['name'], equal_to('Chuck1'), 'Name')
            assert_that(json.loads(repl_sel)['users'][0]['surname'], equal_to('Dorris1'), 'Surname')
            assert_that(json.loads(repl_sel)['users'][0]['age'], equal_to(12345), 'Age')
            assert_that(json.loads(repl_sel)['users'][0]['phone'], equal_to('12345671'), 'Phone')
            assert_that(json.loads(repl_sel)['users'][1]['name'], equal_to('Chuck1'), 'Name')
            assert_that(json.loads(repl_sel)['users'][1]['surname'], equal_to('Dorris1'), 'Surname')
            assert_that(json.loads(repl_sel)['users'][1]['age'], equal_to(12345), 'Age')
            assert_that(json.loads(repl_sel)['users'][1]['phone'], equal_to('12345672'), 'Phone')

            delete_after2 = json.dumps({'id': '12313', 'method': 'delete', 'phone': '12345672'})
            await ws_request(service_url, delete_after2)
        else:
            assert_that(json.loads(repl_sel)['id'], equal_to('12313'), 'ID')
            assert_that(json.loads(repl_sel)['method'], equal_to('select'), 'Method')
            assert_that(json.loads(repl_sel)['status'], equal_to('failure'), 'Status')  # баг 13 - заменить на success
            assert_that(json.loads(repl_sel)['users'][0]['name'], equal_to('Chuck1'), 'Name')
            assert_that(json.loads(repl_sel)['users'][0]['surname'], equal_to('Dorris1'), 'Surname')
            assert_that(json.loads(repl_sel)['users'][0]['age'], equal_to(12345), 'Age')
            assert_that(json.loads(repl_sel)['users'][0]['phone'], equal_to('12345671'), 'Phone')

        delete_after1 = json.dumps({'id': '12313', 'method': 'delete', 'phone': '12345671'})
        await ws_request(service_url, delete_after1)

    @pytest.mark.parametrize("id_key, id, method_key, method, expected_key, variable_key, variable_name, status_in_response",
     [
         ('id', None, 'method', 'select', 'phone', 'phone', '1234567', 'failure'),  # отсутствующий id
         ('id', '123', 'method', 'select', 'phone', 'phone', None, 'failure'),  # отсутствующий phone
         ('id', '123', 'method', 'select', 'name', 'name', None, 'failure'),  # отсутствующий name
         ('id', '123', 'method', 'select', 'surname', 'surname', None, 'failure'),  # отсутствующий surname
         ('test', '123', 'method', 'select', 'phone', 'phone', '1234567', 'failure'),  # нет поля id
         ('id', '123', 'test', 'select', 'phone', 'phone', '1234567', 'failure'),  # нет поля method
         ('id', '123', 'method', 'select', 'phone', 'test', '1234567', 'failure'),  # нет поля для поиска - баг 16
         ('id', 1236, 'method', 'select',  'phone', 'phone', '1234567', 'failure'),  # не верный тип данных для id
         ('id', '123', 'method', 'select',  'phone', 'phone', 111, 'failure'),  # не верный тип данных для phone
         ('id', '123', 'method', 'select', 'name', 'name', 111, 'failure'),  # не верный тип данных для name
         ('id', '123', 'method', 'select', 'surname', 'surname', 111, 'failure'),  # не верный тип данных для surname
         ('id', '@«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂', 'method', 'select', 'phone', 'phone', "SELECT * FROM Users", 'failure'),  # нет обработки потенциально опасных символов
         ('id', '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >',
          'method', 'select', 'phone', 'phone', "<script>alert('XSS1')</script>", 'failure'),  # нет обработки потенциально опасных символов
         ('id', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
          'method', 'select', 'phone', 'phone', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
          'failure')  # перегрузка
     ])
    @pytest.mark.asyncio
    async def test_check_delete_negative_functionality(self, service_url, id_key, id, method_key, method, expected_key, variable_key, variable_name, status_in_response):

        selected_text = json.dumps({id_key: id, method_key: method, variable_key: variable_name})
        repl_sel = await ws_request(service_url, selected_text)
        assert_that(json.loads(repl_sel)['status'], equal_to(status_in_response), 'Status')
        if id is not None and id_key == 'id' and isinstance(id, str):
            assert_that(json.loads(repl_sel)['id'], equal_to(id), 'ID')

        for key, value in zip((id_key, method_key, variable_key), ('id', 'method', expected_key)):
            if key != value:
                assert_that(json.loads(repl_sel)['reason'], contains_string('[json.exception.out_of_range.403] key '),
                            'Reason')
                break

        variables = {'id': id, 'method': method, variable_name: variable_key}
        keys = {'id': id_key, 'method': method_key, variable_name: variable_key}
        for variable_name, variable in variables.items():
            key = keys[variable_name]
            if key and not isinstance(variable, str):
                assert_that(json.loads(repl_sel)['reason'],
                            contains_string(f'[json.exception.type_error.302] type must be string'), 'Reason')
