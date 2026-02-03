## Типы связей между таблицами в схеме

![](../img/cinema_schema_diagram.png)

|      Тип связи       | Таблица 1 | Таблица 2       |
|:--------------------:|-----------|-----------------|
| Один-ко-многим (1:N) | actors    | movie_cast      |
| Один-ко-многим (1:N) | movie     | movie_cast      |
| Один-ко-многим (1:N) | movie     | oscar_awarded   |
| Один-ко-многим (1:N) | movie     | movie_direction |
| Один-ко-многим (1:N) | director  | movie_direction |

