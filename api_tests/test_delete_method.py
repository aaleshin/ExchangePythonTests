import pytest
import json
from hamcrest import *
from misc.common_methods import ws_request, generate_random_string


@pytest.mark.usefixtures("service_url")
class TestDeleteMethod:
    """
    Check Delete Method
    """
    @pytest.mark.parametrize("id, phone, status_in_response",
        [
            ('1231', '12345671', 'success'),
            ('1231', generate_random_string(), 'failure'),  # другой номер но id тот же
            ('', '12345671', 'success'),  # пустой id
            ('125631', '12345671', 'success'),  # другой id
            ('1231', '', 'failure'),  # пустое phone
            ('12 31 ', ' 1234 5671 ', 'failure'),  # пробелы в начале, в середине и в конце
            ('12 31 ', ' 12345671 ', 'failure'),  # пробелы в начале и в конце
            ('double', '12345671', 'failure'),  # удаление уже удаленного
        ])
    @pytest.mark.asyncio
    async def test_check_delete_positive_functionality(self, service_url, id, phone, status_in_response):
        request_text = json.dumps({
            'id': '1231',
            'method': 'add',
            'name': 'Chuck1',
            'surname': 'Dorris1',
            'phone': '12345671',
            'age': 12345
        })
        await ws_request(service_url, request_text)

        delete_text = json.dumps({'id': id, 'method': 'delete', 'phone': phone})
        repl_del = await ws_request(service_url, delete_text)
        if id == 'double':
            repl_del = await ws_request(service_url, delete_text)

        if status_in_response == 'failure':
            assert_that(json.loads(repl_del)['status'], equal_to(status_in_response), 'Status')
            delete_after = json.dumps({'id': '123', 'method': 'delete', 'phone': '12345671'})
            await ws_request(service_url, delete_after)
        else:
            assert_that(json.loads(repl_del)['id'], equal_to(id), 'ID')
            assert_that(json.loads(repl_del)['method'], equal_to('delete'), 'Method')
            assert_that(json.loads(repl_del)['status'], equal_to(status_in_response), 'Status')

    @pytest.mark.parametrize("id, name, surname, age, status_in_response",
                             [
                                 ('12317987', 'Chuck2',  'Dorris2', 123456, 'success'),  # удаление после редактирования id
                                 ('12317', 'BlUCK25', 'Dorris2', 123456, 'success'),  # удаление после редактирования name
                                 ('12317', 'Chuck2', 'boris', 123456, 'success'),  # удаление после редактирования surname
                                 ('12317', 'Chuck2', 'Dorris2', 99999, 'success'),  # удаление после редактирования age
                                 ('131313', 'тест', 'тестер', 88888, 'success'),  # удаление после редактирования 4 полей
                             ])
    @pytest.mark.asyncio
    async def test_check_delete_after_update_functionality(self, service_url, id, name, surname, age, status_in_response):
        request_text = json.dumps({
            'id': '12317',
            'method': 'add',
            'name': 'Chuck2',
            'surname': 'Dorris2',
            'phone': '123456719',
            'age': 123456
        })
        await ws_request(service_url, request_text)

        request_updated_text = json.dumps({
            'id': id,
            'method': 'update',
            'name': name,
            'surname': surname,
            'phone': '123456719',
            'age': age
        })
        await ws_request(service_url, request_updated_text)

        delete_text = json.dumps({'id': id, 'method': 'delete', 'phone': '123456719'})
        repl_del = await ws_request(service_url, delete_text)
        assert_that(json.loads(repl_del)['id'], equal_to(id), 'ID')
        assert_that(json.loads(repl_del)['method'], equal_to('delete'), 'Method')
        assert_that(json.loads(repl_del)['status'], equal_to(status_in_response), 'Status')

    @pytest.mark.parametrize("id_key, id, method_key, method, phone_key, phone, status_in_response",
        [
            ('id', None, 'method', 'delete', 'phone', '1234567', 'failure'),  # отсутствующий id
            ('id', '123', 'method', None, 'phone', '1234567', 'failure'),  # отсутствующий method
            ('id', '123', 'method', 'delete', 'phone', None, 'failure'),  # отсутствующий phone
            ('test', '123', 'method', 'delete', 'phone', '1234567', 'failure'),  # нет поля id
            ('id', '123', 'test', 'delete', 'phone', '1234567', 'failure'),  # нет поля method
            ('id', '123', 'method', 'delete', 'test', '1234567', 'failure'),  # нет поля phone
            ('id', 1236, 'method', 'delete', 'phone', '1234567', 'failure'),  # не верный тип данных для id
            ('id', '123', 'method', 123, 'phone', '1234567', 'failure'),  # не верный тип данных для method
            ('id', '123', 'method', 'update', 'phone', '1234567', 'failure'),  # не верный метод
            ('id', '123', 'method', 'delete', 'phone', 111, 'failure'),  # не верный тип данных для phone
            ('id', '@«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂', 'method', 'delete', 'phone', "SELECT * FROM Users", 'failure'),  # нет обработки потенциально опасных символов
            ('id', '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >', 'method', 'delete', 'phone', "<script>alert('XSS1')</script>", 'failure'),  # нет обработки потенциально опасных символов
            ('id', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
             'method', 'delete', 'phone', '21231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444212312341413434344442123123414134343444421231234141343434444',
             'failure')
        ])
    @pytest.mark.asyncio
    async def test_check_delete_negative_functionality(self, service_url, id_key, id, method_key, method, phone_key, phone, status_in_response):

        delete_text = json.dumps({id_key: id, method_key: method, phone_key: phone})
        repl_del = await ws_request(service_url, delete_text)
        assert_that(json.loads(repl_del)['status'], equal_to(status_in_response), 'Status')
        if id is not None and id_key == 'id' and id is isinstance(id, str):
            assert_that(json.loads(repl_del)['id'], equal_to(id), 'ID')

        for key, value in zip((id_key, method_key, phone_key), ('id', 'method', 'phone')):
            if key != value:
                assert_that(json.loads(repl_del)['reason'], contains_string('[json.exception.out_of_range.403] key '),'Reason')
                break

        variables = {'id': id, 'method': method, 'phone': phone}
        keys = {'id': id_key, 'method': method_key, 'phone': phone_key}
        for variable_name, variable in variables.items():
            key = keys[variable_name]
            if key and not isinstance(variable, str):
                assert_that(json.loads(repl_del)['reason'], contains_string(f'[json.exception.type_error.302] type must be string'), 'Reason')

