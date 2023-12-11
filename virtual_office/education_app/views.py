import logging
from typing import Callable

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages

from abstract_app.views import  menu, check_authorization, check_doc, get_data_with_verbose_name

from .models import Diploma
from .forms import DiplomaForm


logger = logging.getLogger(__name__)



def show_diplomas(user_id: int) -> HttpResponse:
    diplomas = Diploma.objects.filter(user_id=user_id).all()
    if diplomas:
        output_diplomas = []
        for dip in output_diplomas:
            diplom = Diploma.objects.values('name','number', 'series',
                                             'date_registration',
                                             'registration_number',
                                             'name_institution',
                                             'year_of_start_edu',
                                             'year_of_finish_edu',
                                             'spiciality', 'spicialization',
                                             'description').filter(
                                                 pk=dip.pk).first()
            object_diplom = get_object_or_404(Diploma, pk=dip.pk)
            output_diplomas.append(
                get_data_with_verbose_name(object_diplom, diplom))
        return output_diplomas



@check_authorization
def education(request: HttpResponse, user_id: int) -> HttpResponse:
    diplomas = show_diplomas(user_id)
    if diplomas:
        context = {'diplomas': diplomas,
                               'title': 'Данные об образовании',
                               'user_id': user_id,
                               'menu': menu}
        return render(request, 'eduction_app/show_diplomas.html', context=context)
    return redirect('edit_diploma', user_id=user_id)


@check_authorization
def edit_diploma(request: HttpResponse, user_id: int) -> Callable:
    if not check_doc(user_id, Diploma):
        logger.debug(f"Нет данных об образовании пользователя {user_id} - \
переход к заполнению данных")
        messages.error(request,
        'Нет сведений об образовании пользователя. Введите необходимые данные')
        return add_diploma(request, user_id)
    return show_diplomas_for_change(request, user_id)


@check_authorization
def show_diplomas_for_change(request: HttpResponse, user_id: int) -> HttpResponse:
    diplomas = Diploma.objects.filter(user_id=user_id).all()
    context = {'diplomas': diplomas,
               'user_id': user_id,
               'menu': menu}
    return render(request, 'education_app/show_diplomas.html', context=context)


@check_authorization
def add_diploma(request: HttpResponse, user_id: int) -> HttpResponse:
    if request.method == 'POST':
        form = DiplomaForm(request.POST)
        if form.is_valid():
            diploma = form.save(commit=False)
            diploma.user_id = user_id
            diploma.save()
            messages.success(request, "Документ об образовании создан")
            logger.info(f"Сохранение данных об образовании пользователя {user_id}")
            return redirect('education', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных об образовательном документе пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = DiplomaForm()
    context = {'form': form,
               'title': 'Документ об образовании',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'education_app/new_diploma.html', context=context)


@check_authorization
def change_diploma(request: HttpResponse, user_id: int, diploma_id: int) -> HttpResponse:
    current_diploma = Diploma.objects.filter(pk=diploma_id).first()
    if request.method == 'POST':
        form = DiplomaForm(request.POST)
        if form.is_valid():
            data_by_form = form.cleaned_data
            current_diploma.name = \
                data_by_form['name'] or current_diploma.name
            current_diploma.series = \
                data_by_form['series'] or current_diploma.series
            current_diploma.number = \
                data_by_form['number'] or current_diploma.number
            current_diploma.date_registration = \
                data_by_form['date_registration'] or current_diploma.date_registration
            current_diploma.registration_number = \
                data_by_form['registration_number'] or current_diploma.registration_number
            current_diploma.name_institution = \
                data_by_form['name_institution'] or current_diploma.name_institution
            current_diploma.year_of_start_edu = \
                data_by_form['year_of_start_edu'] or current_diploma.year_of_start_edu
            current_diploma.year_of_finish_edu = \
                data_by_form['year_of_finish_edu'] or current_diploma.year_of_finish_edu
            current_diploma.spiciality = \
                data_by_form['spiciality'] or current_diploma.spiciality
            current_diploma.spicialization = \
                data_by_form['spicialization'] or current_diploma.spicialization
            current_diploma.description = \
                data_by_form['description'] or current_diploma.description
            logger.info(f"Изменение данных о дипломе {diploma_id} пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('education', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных диплома {diploma_id} пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = DiplomaForm()
    context = {'form': form,
               'title': 'Изменение данных об образовании',
               'user_id': user_id,
               'diploma': current_diploma,
               'menu': menu}
    return render(request, 'education_app/edit_diploma.html', context)


@check_authorization
def del_diploma(request: HttpResponse, user_id: int, diploma_id: int) -> HttpResponse:
    try:
        Diploma.objects.filter(pk=diploma_id).delete()
        logger.info(f"Удалены данные об образовательном документе {diploma_id} {user_id}")
        messages.success(request, "Данные успешно удалены")
    except:
        logger.debug(
            f"Ошибка удаления данных об образовательном документе {diploma_id} {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('education', user_id=user_id)
