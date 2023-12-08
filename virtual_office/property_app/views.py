import logging

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages

from abstract_app.views import properties, menu, check_authorization, check_doc, get_data_with_verbose_name

from .models import Transport, Realty
from .forms import TransportForm, RealtyForm
from user_app.models import Data


logger = logging.getLogger(__name__)

@check_authorization
def get_properties(request, user_id):
    context = {'title': 'Документы',
               'user_id': user_id,
               'properties': properties,
               'menu': menu}
    return render(request, 'property_app/property.html', context=context)


def show_realty(user_id):
    realties = Realty.objects.filter(user_id=user_id).all()
    if realties:
        output_realty = []
        for real in realties:
            realty = Realty.objects.values('type_property', 'cadastral_number',
                                           'cadastral_cost', 'adress', 'area',
                                           'date_rregistration', 'description',
                                           ).filter(pk=real.pk).first()
            object_realty = get_object_or_404(Realty, pk=real.pk)
            output_realty.append(get_data_with_verbose_name(object_realty, realty))
        return output_realty


@check_authorization
def get_realty(request, user_id):
    properties = show_realty(user_id)
    if properties:
        context = {'properties': properties,
                   'title': 'Данные о недвижимости',
                   'user_id': user_id, 'menu': menu}
        return render(request, 'show_property.html', context=context)
    return redirect('edit_realty', user_id=user_id)


@check_authorization
def edit_realty(request, user_id):
    if not check_doc(user_id, Realty):
        logger.debug(f"Нет данных о недвижимости пользователя {user_id} - \
переход к заполнению данных")
        messages.error(request,
        'Нет сведений о недвижимости пользователя. Введите необходимые данные')
        return add_realty(request, user_id)
    return show_realty_for_change(request, user_id)


@check_authorization
def show_realty_for_change(request, user_id):
    realty = Realty.objects.filter(user_id=user_id).all()
    context = {'property': realty,
               'title': 'Недвижимость',
               'user_id': user_id,
               'change_property': 'change_realty',
               'add_property': 'add_realty',
               'menu': menu}
    return render(request, 'property_app/show_property.html', context=context)


@check_authorization
def add_realty(request, user_id):
    if request.method == 'POST':
        form = RealtyForm(request.POST)
        if form.is_valid():
            realty = form.save(commit=False)
            realty.user_id = user_id
            realty.save()
            messages.success(request, "Создан объект недвижимости")
            logger.info(f"Сохранение данных об объекте недвижимости пользователя {user_id}")
            return redirect('show_realty', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных об объекте недвижимости пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = RealtyForm()
    context = {'form': form,
               'title': 'Новый объект недвижимости',
               'add_property': 'add_realty',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'property_app/new_property.html', context=context)


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
            return redirect('property', user_id=user_id)
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


@check_authorization
def del_realty(request, user_id, realty_id):
    try:
        Realty.objects.filter(pk=realty_id).delete()
        logger.info(f"Удалены данные об объекте недвижимости {realty_id} \
пользователя {user_id}")
        messages.success(request, "Данные успешно удалены")
    except:
        logger.debug(
            f"Ошибка удаления данных об объекте недвижимости {realty_id} \
пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('edit_realty', user_id=user_id)


def show_transport(user_id):
    transports = Transport.objects.filter(user_id=user_id).all()
    if transports:
        output_transport = []
        for tr in transports:
            transport = Transport.objects.values('type_property', 'brand', 'model',
                                                 'year_release', 'power_engine',
                                                 'registration_number', 'weigth', 'carrying',
                                                 'date_rregistration', 'description',
                                           ).filter(pk=tr.pk).first()
            object_transport = get_object_or_404(Transport, pk=tr.pk)
            output_transport.append(get_data_with_verbose_name(object_transport, transport))
        return output_transport


@check_authorization
def get_transport(request, user_id):
    properties = show_transport(user_id)
    if properties:
        context = {'properties': properties,
                   'title': 'Данные о транспорте',
                   'user_id': user_id, 'menu': menu}
        return render(request, 'show_property.html', context=context)
    return redirect('edit_transport', user_id=user_id)


@check_authorization
def edit_transport(request, user_id):
    if not check_doc(user_id, Transport):
        logger.debug(f"Нет данных о недвижимости пользователя {user_id} - \
переход к заполнению данных")
        messages.error(request,
        'Нет сведений о недвижимости пользователя. Введите необходимые данные')
        return add_transport(request, user_id)
    return show_transport_for_change(request, user_id)


@check_authorization
def show_transport_for_change(request, user_id):
    transport = Transport.objects.filter(user_id=user_id).all()
    context = {'property': transport,
               'title': 'Транспорт',
               'user_id': user_id,
               'change_property': 'change_transport',
               'add_property': 'add_transport',
               'menu': menu}
    return render(request, 'property_app/show_property.html', context=context)


@check_authorization
def add_transport(request, user_id):
    if request.method == 'POST':
        form = TransportForm(request.POST)
        if form.is_valid():
            transport = form.save(commit=False)
            transport.user_id = user_id
            transport.save()
            messages.success(request, "Создано транспортное средство")
            logger.info(f"Сохранение данных о транспортном средстве пользователя {user_id}")
            return redirect('show_transport', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных о транспортном средстве пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = TransportForm()
    context = {'form': form,
               'title': 'Новое транспортное средство',
               'add_property': 'add_transport',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'property_app/new_property.html', context=context)


@check_authorization
def change_transport(request, user_id, transport_id):
    current_transport = Transport.objects.filter(pk=transport_id).first()
    if request.method == 'POST':
        form = TransportForm(request.POST)
        if form.is_valid():
            data_by_form = form.cleaned_data
            current_transport.type_property = \
                data_by_form['type_property'] or current_transport.type_property
            current_transport.brand = \
                data_by_form['brand'] or current_transport.brand
            current_transport.model = \
                data_by_form['model'] or current_transport.model
            current_transport.year_release = \
                data_by_form['year_release'] or current_transport.year_release
            current_transport.registration_number = \
                data_by_form['registration_number'] or \
                    current_transport.registration_number
            current_transport.weigth = \
                data_by_form['weigth'] or current_transport.weigth
            current_transport.carrying = \
                data_by_form['carrying'] or current_transport.carrying
            current_transport.date_registration = \
                data_by_form['date_registration'] or current_transport.date_registration
            current_transport.description = \
                data_by_form['description'] or current_transport.description
            logger.info(f"Изменение данных о транспортном средстве {transport_id} \
пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('property', user_id=user_id)
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
def del_transport(request, user_id, transport_id):
    try:
        Transport.objects.filter(pk=transport_id).delete()
        logger.info(f"Удалены данные о транспортном средстве {transport_id} \
пользователя {user_id}")
        messages.success(request, "Данные успешно удалены")
    except:
        logger.debug(f"Ошибка удаления данных о транспортном средстве \
{transport_id} пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('edit_transport', user_id=user_id)