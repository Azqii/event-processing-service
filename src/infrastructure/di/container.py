from dishka import AsyncContainer, make_async_container

from infrastructure.di.providers import AppProvider


def create_container() -> AsyncContainer:
    return make_async_container(AppProvider())
