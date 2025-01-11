from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')

class ObjList(Generic[T]):
    """Объекты класса ObjList должны иметь следующий набор приватных локальных свойств:
    __next - ссылка на следующий объект связного списка (если следующего объекта нет, то __next = None);
    __prev - ссылка на предыдущий объект связного списка (если предыдущего объекта нет, то __prev = None);
    __data - данные типа T.
    Также в классе ObjList должны быть реализованы следующие сеттеры и геттеры:
    """

    def __init__(self, data: T, previous_obj: Optional["ObjList"] = None, next_obj: Optional["ObjList"] = None) -> None:
        self.__data: T = data
        self.__prev: Optional["ObjList"] = previous_obj
        self.__next: Optional["ObjList"] = next_obj

    def set_next(self, obj: "ObjList") -> None:
        """изменение приватного свойства __next на значение obj;"""
        self.__next = obj

    def set_prev(self, obj: "ObjList") -> None:
        """изменение приватного свойства __prev на значение obj;"""
        self.__prev = obj

    def get_next(self) -> Optional["ObjList"]:
        """получение значения приватного свойства __next;"""
        return self.__next

    def get_prev(self) -> Optional["ObjList"]:
        """получение значения приватного свойства __prev;"""
        return self.__prev

    def set_data(self, data: T) -> None:
        """изменение приватного свойства __data на значение data;"""
        self.__data = data

    def get_data(self) -> T:
        """получение значения приватного свойства __data."""
        return self.__data


class LinkedList(Generic[T]):
    """объявите класс LinkedList, который будет представлять связный список в целом
    и иметь набор следующих методов:
    И локальные публичные атрибуты:
    head - ссылка на первый объект связного списка (если список пустой, то head = None);
    tail - ссылка на последний объект связного списка (если список пустой, то tail = None).
    """

    def __init__(self) -> None:
        self.head: Optional[ObjList[T]] = None
        self.tail: Optional[ObjList[T]] = None

    def add_obj(self, obj: ObjList[T]) -> None:
        """добавление нового объекта obj класса ObjList в конец связного списка;"""
        if self.head is None:
            self.head = obj
            self.tail = obj
        else:
            self.tail.set_next(obj)
            tail = self.tail
            self.tail = obj
            self.tail.set_prev(tail)

    def remove_obj(self) -> None:
        """удаление последнего объекта из связного списка;"""
        if self.tail and self.tail.get_prev():
            self.tail.get_prev().set_next(None)
            self.tail = self.tail.get_prev()
        elif self.head == self.tail:  # Если остался только один элемент
            self.head = None
            self.tail = None

    def get_data(self) -> List[T]:
        """получение списка из данных всех объектов связного списка."""
        cur = self.head
        data = []
        while cur:
            data.append(cur.get_data())
            cur = cur.get_next()

        return data


# Пример использования
ob = ObjList("данные 1")