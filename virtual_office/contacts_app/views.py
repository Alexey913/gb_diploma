import logging
from django import forms

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages

from abstract_app.views import properties, menu, check_authorization, check_doc, get_data_with_verbose_name

from .models import Contact, Phone, Email
from .forms import ContactForm, PhoneForm, EmailForm
from user_app.models import Data


logger = logging.getLogger(__name__)


@check_authorization
def get_contacts(request, user_id):
    contacts = Contact.objects.filter(user_id=user_id).all()
    context = {'title': 'Контакты',
               'user_id': user_id,
               'contacts': contacts,
               'menu': menu}
    return render(request, 'contacts_app/contacts.html', context=context)


@check_authorization
def show_contact(request, user_id, contact_id):
    object_contact = get_object_or_404(Contact, pk=contact_id)
    contact = Contact.objects.values('surname', 'name', 'patronymic',
                                     'organization', 'birthday',
                                     'place_residense').filter(
                                         pk=contact_id).first()
    output_contact = get_data_with_verbose_name(object_contact, contact)
    phones = Phone.objects.filter(contact_id=contact_id).all()
    emails = Email.objects.filter(contact_id=contact_id).all()
    title = f'Контакт: {output_contact}'
    context = {'title': title,
               'user_id': user_id,
               'contact_id': contact_id,
               'contact': output_contact,
               'phones': phones,
               'emails': emails,
               'menu': menu}
    return render(request, 'contacts_app/show_contact.html', context=context)


@check_authorization
def add_contact(request, user_id):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        phone_form = PhoneForm(request.POST)
        email_form = EmailForm(request.POST)
        if contact_form.is_valid() and phone_form.is_valid() and email_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.user_id = user_id
            contact.save()
            if phone_form.has_changed():
                phone = phone_form.save(commit=False)
                phone.contact_id = contact.id
                phone.save()
            if email_form.has_changed():
                email = email_form.save(commit=False)
                email.contact_id = contact.id
                email.save()
            messages.success(request, "Контакт успешно создан")
            logger.info(f"Сохранение данных контакта {contact} пользователя {user_id}")
            return redirect('contacts', user_id=user_id)
        logger.debug(
            f"Ошибка сохранения данных контакта для пользователя {user_id}")
        messages.error(request, "Необходимо указать имя или фамилию")
    else:
        contact_form = ContactForm()
        phone_form = PhoneForm()
        email_form = EmailForm()
    context = {'form': contact_form,
               'phone_form': phone_form,
               'email_form': email_form,
               'title': 'Новый контакт',
               'user_id': user_id,
               'view': 'add_contact',
               'menu': menu}
    return render(request, 'contacts_app/new_contact.html', context=context)


@check_authorization
def add_phone(request, user_id, contact_id):
    if request.method == 'POST':
        phone_form = PhoneForm(request.POST)
        if phone_form.is_valid() and phone_form.has_changed():
            if not Phone.objects.filter(phone=phone_form.cleaned_data['phone'],
                                    contact_id=contact_id).first():
                phone = phone_form.save(commit=False)
                phone.contact_id = contact_id
                phone.save()
                messages.success(request, "Номер телефона добавлен")
                logger.info(f"Сохранение данных контакта {contact_id} \
пользователя {user_id}")
                return redirect('show_contact', user_id=user_id, contact_id=contact_id)
            else:
                logger.debug(f"Ошибка сохранения данных контакта пользователя {user_id}")
                messages.error(request, "Телефон пользователя уже существует")
        else:
            logger.debug(
                f"Ошибка сохранения данных контакта пользователя {user_id}")
            messages.error(request, "Необходимо ввести номер телефона")
    else:
        phone_form = PhoneForm()
    context = {'form': phone_form,
               'title': f'Контакт {contact_id}',
               'user_id': user_id,
               'contact_id': contact_id,
               'view': 'add_phone',
               'menu': menu}
    return render(request, 'contacts_app/edit_contact.html', context=context)


@check_authorization
def add_email(request, user_id, contact_id):
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid() and email_form.has_changed():
            if not Email.objects.filter(email=email_form.cleaned_data['email'],
                                        contact_id=contact_id).first():
                email = email_form.save(commit=False)
                email.contact_id = contact_id
                email.save()
                messages.success(request, "E-mail добавлен")
                logger.info(f"Сохранение данных контакта {contact_id} \
пользователя {user_id}")
                return redirect('show_contact', user_id=user_id, contact_id=contact_id)
            else:
                logger.debug(f"Ошибка сохранения данных контакта пользователя \
{user_id} - дублирование e-mail")
                messages.error(request, "E-mail пользователя уже существует")
        else:
            logger.debug(f"Ошибка сохранения данных контакта пользователя {user_id}")
            messages.error(request, "Необходимо ввести e-mail")
    else:
        email_form = EmailForm()
    context = {'form': email_form,
               'title': f'Контакт {contact_id}',
               'user_id': user_id,
               'contact_id': contact_id,
               'view': 'add_email',
               'menu': menu}
    return render(request, 'contacts_app/edit_contact.html', context=context)


