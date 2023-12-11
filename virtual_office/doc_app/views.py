import logging

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages

from abstract_app.views import documents, menu, check_authorization, check_doc, get_data_with_verbose_name

from .models import Children, DriverCategory, Passport, Inn, Snils, DriverLicense, MilitaryTicket, ForeignPassport, Spouce, People, DriverCategoryShedule
from .forms import PassportForm, InnForm, DriverLicenseForm, ForeignPassportForm, MilitaryTicketForm, SnilsForm, SpouceForm, ChildrenForm, DriverCategoryAddForm, DriverCategoryEditForm

from user_app.models import Data


logger = logging.getLogger(__name__)


def redirect_to_enter_doc(request: HttpResponse,
                          user_id: int,
                          doc: str,
                          func_name: str) -> HttpResponse:
    logger.debug(f"Документ {doc} пользователя {user_id} не создан - \
попытка ввода данных")
    messages.error(request, f'Для работы с данными документа {doc} \
необходимо его создать')
    return redirect(func_name, user_id=user_id)


def load_form_people(entity: People, data_by_form: type):
    entity.name = data_by_form['name'] or entity.name
    entity.surname = data_by_form['surname'] or entity.surname
    entity.patronymic = data_by_form['patronymic'] or entity.patronymic
    entity.birthday = data_by_form['birthday'] or entity.birthday
    entity.gender = data_by_form['gender'] or entity.gender
    entity.save()


@check_authorization
def docs(request, user_id):
    context = {'title': 'Документы',
               'user_id': user_id,
               'documents': documents,
               'menu': menu}
    return render(request, 'doc_app/docs.html', context=context)


def show_spouce(passport: Passport) -> dict:
    if passport and Spouce.objects.filter(pk=passport.pk):
        spouce = Spouce.objects.values('surname', 'name', 'patronymic',
                                       'birthday', 'gender',
                                       'date_marriage').filter(
            pk=passport.pk).first()
        object_spouce = get_object_or_404(Spouce, pk=passport.pk)
        return get_data_with_verbose_name(object_spouce, spouce)


def show_childrens(passport: Passport) -> list[dict]:
    if passport:
        childrens = Passport.objects.filter(
            pk=passport.pk).first().children_set.all()
        output_cilds = []
        for child in childrens:
            children = Children.objects.values('surname', 'name',
                                               'patronymic', 'birthday',
                                               'gender').filter(
                pk=child.pk).first()
            object_child = get_object_or_404(Children, pk=child.pk)
            output_cilds.append(
                get_data_with_verbose_name(object_child, children))
        return output_cilds


@check_authorization
def get_passport(request, user_id):
    if check_doc(user_id, Passport):
        data = Data.objects.values('surname', 'name', 'patronymic',
                                   'birthday', 'birth_place',
                                   'place_residense', 'gender').filter(
            user_id=user_id).first()
        passport = Passport.objects.values('series', 'number',
                                           'date_registration',
                                           'id_inspection',
                                           'name_inspection',
                                           'adress_registration',
                                           'date_adress_reg').filter(
            user_id=user_id).first()
        object_data = get_object_or_404(Data, user_id=user_id)
        object_passport = get_object_or_404(Passport, user_id=user_id)
        spouce = show_spouce(object_passport)
        childrens = show_childrens(object_passport)
        context = {**get_data_with_verbose_name(object_data, data),
                   **get_data_with_verbose_name(object_passport, passport),
                   }
        context_to_template = {'context': context,
                               'spouce': spouce,
                               'childrens': childrens,
                               'title': 'Данные пользователя',
                               'user_id': user_id,
                               'menu': menu}
        return render(request, 'doc_app/passport.html', context=context_to_template)
    logger.debug(f"Паспорт пользователя {user_id} не создан - \
попытка ввода данных о супруге")
    messages.error(request,
                   'Для работы с паспортом необходимо ввести паспортные данные')
    return redirect('change_passport', user_id=user_id)


