from itertools import count
from typing import Dict, List, Any


class Router:
    def __init__(self) -> None:
        """
        Класс для описания работы роутеров в сети (в данной задаче полагается один роутер).
        И одно обязательное локальное свойство (могут быть и другие свойства):
        buffer - список для хранения принятых от серверов пакетов (объектов класса Data).
        """
        self.buffer: List[Data] = []
        self.servers: Dict[int, "Server"] = {}

    def link(self, server: "Server") -> None:
        """
        Метод для присоединения сервера server (объекта класса Server) к роутеру.
        :param server: Сервер, который мы хотим привязать к данному роутеру.
        :return: Ничего не возвращает.
        """
        self.servers[server.ip] = server
        server.router = self

    def unlink(self, server: "Server") -> None:
        """
        Метод для отсоединения сервера server (объекта класса Server) от роутера
        :param server:
        :return:
        """
        s = self.servers.pop(server.ip, False)
        if s:
            s.router = None

    def send_data(self) -> None:
        """
        Метод для отправки всех пакетов (объектов класса Data) из буфера роутера
        соответствующим серверам (после отправки буфер должен очищаться).
        :return: Ничего не возвращает
        """
        for d in self.buffer:
            if d.ip in self.servers:
                self.servers[d.ip].buffer.append(d)
        self.buffer.clear()


class Server:
    """
    Для описания работы серверов в сети.
    Соответственно в объектах класса Server должны быть локальные свойства:
    - buffer - список принятых пакетов (изначально пустой);
    - ip - IP-адрес текущего сервера.
    """
    __counter = count(1)

    def __init__(self):
        self.buffer: List["Data"] = []
        self.ip = self.__counter.__next__()
        self.router = None

    def send_data(self, data: "Data") -> None:
        """
        Для отправки информационного пакета data (объекта класса Data)
        с указанным IP-адресом получателя (пакет отправляется роутеру и
        сохраняется в его буфере - локальном свойстве buffer);
        :param data: информация, которую мы хотим отправить.
        :return: Ничего не возвращает
        """
        if self.router:
            self.router.buffer.append(data)

    def get_data(self) -> List["Data"]:
        """
        Возвращает список принятых пакетов (если ничего принято не было,
        то возвращается пустой список) и очищает входной буфер;
        :return: список с информацией от сервера.
        """
        b = self.buffer.copy()
        self.buffer.clear()
        return b

    def get_ip(self) -> int:
        """
        Геттер, чтобы получить IP с сервера
        :return: возвращает IP сервера - целое число.
        """
        return self.ip


class Data:
    def __init__(self, data: Any, ip: int) -> None:
        """
        Класс для описания пакета информации.
        Наконец, объекты класса Data должны содержать, два следующих локальных свойства:
        :param data: Передаваемые данные (строка);
        :param ip: IP-адрес назначения.
        """
        self.data = data
        self.ip = ip