@check_authorization
def change_email(request, user_id, contact_id, email_id):
    current_email = Email.objects.filter(pk=email_id)
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid() and email_form.has_changed():
            input_email = email_form.cleaned_data['email']
            if not Email.objects.filter(email=input_email,
                                        contact_id=contact_id).first():
                current_email.email = input_email
                current_email.save()
                messages.success(request, "E-mail изменен")
                logger.info(f"Сохранение данных контакта {contact_id} \
пользователя {user_id}")
                return redirect('show_contact', user_id=user_id, contact_id=contact_id)
            else:
                logger.debug(f"Ошибка сохранения данных контакта пользователя \
{user_id} - дублирование e-mail")
                messages.error(request, "E-mail пользователя уже существует")
        else:
            logger.debug(f"Ошибка сохранения данных контакта пользователя {user_id}")
            messages.error(request, "Необходимо ввести e-mail")
    else:
        email_form = EmailForm()
    context = {'form': email_form,
               'title': f'E-mail {email_id}',
               'user_id': user_id,
               'contact_id': contact_id,
               'change_pk': email_id,
               'change_note': 'change_email',
               'note': 'e-mail',
               'del_note': 'del_email',
               'menu': menu}
    return render(request, 'contacts_app/edit_contact_data.html', context=context)


@check_authorization
def change_phone(request, user_id, contact_id, phone_id):
    current_phone = Phone.objects.filter(pk=phone_id)
    if request.method == 'POST':
        phone_form = PhoneForm(request.POST)
        if phone_form.is_valid() and phone_form.has_changed():
            input_phone = phone_form.cleaned_data['phone']
            if not Phone.objects.filter(phone=input_phone,
                                        contact_id=contact_id).first():
                current_phone.phone = input_phone
                current_phone.save()
                messages.success(request, "Номер изменен")
                logger.info(f"Сохранение данных контакта {contact_id} \
пользователя {user_id}")
                return redirect('show_contact', user_id=user_id, contact_id=contact_id)
            else:
                logger.debug(f"Ошибка сохранения данных контакта пользователя \
{user_id} - дублирование телефона")
                messages.error(request, "E-mail пользователя уже существует")
        else:
            logger.debug(f"Ошибка сохранения данных контакта пользователя {user_id}")
            messages.error(request, "Необходимо ввести номер телефона")
    else:
        phone_form = PhoneForm()
    context = {'form': phone_form,
               'title': f'Телефон {phone_id}',
               'user_id': user_id,
               'contact_id': contact_id,
               'change_pk': phone_id,
               'change_note': 'change_phone',
               'note': 'телефон',
               'del_note': 'del_phone',
               'menu': menu}
    return render(request, 'contacts_app/edit_contact_data.html', context=context)


@check_authorization
def del_email(request, user_id, contact_id, email_id):
    try:
        Email.objects.filter(pk=email_id).delete()
        logger.info(f"Удален e-mail {email_id} контакта {contact_id} \
пользователя {user_id}")
        messages.success(request, "Данные контакта успешно удалены")
    except:
        logger.debug(f"Ошибка удаления e-mail {email_id} контакта {contact_id} \
пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('show_contact', user_id=user_id, contact_id=contact_id)


@check_authorization
def del_phone(request, user_id, contact_id, phone_id):
    try:
        Phone.objects.filter(pk=phone_id).delete()
        logger.info(f"Удален телефон {phone_id} контакта {contact_id} \
пользователя {user_id}")
        messages.success(request, "Данные контакта успешно удалены")
    except:
        logger.debug(f"Ошибка удаления телефона {phone_id} контакта {contact_id} \
пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('show_contact', user_id=user_id, contact_id=contact_id)


@check_authorization
def change_contact(request, user_id, contact_id):
    current_contact = Contact.objects.filter(pk=contact_id).first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data_by_form = form.cleaned_data
            current_contact.surname = \
                data_by_form['surname'] or current_contact.surname
            current_contact.name = \
                data_by_form['name'] or current_contact.name
            current_contact.patronymic = \
                data_by_form['patronymic'] or current_contact.patronymic
            current_contact.organization = \
                data_by_form['organization'] or current_contact.organization
            current_contact.birthday = \
                data_by_form['birthday'] or current_contact.birthday
            current_contact.place_residense = \
                data_by_form['place_residense'] or current_contact.place_residense
            current_contact.save()
            logger.info(f"Изменение данных о контакте {contact_id} \
пользователя {user_id}")
            messages.success(request, "Данные успешно изменены")
            return redirect('show_contact', user_id=user_id, contact_id=contact_id)
        logger.debug(
            f"Ошибка сохранения данных контакта {contact_id} пользователя {user_id}")
        messages.error(request, "Необходимо ввести имя или фамилию")
    else:
        form = ContactForm()
    context = {'form': form,
               'title': 'Изменение данных контакта',
               'user_id': user_id,
               'contact': current_contact,
               'contact_id': current_contact.pk,
               'change_pk': 0,
               'view': 'change_contact',
               'menu': menu}
    return render(request, 'contacts_app/edit_contact.html', context)


@check_authorization
def del_contact(request, user_id, contact_id):
    try:
        Contact.objects.filter(pk=contact_id).delete()
        logger.info(f"Удалены данные контакта {contact_id} пользователя {user_id}")
        messages.success(request, "Данные контакта успешно удалены")
    except:
        logger.debug(
            f"Ошибка удаления данных контакта {contact_id} пользователя {user_id}")
        messages.error(request, "Данных не сущствует")
    finally:
        return redirect('contacts', user_id=user_id)