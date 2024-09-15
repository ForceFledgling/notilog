import logging

from fastapi import APIRouter, Query

from app.controllers.menu import menu_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.menus import *
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.admin import Menu
from fastapi import Depends, Query

from app.core.database import get_session, SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter()


# @router.get("/list", summary="Просмотр списка меню")
# async def list_menu(
#     page: int = Query(1, description="Номер страницы"),
#     page_size: int = Query(10, description="Количество на странице"),
# ):
#     async def get_menu_with_children(menu_id: int):
#         menu = await menu_controller.model.get(id=menu_id)
#         menu_dict = await menu.to_dict()
#         child_menus = await menu_controller.model.filter(parent_id=menu_id).order_by("order")
#         menu_dict["children"] = [await get_menu_with_children(child.id) for child in child_menus]
#         return menu_dict

#     parent_menus = await menu_controller.model.filter(parent_id=0).order_by("order")
#     res_menu = [await get_menu_with_children(menu.id) for menu in parent_menus]
#     return SuccessExtra(data=res_menu, total=len(res_menu), page=page, page_size=page_size)

@router.get("/list", summary="Просмотр списка меню")
async def list_menu(
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(10, description="Количество на странице"),
):
    async def get_menu_with_children(menu_id: int):
        menu = await menu_controller.model.get(id=menu_id)
        menu_dict = await menu.to_dict()
        child_menus_query = menu_controller.model.filter(parent_id=menu_id)
        child_menus_query = child_menus_query.order_by("order")
        async with SessionLocal() as session:
            child_menus = await session.execute(child_menus_query)
            child_menus = child_menus.scalars().all()
        menu_dict["children"] = [await get_menu_with_children(child.id) for child in child_menus]
        return menu_dict

    parent_menus_query = menu_controller.model.filter(parent_id=0)
    parent_menus_query = parent_menus_query.order_by("order")
    async with SessionLocal() as session:
        parent_menus = await session.execute(parent_menus_query)
        parent_menus = parent_menus.scalars().all()
    res_menu = [await get_menu_with_children(menu.id) for menu in parent_menus]
    return SuccessExtra(data=res_menu, total=len(res_menu), page=page, page_size=page_size)



@router.get("/get", summary="Просмотр меню")
async def get_menu(
    menu_id: int = Query(..., description="ID меню"),
):
    result = await menu_controller.get(id=menu_id)
    return Success(data=result)


@router.post("/create", summary="Создание меню")
async def create_menu(
    menu_in: MenuCreate,
):
    await menu_controller.create(obj_in=menu_in)
    return Success(msg="Создание успешно")


@router.post("/update", summary="Обновление меню")
async def update_menu(
    menu_in: MenuUpdate,
):
    await menu_controller.update(id=menu_in.id, obj_in=menu_in)
    return Success(msg="Обновление успешно")


@router.delete("/delete", summary="Удаление меню")
async def delete_menu(
    id: int = Query(..., description="ID меню"),
):
    child_menu_count = await menu_controller.model.filter(parent_id=id).count()
    if child_menu_count > 0:
        return Fail(msg="Невозможно удалить меню с дочерними меню")
    await menu_controller.remove(id=id)
    return Success(msg="Удаление успешно")