class LinkedList:
    """объявите класс LinkedList, который будет представлять связный список в целом
    и иметь набор следующих методов:
    И локальные публичные атрибуты:
    head - ссылка на первый объект связного списка (если список пустой, то head = None);
    tail - ссылка на последний объект связного списка (если список пустой, то tail = None).
    """

    def add_obj(self, obj):
        """добавление нового объекта obj класса ObjList в конец связного списка;
        """
        pass

    def remove_obj(self):
        """удаление последнего объекта из связного списка;
        """
        pass

    def get_data(self):
        """получение списка из строк локального свойства __data всех объектов связного списка.
        """
        pass


class ObjList:
    """Объекты класса ObjList должны иметь следующий набор приватных локальных свойств:
    __next - ссылка на следующий объект связного списка (если следующего объекта нет, то __next = None);
    __prev - ссылка на предыдущий объект связного списка (если предыдущего объекта нет, то __prev = None);
    __data - строка с данными.
    Также в классе ObjList должны быть реализованы следующие сеттеры и геттеры:
    """

    def set_next(self, obj):
        """изменение приватного свойства __next на значение obj;
        """
        pass

    def set_prev(self, obj):
        """изменение приватного свойства __prev на значение obj;
        """
        pass

    def get_next(self):
        """получение значения приватного свойства __next;
        """
        pass

    def get_prev(self):
        """получение значения приватного свойства __prev;
        """
        pass

    def set_data(self, data):
        """изменение приватного свойства __data на значение data;
        """
        pass

    def get_data(self):
        """получение значения приватного свойства __data.
        """
        pass


ob = ObjList("данные 1")
