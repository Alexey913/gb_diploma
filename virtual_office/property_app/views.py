import logging
from typing import Callable
from django import forms

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.db import models

from abstract_app.views import properties, menu, check_authorization, get_data_with_verbose_name

from .models import Transport, Realty
from .forms import TransportForm, RealtyForm


logger = logging.getLogger(__name__)

@check_authorization
def get_properties(request: HttpResponse, user_id: int) -> HttpResponse:
    context = {'title': 'Документы',
               'user_id': user_id,
               'properties': properties,
               'menu': menu}
    return render(request, 'property_app/property.html', context=context)



def show_property(user_id: int, entity: models.Model, list_fields: list) -> dict:
    properties = entity.objects.filter(user_id=user_id).all()
    if properties:
        output_property = []
        for item in properties:
            prop_instance = entity.objects.values(*list_fields).filter(pk=item.pk).first()
            object_property = get_object_or_404(entity, pk=item.pk)
            output_property.append(get_data_with_verbose_name(object_property, prop_instance))
        return output_property


def get_property(request: HttpResponse, user_id: int,
                 entity: models.Model, list_fields: list,
                 kind: str, in_title: str) -> HttpResponse:
    properties = show_property(user_id, entity, list_fields)
    if properties:
        context = {'properties': properties,
                   'title': f'Данные о {in_title}',
                   'user_id': user_id, 'menu': menu,
                   'add_property':'add_'+kind,
                   'change_property': 'change_'+kind}
        return render(request, 'property_app/show_property.html', context=context)
    return redirect('edit_'+kind, user_id=user_id)


@check_authorization
def get_realty(request:HttpResponse, user_id: int) -> Callable:
    list_fields = ['type_property', 'cadastral_number', 'cadastral_cost',
                   'adress', 'area', 'date_registration', 'description']
    return get_property(request, user_id, Realty, list_fields, 'realty', "недвижимости")


@check_authorization
def get_transport(request:HttpResponse, user_id: int) -> Callable:
    list_fields = ['type_property', 'brand', 'model', 'year_release',
                   'power_engine', 'registration_number', 'weigth',
                   'carrying', 'date_registration', 'description',]
    return get_property(request, user_id, Transport, list_fields, 'transport', "транспорте")


def check_property(user_id: int, entity: models.Model) -> bool:
    if entity.objects.filter(user_id=user_id).first():
        return True
    return False

def edit_property(request: HttpResponse, user_id: int,
                  entity: models.Model,
                  in_title:str, kind: str) -> Callable:
    if not check_property(user_id, entity):
        logger.debug(f"Нет данных о '{in_title}' пользователя {user_id} - \
переход к заполнению данных")
        messages.error(request,
        f'Нет сведений о {in_title} пользователя. Введите необходимые данные')
        if kind == 'realty':
            return add_transport(request, user_id)
        return add_realty(request, user_id)
    if kind =='realty':
        return show_realty_for_change(request, user_id)
    return show_transport_for_change(request, user_id)


@check_authorization
def edit_realty(request: HttpResponse, user_id: int) -> Callable:
    return edit_property(request, user_id, Realty,
                         'недвижимости', 'realty')


@check_authorization
def edit_transport(request: HttpResponse, user_id: int) -> Callable:
    return edit_property(request, user_id, Transport,
                         'транспорте', 'transport', 'Транспорт')

@check_authorization
def show_property_for_change(request: HttpResponse, user_id: int,
                             entity: models.Model, kind: str,
                             title: str) -> HttpResponse:
    properties = entity.objects.filter(user_id=user_id).all()
    context = {'property': properties,
               'title': title,
               'user_id': user_id,
               'change_property': 'change_'+kind,
               'add_property': 'add_'+kind,
               'menu': menu}
    return render(request, 'property_app/show_property.html', context=context)



def show_transport_for_change(request: HttpResponse, user_id: int) -> Callable:
    return show_property_for_change(request, user_id,
                                    Transport, 'transport', 'Транспорт')


def show_realty_for_change(request: HttpResponse, user_id: int) -> Callable:
    return show_property_for_change(request, user_id,
                                    Realty, 'realty', 'Недвижимость')


