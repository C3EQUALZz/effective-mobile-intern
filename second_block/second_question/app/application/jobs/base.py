from taskiq import AsyncBroker

# TODO: перенести инициализацию jobs в папку core, как раз здесь можно будет настроить broker.
# Как раз поставить запуск контейнера на эту штуку.

broker: AsyncBroker | None = None