@check_authorization
def change_passport(request, user_id):
    if request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            current_passport = Passport.objects.filter(
                user_id=user_id).first()
            if current_passport:
                data_by_form = form.cleaned_data
                current_passport.series = \
                    data_by_form['series'] or current_passport.series
                current_passport.number = \
                    data_by_form['number'] or current_passport.number
                current_passport.date_registration = \
                    data_by_form['date_registration'] \
                    or current_passport.date_registration
                current_passport.id_inspection = \
                    data_by_form['id_inspection'] \
                    or current_passport.id_inspection
                current_passport.name_inspection = \
                    data_by_form['name_inspection'] \
                    or current_passport.name_inspection
                current_passport.date_adress_reg = \
                    data_by_form['date_adress_reg'] \
                    or current_passport.date_adress_reg
                current_passport.adress_reg_eq_place = \
                    data_by_form['adress_reg_eq_place'] \
                    or current_passport.adress_reg_eq_place
                if current_passport.adress_reg_eq_place:
                    current_passport.adress_registration = \
                        Data.objects.filter(
                            user_id=user_id).first().place_residense
                else:
                    current_passport.adress_registration = \
                        data_by_form['adress_registration'] \
                        or current_passport.adress_registration
                current_passport.save()
            else:
                passport = form.save(commit=False)
                passport.user_id = user_id
                passport.save()
            messages.success(request, "Паспортные данные успешно изменены")
            logger.info(f"Сохранение паспортных данных пользователя {user_id}")
            return redirect('passport', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения паспортных данных пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = PassportForm()
    context = {'form': form,
               'title': 'Изменение паспортных данных',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/change_passport.html', context=context)


@check_authorization
def add_spouce(request, user_id):
    if request.method == 'POST':
        form = SpouceForm(request.POST)
        if form.is_valid():
            spouce = form.save(commit=False)
            if spouce.name or spouce.surname or \
                    spouce.patronymic or spouce.birthday or \
                    spouce.gender or spouce.date_marriage:
                spouce.passport_id = user_id
                spouce.save()
                Passport.objects.filter(
                    user_id=user_id).first().spouce = spouce
                logger.info(
                    f"Сохранение данных о супруге пользователя {user_id}")
                messages.success(request, "Данные о супруге добавлены")
                return redirect('passport', user_id=user_id)
            logger.debug(
                f"Ошибка сохранения данных о супруге пользователя {user_id}")
            messages.error(request, "Необходимо заполнить хотя бы одно поле")
    else:
        form = SpouceForm()
    context = {'form': form,
               'title': 'Данные о супруге',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/edit_spouce.html', context)


@check_authorization
def change_spouce(request, user_id):
    if request.method == 'POST':
        form = SpouceForm(request.POST)
        if form.is_valid():
            current_spouce = Spouce.objects.get(passport_id=user_id)
            data_by_form = form.cleaned_data
            load_form_people(current_spouce, data_by_form)
            current_spouce.date_marriage = data_by_form['date_marriage']\
                or current_spouce.date_marriage
            current_spouce.save()
            logger.info(f"Изменение данных о супруге пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('passport', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения паспортных данных пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = SpouceForm()
    context = {'form': form,
               'title': 'Данные о супруге',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/edit_spouce.html', context)


@check_authorization
def edit_spouce(request, user_id):
    if check_doc(user_id, Passport):
        if Spouce.objects.filter(passport_id=user_id).first():
            return change_spouce(request, user_id)
        return add_spouce(request, user_id)
    return redirect_to_enter_doc(request, user_id, 'Паспорт',
                                 change_passport.__name__)


@check_authorization
def del_spouce(request, user_id):
    try:
        Spouce.objects.filter(passport_id=user_id).delete()
        logger.info(f"Удалены данные о супруге пользователя {user_id}")
        messages.success(request, "Данные успешно удалены")
    except:
        logger.debug(
            f"Ошибка удаления данных о супруге пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('passport', user_id=user_id)


@check_authorization
def add_children(request, user_id):
    if request.method == 'POST':
        form = ChildrenForm(request.POST)
        if form.is_valid():
            children = form.save(commit=False)
            if children.name or children.surname or \
                    children.patronymic or children.birthday or children.gender:
                children.save()
                Passport.objects.filter(
                    user_id=user_id).first().children_set.add(children)
                logger.info(
                    f"Сохранение данных о детях пользователя {user_id}")
                messages.success(request, "Данные о детях добавлены")
                return redirect('show_children', user_id=user_id)
            logger.debug(
                f"Ошибка сохранения данных о детях пользователя {user_id}")
            messages.error(request, "Необходимо заполнить хотя бы одно поле")
    else:
        form = ChildrenForm()
    context = {'form': form,
               'title': 'Данные о детях',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/new_children.html', context)


@check_authorization
def change_children(request, user_id, children_id):
    current_children = Children.objects.filter(pk=children_id).first()
    if request.method == 'POST':
        form = ChildrenForm(request.POST)
        if form.is_valid():
            data_by_form = form.cleaned_data
            load_form_people(current_children, data_by_form)
            logger.info(f"Изменение данных о детях пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('show_children', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения паспортных данных пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = ChildrenForm()
    context = {'form': form,
               'title': 'Данные о детях',
               'user_id': user_id,
               'children': current_children,
               'menu': menu}
    return render(request, 'doc_app/edit_children.html', context)


@check_authorization
def show_childrens_for_change(request, user_id):
    childrens = Passport.objects.filter(pk=user_id).first().children_set.all()
    context = {'childrens': childrens,
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/show_children.html', context=context)


@check_authorization
def edit_children(request, user_id):
    if check_doc(user_id, Passport):
        if not Passport.objects.filter(pk=user_id).first().children_set.all():
            messages.error(request, "Данные о детях отсутствуют")
            return add_children(request, user_id)
        return show_childrens_for_change(request, user_id)
    return redirect_to_enter_doc(request, user_id, 'Паспорт',
                                 change_passport.__name__)


@check_authorization
def del_children(request, user_id, children_id):
    try:
        Children.objects.filter(pk=children_id).delete()
        logger.info(f"Удалены данные о ребенке пользователя {user_id}")
        messages.success(request, "Данные успешно удалены")
    except:
        logger.debug(
            f"Ошибка удаления данных о ребенке пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('passport', user_id=user_id)


@check_authorization
def get_inn(request, user_id):
    if check_doc(user_id, Inn):
        data = Data.objects.values('surname', 'name', 'patronymic',
                                   'birthday', 'birth_place',
                                   'gender').filter(
            user_id=user_id).first()
        inn = Inn.objects.values('inn', 'series', 'number',
                                 'date_registration',
                                 'id_inspection',
                                 'name_inspection').filter(
            user_id=user_id).first()
        object_data = get_object_or_404(Data, user_id=user_id)
        object_inn = get_object_or_404(Inn, user_id=user_id)
        context = {**get_data_with_verbose_name(object_data, data),
                   **get_data_with_verbose_name(object_inn, inn),
                   }
        context_to_template = {'context': context,
                               'title': 'ИНН',
                               'user_id': user_id,
                               'view': 'change_inn',
                               'menu': menu}
        return render(request, 'doc_app/base_doc.html', context=context_to_template)
    logger.debug(f"ИНН пользователя {user_id} не существует")
    messages.error(request,
                   'Для работы с ИНН необходимо ввести данные ФНС')
    return redirect('change_inn', user_id=user_id)


@check_authorization
def change_inn(request, user_id):
    if request.method == 'POST':
        form = InnForm(request.POST)
        if form.is_valid():
            current_inn = Inn.objects.filter(
                user_id=user_id).first()
            if current_inn:
                data_by_form = form.cleaned_data
                current_inn.series = \
                    data_by_form['series'] or current_inn.series
                current_inn.number = \
                    data_by_form['number'] or current_inn.number
                current_inn.date_registration = \
                    data_by_form['date_registration'] \
                    or current_inn.date_registration
                current_inn.id_inspection = \
                    data_by_form['id_inspection'] \
                    or current_inn.id_inspection
                current_inn.name_inspection = \
                    data_by_form['name_inspection'] \
                    or current_inn.name_inspection
                current_inn.inn = \
                    data_by_form['inn'] \
                    or current_inn.inn
                current_inn.save()
            else:
                inn = form.save(commit=False)
                inn.user_id = user_id
                inn.save()
            messages.success(request, "Данные ИНН успешно изменены")
            logger.info(f"Сохранение ИНН пользователя {user_id}")
            return redirect('inn', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения паспортных данных пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = InnForm()
    context = {'form': form,
               'title': 'Изменение данных ИНН',
               'view': 'change_inn',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/base_change_doc.html', context=context)


@check_authorization
def get_snils(request, user_id):
    if check_doc(user_id, Inn):
        data = Data.objects.values('surname', 'name', 'patronymic',
                                   'birthday', 'birth_place',
                                   'gender').filter(
            user_id=user_id).first()
        snils = Snils.objects.values('number',
                                     'date_registration',
                                     'id_inspection',
                                     'name_inspection').filter(
            user_id=user_id).first()
        object_data = get_object_or_404(Data, user_id=user_id)
        object_snils = get_object_or_404(Snils, user_id=user_id)
        context = {**get_data_with_verbose_name(object_data, data),
                   **get_data_with_verbose_name(object_snils, snils),
                   }
        context_to_template = {'context': context,
                               'title': 'CНИЛС',
                               'user_id': user_id,
                               'view': 'change_snils',
                               'menu': menu}
        return render(request, 'doc_app/base_doc.html', context=context_to_template)
    logger.debug(f"СНИЛС пользователя {user_id} не существует")
    messages.error(request,
                   'Для работы со СНИЛС необходимо ввести данные')
    return redirect('change_snils', user_id=user_id)


@check_authorization
def change_snils(request, user_id):
    if request.method == 'POST':
        form = SnilsForm(request.POST)
        if form.is_valid():
            current_inn = Snils.objects.filter(
                user_id=user_id).first()
            if current_inn:
                data_by_form = form.cleaned_data
                current_inn.number = \
                    data_by_form['number'] or current_inn.number
                current_inn.date_registration = \
                    data_by_form['date_registration'] \
                    or current_inn.date_registration
                current_inn.id_inspection = \
                    data_by_form['id_inspection'] \
                    or current_inn.id_inspection
                current_inn.name_inspection = \
                    data_by_form['name_inspection'] \
                    or current_inn.name_inspection
                current_inn.save()
            else:
                inn = form.save(commit=False)
                inn.user_id = user_id
                inn.save()
            messages.success(request, "Данные СНИЛС успешно изменены")
            logger.info(f"Сохранение СНИЛС пользователя {user_id}")
            return redirect('snils', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения паспортных данных пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = SnilsForm()
    context = {'form': form,
               'title': 'Изменение данных СНИЛС',
               'view': 'change_snils',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/base_change_doc.html', context=context)


@check_authorization
def add_driver_category(request, user_id):
    if request.method == 'POST':
        form = DriverCategoryAddForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.driver_license_id = user_id
            category.save()
            logger.info(
                f"Сохранение данных о водительской категории пользователя {user_id}")
            messages.success(request, "Данные о категории добавлены")
            return redirect('show_driver_categories', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных о категории {user_id}")
        messages.error(request, "Необходимо заполнить все поля")
    else:
        form = DriverCategoryAddForm()
    context = {'form': form,
               'title': 'Данные о категории',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/new_driver_category.html', context)


@check_authorization
def del_driver_category(request, user_id, category_id):
    try:
        DriverCategoryShedule.objects.filter(
            driver_license_id=user_id, category_id=category_id).delete()
        logger.info(f"Удалены данные о категории {category_id} пользователя {user_id}")
        messages.success(request, "Данные успешно удалены")
    except:
        logger.debug(f"Ошибка удаления данных о категории {category_id} пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect ('driver_license', user_id=user_id)


@check_authorization
def edit_driver_categories(request, user_id):
    if check_doc(user_id, DriverLicense):
        if not DriverLicense.objects.filter(pk=user_id).first().categories.all():
            messages.error(
                request, "Данные об открытых категориях отсутствуют")
            return change_driver_license(request, user_id)
        return show_categories_for_change(request, user_id)
    return redirect_to_enter_doc(request, user_id, 'Водительское удостоверение',
                                 change_driver_license.__name__)


@check_authorization
def change_driver_category(request, user_id, category_id):
    current_shedule_cat = DriverCategoryShedule.objects.filter(
        driver_license_id=user_id, category_id=category_id).first()
    if request.method == 'POST':
        form = DriverCategoryEditForm(request.POST)
        if form.is_valid():
            data_by_form = form.cleaned_data
            current_shedule_cat.date_begin = \
                data_by_form['date_begin'] or current_shedule_cat.date_begin
            current_shedule_cat.date_end = \
                data_by_form['date_end'] or current_shedule_cat.date_end
            current_shedule_cat.note = \
                data_by_form['note'] or current_shedule_cat.note
            current_shedule_cat.save()
            logger.info(
                f"Изменение данных о водительской категории {category_id} пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('show_driver_categories', user_id=user_id)
        logger.debug(f"Ошибка сохранения данных ВУ пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = DriverCategoryEditForm()
    context = {'form': form,
               'title':
               f'Данные о категории {DriverCategory.objects.filter(pk=category_id).first().name}',
               'user_id': user_id,
               'shedule_cat': current_shedule_cat,
               'menu': menu}
    return render(request, 'doc_app/edit_driver_cat.html', context)


@check_authorization
def show_categories_for_change(request, user_id):
    categories = DriverLicense.objects.filter(
        pk=user_id).first().categories.all().order_by('name')
    context = {'categories': categories,
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/show_driver_cat.html', context=context)


def show_driver_categories(driver_license: DriverLicense) -> list[dict]:
    if driver_license:
        categories = DriverCategoryShedule.objects.filter(
            driver_license_id=driver_license.pk).all()
        output_cats = []
        for cat in categories:
            category = DriverCategoryShedule.objects.values('category_id',
                                                            'date_begin',
                                                            'date_end',
                                                            'note').filter(
                                                                pk=cat.pk).first()
            object_category = get_object_or_404(DriverCategoryShedule, pk=cat.pk)
            temp = get_data_with_verbose_name(object_category, category)
            print(temp)
            temp['Категория'] = DriverCategory.objects.get(id=temp['Категория'])
            output_cats.append(temp)
        return output_cats
    

@check_authorization
def get_driver_license(request, user_id):
    if check_doc(user_id, DriverLicense):
        data = Data.objects.values('surname', 'name', 'patronymic',
                                   'birthday', 'birth_place', 'gender').filter(
            user_id=user_id).first()
        license = DriverLicense.objects.values('series', 'number',
                                               'date_registration',
                                               'id_inspection',
                                               'name_inspection',
                                               'date_end_action',
                                               'date_start_expirience',
                                               'special_marks',
                                               'categories').filter(
            user_id=user_id).first()
        object_data = get_object_or_404(Data, user_id=user_id)
        object_license = get_object_or_404(DriverLicense, user_id=user_id)
        context = {**get_data_with_verbose_name(object_data, data),
                   **get_data_with_verbose_name(object_license, license),
                   }
        categories = show_driver_categories(object_license)
        context_to_template = {'context': context,
                               'categories': categories,
                               'title': 'Водительское удостоверение',
                               'view': 'change_driver_license',
                               'user_id': user_id,
                               'menu': menu}
        return render(request, 'doc_app/driver_license.html', context=context_to_template)
    logger.debug(f"Водительское удостоверение пользователя {user_id} не создано - \
ВУ еще не создано")
    messages.error(request,
                   'Для работы с водительским удостоверением необходимо ввести данные')
    return redirect('change_driver_license', user_id=user_id)


@check_authorization
def change_driver_license(request, user_id):
    if request.method == 'POST':
        form = DriverLicenseForm(request.POST)
        if form.is_valid():
            current_license = DriverLicense.objects.filter(
                user_id=user_id).first()
            if current_license:
                data_by_form = form.cleaned_data
                current_license.series = \
                    data_by_form['series'] or current_license.series
                current_license.number = \
                    data_by_form['number'] or current_license.number
                current_license.date_registration = \
                    data_by_form['date_registration'] \
                    or current_license.date_registration
                current_license.id_inspection = \
                    data_by_form['id_inspection'] \
                    or current_license.id_inspection
                current_license.name_inspection = \
                    data_by_form['name_inspection'] \
                    or current_license.name_inspection
                current_license.date_end_action = \
                    data_by_form['date_end_action'] \
                    or current_license.date_end_action
                current_license.date_start_expirience = \
                    data_by_form['date_start_expirience'] \
                    or current_license.date_start_expirience
                current_license.special_marks = \
                    data_by_form['special_marks'] \
                    or current_license.special_marks
                categories = data_by_form['categories']
                if categories:
                    current_license.categories.set(categories)
            else:
                license = form.save(commit=False)
                license.user_id = user_id
                license.save()
                form.save_m2m()
            messages.success(request,
                             "Данные о водительском удостоверении успешно изменены")
            logger.info(f"Сохранение данных о ВУ пользователя {user_id}")
            return redirect('show_driver_categories', user_id=user_id)
        logger.debug(f"Ошибка сохранения данных о ВУ пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = DriverLicenseForm()
    context = {'form': form,
               'title': 'Изменение данных о водительском удостоверении',
               'view': 'change_driver_license',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/change_driver_license.html', context=context)


@check_authorization
def get_foreign_passport(request, user_id):
    if check_doc(user_id, ForeignPassport):
        data = Data.objects.values('surname', 'name', 'patronymic',
                                   'birthday', 'birth_place', 'gender').filter(
            user_id=user_id).first()
        foreign_pass = ForeignPassport.objects.values('series', 'number',
                                                      'date_registration',
                                                      'id_inspection',
                                                      'name_inspection',
                                                      'foreign_name',
                                                      'foreign_surname',
                                                      'date_end_action').filter(
            user_id=user_id).first()
        object_data = get_object_or_404(Data, user_id=user_id)
        object_foreign_pass = get_object_or_404(
            ForeignPassport, user_id=user_id)
        context = {**get_data_with_verbose_name(object_data, data),
                   **get_data_with_verbose_name(object_foreign_pass, foreign_pass),
                   }
        context_to_template = {'context': context,
                               'title': 'Заграничный паспорт',
                               'view': 'change_foreign_passport',
                               'user_id': user_id,
                               'menu': menu}
        return render(request, 'doc_app/base_doc.html', context=context_to_template)
    logger.debug(f"Заграничный паспорт пользователя {user_id} не создан - \
ошибка ввода данных")
    messages.error(request,
                   'Для работы с заграничным паспортом необходимо ввести данные')
    return redirect('change_foreign_passport', user_id=user_id)


@check_authorization
def change_foreign_passport(request, user_id):
    if request.method == 'POST':
        form = ForeignPassportForm(request.POST)
        if form.is_valid():
            current_foreign_pass = ForeignPassport.objects.filter(
                user_id=user_id).first()
            if current_foreign_pass:
                data_by_form = form.cleaned_data
                current_foreign_pass.series = \
                    data_by_form['series'] or current_foreign_pass.series
                current_foreign_pass.number = \
                    data_by_form['number'] or current_foreign_pass.number
                current_foreign_pass.date_registration = \
                    data_by_form['date_registration'] \
                    or current_foreign_pass.date_registration
                current_foreign_pass.id_inspection = \
                    data_by_form['id_inspection'] \
                    or current_foreign_pass.id_inspection
                current_foreign_pass.name_inspection = \
                    data_by_form['name_inspection'] \
                    or current_foreign_pass.name_inspection
                current_foreign_pass.date_end_action = \
                    data_by_form['date_end_action'] \
                    or current_foreign_pass.date_end_action
                current_foreign_pass.foreign_name = \
                    data_by_form['foreign_name'] \
                    or current_foreign_pass.foreign_name
                current_foreign_pass.foreign_surname = \
                    data_by_form['foreign_surname'] \
                    or current_foreign_pass.foreign_surname
                current_foreign_pass.save()
            else:
                foreign_pass = form.save(commit=False)
                foreign_pass.user_id = user_id
                foreign_pass.save()
            messages.success(request,
                             "Данные о заграничном паспорте успешно изменены")
            logger.info(
                f"Сохранение данных о загранпаспорте пользователя {user_id}")
            return redirect('foreign_passport', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных о загранпаспорте пользователя {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = ForeignPassportForm()
    context = {'form': form,
               'title': 'Изменение данных о загарничном паспорте',
               'view': 'change_foreign_passport',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/base_change_doc.html', context=context)


@check_authorization
def get_military_ticket(request, user_id):
    if check_doc(user_id, MilitaryTicket):
        data = Data.objects.values('surname', 'name', 'patronymic',
                                   'birthday', 'birth_place', 'gender').filter(
            user_id=user_id).first()
        military_ticket = MilitaryTicket.objects.values('series', 'number',
                                                        'date_registration',
                                                        'id_inspection',
                                                        'name_inspection',
                                                        'category',
                                                        'speciality',
                                                        'description').filter(
            user_id=user_id).first()
        object_data = get_object_or_404(Data, user_id=user_id)
        object_ticket = get_object_or_404(MilitaryTicket, user_id=user_id)
        context = {**get_data_with_verbose_name(object_data, data),
                   **get_data_with_verbose_name(object_ticket, military_ticket),
                   }
        context_to_template = {'context': context,
                               'title': 'Военыый билет',
                               'view': 'change_military_ticket',
                               'user_id': user_id,
                               'menu': menu}
        return render(request, 'doc_app/base_doc.html', context=context_to_template)
    logger.debug(f"Военный билет пользователя {user_id} не создан - \
ошибка ввода данных")
    messages.error(request,
                   'Для работы с военным билетом необходимо ввести данные')
    return redirect('change_military_ticket', user_id=user_id)


@check_authorization
def change_military_ticket(request, user_id):
    if request.method == 'POST':
        form = MilitaryTicketForm(request.POST)
        if form.is_valid():
            current_ticket = MilitaryTicket.objects.filter(
                user_id=user_id).first()
            if current_ticket:
                data_by_form = form.cleaned_data
                current_ticket.series = \
                    data_by_form['series'] or current_ticket.series
                current_ticket.number = \
                    data_by_form['number'] or current_ticket.number
                current_ticket.date_registration = \
                    data_by_form['date_registration'] \
                    or current_ticket.date_registration
                current_ticket.id_inspection = \
                    data_by_form['id_inspection'] \
                    or current_ticket.id_inspection
                current_ticket.name_inspection = \
                    data_by_form['name_inspection'] \
                    or current_ticket.name_inspection
                current_ticket.category = \
                    data_by_form['category'] \
                    or current_ticket.category
                current_ticket.speciality = \
                    data_by_form['speciality'] \
                    or current_ticket.speciality
                current_ticket.description = \
                    data_by_form['description'] \
                    or current_ticket.description
                current_ticket.save()
            else:
                ticket = form.save(commit=False)
                ticket.user_id = user_id
                ticket.save()
            messages.success(request,
                             "Данные о военном билете успешно изменены")
            logger.info(f"Сохранение данных о военном билете {user_id}")
            return redirect('military_ticket', user_id=user_id)
        logger.debug(f"Ошибка сохранения данных о военном билете {user_id}")
        messages.error(request, "Неверные данные")
    else:
        form = MilitaryTicketForm()
    context = {'form': form,
               'title': 'Изменение данных о военном билете',
               'view': 'change_military_ticket',
               'user_id': user_id,
               'menu': menu}
    return render(request, 'doc_app/base_change_doc.html', context=context)