@check_authorization
def add_property(request: HttpResponse, user_id: int,
                 type_form: forms.ModelForm,
                 in_title: str, kind: str) -> HttpResponse:
    if request.method == 'POST':
        form = type_form(request.POST)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.user_id = user_id
            prop.save()
            messages.success(request, f"Успешное создание {in_title}")
            logger.info(f"Сохранение {in_title} пользователя {user_id}")
            return redirect('show_'+kind, user_id=user_id)
        logger.debug(
            f"Ошибка сохранения {in_title} пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = type_form()
    context = {'form': form,
               'title': 'Добавление '+in_title,
               'add_property': 'add_'+kind,
               'user_id': user_id,
               'menu': menu}
    return render(request, 'property_app/new_property.html', context=context)


@check_authorization
def add_transport(request: HttpResponse, user_id: int) -> Callable:
    return add_property(request, user_id, TransportForm,
                 'транспортного средства', 'transport')


@check_authorization
def add_realty(request: HttpResponse, user_id: int) -> Callable:
    return add_property(request, user_id, RealtyForm,
                 'объекта недвижимости', 'realty')


@check_authorization
def change_transport(request, user_id, transport_id):
    current_transport = Transport.objects.filter(pk=transport_id).first()
    if request.method == 'POST':
        form = TransportForm(request.POST)
        if form.is_valid():
            data_by_form = form.cleaned_data
            for field, value in data_by_form.items():
                if value:
                    setattr(current_transport, field, value)
            current_transport.save()
            #     data_by_form['type_property'] or current_transport.type_property
            # current_transport.brand = \
            #     data_by_form['brand'] or current_transport.brand
            # current_transport.model = \
            #     data_by_form['model'] or current_transport.model
            # current_transport.year_release = \
            #     data_by_form['year_release'] or current_transport.year_release
            # current_transport.registration_number = \
            #     data_by_form['registration_number'] or \
            #         current_transport.registration_number
            # current_transport.weigth = \
            #     data_by_form['weigth'] or current_transport.weigth
            # current_transport.carrying = \
            #     data_by_form['carrying'] or current_transport.carrying
            # current_transport.date_registration = \
            #     data_by_form['date_registration'] or current_transport.date_registration
            # current_transport.description = \
            #     data_by_form['description'] or current_transport.description
            logger.info(f"Изменение данных о транспортном средстве {transport_id} \
пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('show_transport', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных объекта недвижимости {transport_id} \
пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = TransportForm()
    context = {'form': form,
               'title': 'Изменение данных о транспортном средстве',
               'user_id': user_id,
               'change_property': 'change_transport',
               'del_property': 'del_transport',
               'property': current_transport,
               'menu': menu}
    return render(request, 'property_app/edit_property.html', context)


@check_authorization
def change_realty(request, user_id, realty_id):
    current_realty = Realty.objects.filter(pk=realty_id).first()
    if request.method == 'POST':
        form = RealtyForm(request.POST)
        if form.is_valid():
            data_by_form = form.cleaned_data
            current_realty.type_property = \
                data_by_form['type_property'] or current_realty.type_property
            current_realty.cadastral_number = \
                data_by_form['cadastral_number'] or current_realty.cadastral_number
            current_realty.cadastral_cost = \
                data_by_form['cadastral_cost'] or current_realty.cadastral_cost
            current_realty.date_registration = \
                data_by_form['date_registration'] or current_realty.date_registration
            current_realty.adress =  data_by_form['adress'] or current_realty.adress
            current_realty.area = data_by_form['area'] or current_realty.area
            current_realty.description = \
                data_by_form['description'] or current_realty.description
            logger.info(f"Изменение данных об объекте недвижимости {realty_id} пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('show_realty', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных объекта недвижимости {realty_id} пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = RealtyForm()
    context = {'form': form,
               'title': 'Изменение данных об объекте недвижимости',
               'user_id': user_id,
               'change_property': 'change_realty',
               'del_property': 'del_realty',
               'property': current_realty,
               'menu': menu}
    return render(request, 'property_app/edit_property.html', context)


def del_property(request: HttpResponse, user_id: int, property_id: int,
                 entity: models.Model, in_title: str, kind: str) -> HttpResponse:
    try:
        entity.objects.filter(pk=property_id).delete()
        logger.info(f"Удалены данные о {in_title} {property_id} \
пользователя {user_id}")
        messages.success(request, "Данные успешно удалены")
    except:
        logger.debug(
            f"Ошибка удаления данных о {in_title} {property_id} \
пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('edit_'+kind, user_id=user_id)

@check_authorization
def del_realty(request: HttpResponse, user_id: int,
               realty_id: int) -> HttpResponse:
    return del_property(request, user_id, realty_id, Realty,
                        'объекте недвижимости', 'realty')


@check_authorization
def del_transport(request: HttpResponse, user_id: int,
               transport_id: int) -> HttpResponse:
    return del_property(request, user_id, transport_id, Transport,
                        'транспортном средстве', 'transport')