"""
Ошибки и замечания:
1)) Система позволяет создавать и изменять пользователя с невалидным телефоном

2) При ошибке есть поле "reason": "[json.exception.type_error.302]...". Не обработанная внутрення ошибка может быть потенциальной дырой.
"{
  "reason": "[json.exception.parse_error.101] parse error at line 1, column 3: syntax error while parsing value - invalid literal; last read: 'trs'",
  "status": "failure"
}"

3) При добавлении пользователя видим что поля 'id', 'method', 'name', 'surname', 'phone', 'age' - обязательные,что не указано в документации.

4) Нет обработки потенциально опасных символов - что может позволить атаковать систему более успешно. '@«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂',
'< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >', "<script>alert('XSS1')</script>","SELECT * FROM Users".

5) Нет обработки пробела - для значений поля 'method' это приводит к ошибке добавления пользователя.

6) Система позволят создавать и редактировать пользователя с любым значением возраста.

7) Необходимо ограничить длину вводимой строки методов
! При больших значениях  происходит переполнение буфера что приводит к закрытию работы приложения ! add, update
*** buffer overflow detected ***: ./tester.so terminated
/home/ubuntu/bin/start: line 3:   282 Aborted (core dumped) ./tester.so 0.0.0.0 4000
>
raise exceptions.IncompleteReadError(incomplete, n)
E  asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes

 raise self.connection_closed_exc()
E  websockets.exceptions.ConnectionClosedError: no close frame received or sent

8) Не строка в значениях ID:
 - ошибка не содержат поля id: id запроса, как указано в документации
'{
  "reason": "[json.exception.type_error.302] type must be string, but is null",
  "status": "failure"
}'

9)
При отсутствие ключа id:
- ошибка не содержат поля id: id запроса, как указано в документации
"{
  "reason": "[json.exception.out_of_range.403] key 'id' not found",
  "status": "failure"
}"

10) При отсутсвие ключа
- видим поле method": "", что не указано в документации
"{
  "id": "123",
  "method": "delete",
  "reason": "[json.exception.out_of_range.403] key 'phone' not found",
  "status": "failure"
}"

11) При не верном типе данных
- видим поле method": "", что не указано в документации
'{
  "id": "123",
  "method": "delete",
  "reason": "[json.exception.type_error.302] type must be string, but is null",
  "status": "failure"
}'

12) При не верном методе
- видим поле method": "", что не указано в документации и отсутствие поля reason
'{
  "id": "123",
  "method": "delete",
  "status": "failure"
}'

13) Перепутан статус при поиске по телефону.
'{
  "id": "123",
  "method": "select",
  "status": "failure",
  "users": [
    {
      "age": 45609,
      "name": "CHUCK1",
      "phone": "987654321",
      "surname": "dorris1"
    }
  ]
}'

14) После update не меняется поле age
      "age": 45609

15) Update на несуществующего пользователя отдает success - что не соответствует документации
'{
  "id": "1237659",
  "method": "update",
  "status": "success"
}'

16) Запрос методом select и отсутствующем поле для поиска - ложит приложение
('id', '123', 'method', 'select', 'test', '1234567')
terminate called without an active exception
/home/ubuntu/bin/start: line 3:   479 Aborted                 (core dumped) ./tester.so 0.0.0.0 4000

  raise exceptions.IncompleteReadError(incomplete, n)
E asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes

 raise self.connection_closed_exc()
E websockets.exceptions.ConnectionClosedError: no close frame received or sent

17) поиск по surname отдает только 1 сущность из базы. при наличие 2-х со схожим surname

18) Если во время поиска введены 2 и более поля для описка, одно из которых phone, то ищет только по полю phone,
 что не указано в документации.
"""
