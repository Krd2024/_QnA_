from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, OuterRef, Subquery
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from main.serializator import ItemSerializer
from rest_framework import generics
from bs4 import BeautifulSoup
import requests
import uuid
import math
import time
import os

from .forms import ProfileEditForm
import main.settings
from main.models import (
    Notification,
    Question,
    Answer,
    Rection,
    Subscription,
    Teg,
    User,
)


# =================================================================


class ItemList(generics.ListCreateAPIView):
    queryset = Question.objects.all()[:10]
    serializer_class = ItemSerializer
    print(serializer_class, "< ------------- serializer class")


# class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer


# def redirect_to_home(request, exception=None):
#     print("Redirecting to")
#     redirect("index")


def add_tag(request):
    print("tag add")
    try:
        tag_id = request.GET.get("tag_id")
        subscr = Subscription.objects.filter(tag=tag_id, user=request.user)
        tag_obj = Teg.objects.filter(id=tag_id)[0]
        if not subscr.exists():
            Subscription.objects.create(user=request.user, tag=tag_obj)
            return JsonResponse({"success": True, "answer": 1})
        else:
            Subscription.objects.filter(user=request.user, tag=tag_obj).delete()
            return JsonResponse({"success": True, "answer": -1})
    except Exception as e:
        print(e)
    return redirect("tegs")


# =================================================================
def questions_in_tag(request, **kwargs):
    """Показать вопросы по тегу"""

    page = kwargs.get("num_pages")

    print(kwargs)

    try:
        if page is not None:
            try:
                page = int(page)
                if page < 1:
                    raise ValueError()
            except Exception as e:
                print(e)
                return redirect("tegs")
        else:
            page = 1

        print(page, "< -- page")

        answers = (
            Answer.objects.all()
            .values("question_id")
            .annotate(total=Count("question_id"))
        )

        tag_obj = Teg.objects.get(name=kwargs.get("tags"))
        # all_question = Question.tegs_set.filter(tags=tag_obj)
        all_question = Question.objects.select_related("tegs").filter(tegs=tag_obj)

        num_pages = int(
            math.ceil(len(all_question) / main.settings.LIMIT_OF_USERS_ON_PAGE)
        )

        users_per_page = main.settings.LIMIT_OF_USERS_ON_PAGE
        paginator = Paginator(all_question, users_per_page)  # Создаем пагинатор

        try:
            sorted_question = paginator.page(page)
        except PageNotAnInteger:
            sorted_question = paginator.page(1)
        except EmptyPage:
            sorted_question = paginator.page(paginator.num_pages)

        # print(len(sorted_question))

        context = {
            "page_number": page,
            "pages_range": range(1, num_pages + 1),
            "all_question": sorted_question,
            "answers": answers,
            "tags": kwargs.get("tags"),
        }

        return render(request, "questions_tags.html", context)
        # for user in sorted_question:
        #     print(user.autor, user.tegs)

    except Exception as e:
        print(e, "< ----- def questions_in_tag(): ")
        return redirect("tegs")

    #
    #


def tegs(request):
    """Показать все теги"""
    # autor = User.objects.get(id=random.randint(50, 1629))
    # print(autor)
    start_time_0 = time.perf_counter_ns()
    try:
        tegs = {}
        tegs_obj = Teg.objects.prefetch_related("tegs_set").all()

        for teg in tegs_obj:
            # tag_dict = teg.tag_subscription
            # print(f"Название тега: {teg.name}")
            quest = teg.tegs_set.all()
            questions = []
            for related in quest:
                questions.append(related.text)
                # print(f"Вопросы связанные с тегом: {related.text}")
            tegs[teg.name] = questions
        end_time_0 = time.perf_counter_ns()

        execution_time_ns = end_time_0 - start_time_0
        execution_time_s = execution_time_ns / 1_000_000_000
        print(f"Время выполнения Тег-вопросы: {execution_time_s:.4f} секунд")

        #  ==================  Подписки =============================================
        start_time_1 = time.perf_counter_ns()

        data = Subscription.objects.select_related("user", "tag").all()

        tag_dict = {}

        for entry in data:

            user = entry.user
            tag = entry.tag
            # Если тег еще не существует в словаре, создаем для него пустой список
            if tag not in tag_dict:
                tag_dict[tag] = []

            #     # Добавляем пользователя в список значений соответствующего тега
            tag_dict[tag].append(user)

        end_time_1 = time.perf_counter_ns()

        execution_time_ns = end_time_1 - start_time_1
        execution_time_s = execution_time_ns / 1_000_000_000
        print(f"Время выполнения  Тег-подписчики: {execution_time_s:.4f} секунд")

        #  ==========================================================================
        return render(
            request,
            "all_tegs.html",
            {"tegs": tegs, "tag_dict": tag_dict},
        )

    except Exception as e:
        print(e, "< ------------ def tegs(request)")
    return redirect("index")


def pars_up(request, **kwargs):
    print(kwargs)
    try:
        if kwargs.get("value") == "samoe":

            url = "http://qna.habr.com/"
            page = requests.get(url)
            if page.status_code != 200:
                return False
            soup = BeautifulSoup(page.text, "html.parser")
            allNews = soup.findAll("li", class_="content-list__item")
            links = {}
            for news_item in allNews:
                link = news_item.find(
                    "a", class_="question__title-link question__title_thin"
                )
                if link:
                    text = " ".join(link.text.split()).strip()
                    links[text] = link["href"]
            # return render(request, "wrapper/right_pars.html", {"links": links})

        elif kwargs.get("value") == "it":
            url = "http://habr.com/ru/news/"
            page = requests.get(url)
            if page.status_code != 200:

                return False
            soup = BeautifulSoup(page.text, "html.parser")
            allNewsIt = soup.findAll("article", class_="tm-articles-list__item")
            links = {}

            for news_item in allNewsIt:
                h2 = news_item.find("h2", class_="tm-title tm-title_h2")
                a = news_item.find("a", class_="tm-title__link")

                url = a["href"]
                link = f"HTTPS://habr.com{url}"
                text = h2.text
                links[text] = link
        return render(request, "wrapper/right_pars.html", {"links": links})

    except Exception as e:
        print(e)
        return redirect("index")

    # return render(request, "wrapper/right_pars.html", {"links": links})


# =================================================================


def edit_profile(request, **kwargs):
    """Обновить/добавить в ЛК"""

    if request.method == "POST":
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            form.save(commit=False)

            first = form.cleaned_data["first_name"]
            last = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            pro = form.cleaned_data["profession"]

            edit_user = User.objects.get(pk=request.user.id)
            if first != "":
                edit_user.first_name = first
            if last != "":
                edit_user.last_name = last
            if email != "":
                edit_user.email = email
            if pro != "":
                edit_user.profession = pro
            edit_user.save()

            return redirect("user_profile", request.user.username)
            # return HttpResponse(1)

        print()
    form = ProfileEditForm

    return render(request, "editProfile.html", {"form": form})


# =================================================================
#                 НЕ ИСПОЛЬЗУЕТСЯ


def generate_filename(instance, filename):
    # Получить расширение файла
    extension = os.path.splitext(filename)[1]
    # Генерировать уникальное имя файла с помощью uuid
    new_filename = str(uuid.uuid4()) + extension
    # Вернуть путь для сохранения файла
    return os.path.join("static", "profile", "picture", new_filename)


def all_users(request, **kwargs):
    """Показать всех пользователей"""

    start_time_0 = time.perf_counter_ns()
    try:
        question_count_subquery = (
            Question.objects.filter(autor=OuterRef("pk"))
            .values("autor")
            .annotate(count=Count("*"))
            .values("count")
        )
        answer_count_subquery = (
            Answer.objects.filter(autor=OuterRef("pk"))
            .values("autor")
            .annotate(count=Count("*"))
            .values("count")
        )

        users_obj_count = User.objects.annotate(
            question_count=Subquery(question_count_subquery),
            answer_count=Subquery(answer_count_subquery),
        )
    except Exception as e:
        print(e, "< --------- all users")

    end_time_0 = time.perf_counter_ns()

    execution_time_ns = end_time_0 - start_time_0
    execution_time_s = execution_time_ns / 1_000_000_000
    print(f"Время выполнения запроса к базе: {execution_time_s:.4f} секунд")

    # users_obj_count = User.objects.annotate(
    #     question_count=Count("question_set"), answer_count=Count("answer_set")
    # )

    # for user in users_obj_count:
    #     print(user.answer_count, " ", user.question_count)

    page = kwargs.get("page")

    if page is not None:
        try:
            page = int(page)
            if page < 2:
                raise ValueError()
        except Exception as e:
            print(e)
            return redirect("all_users")
    else:
        page = 1

    start_time_1 = time.perf_counter_ns()

    users_per_page = (
        main.settings.LIMIT_OF_USERS_ON_PAGE
    )  # Ограничение пользователей на странице

    # Сортировка и пагинация с использованием ORM
    users_obj_pag = User.objects.order_by(
        "-rating_cache"
    )  # Сортируем по рейтингу по убыванию
    paginator = Paginator(users_obj_pag, users_per_page)  # Создаем пагинатор

    users_obj = User.objects.all()
    num_pages = int(math.ceil(len(users_obj) / main.settings.LIMIT_OF_USERS_ON_PAGE))

    if num_pages <= 15:
        start = 1
        end = num_pages + 1
    else:
        start = max(1, page - 5)
        end = min(page + 5, num_pages + 1)

        # Корректировка диапазона, если он выходит за пределы допустимых значений
        if end - start < 10:
            if start == 1:
                end = 11
            elif end == num_pages + 1:
                end = num_pages - 9
    if page > 5:
        page_range = range(page - 5, min(page + 5, paginator.num_pages + 1))
    else:
        page_range = range(1, min(page + 10, paginator.num_pages + 1))

    try:
        sorted_users = paginator.page(page)
    except PageNotAnInteger:
        sorted_users = paginator.page(1)
    except EmptyPage:
        sorted_users = paginator.page(paginator.num_pages)

    # sorted_users = sorted(users_obj, key=lambda u: u.rating, reverse=True)
    # sorted_users = sorted_users[
    #     (page - 1)
    #     * main.settings.LIMIT_OF_USERS_ON_PAGE : (page)
    #     * main.settings.LIMIT_OF_USERS_ON_PAGE

    end_time_1 = time.perf_counter_ns()
    execution_time_ns_1 = end_time_1 - start_time_1
    total_time_ms_1 = execution_time_ns_1 / 1_000_000_000
    print(
        f"Время выполнения сортировки страниц в представлении: {total_time_ms_1:.4f} seconds"
    )

    start_time = time.time()

    response = render(
        request,
        "all_users.html",
        {
            "users": sorted_users,
            "pages_range": page_range,
            # "pages_range": range(1, num_pages + 1),
            "page_number": page,
            # "count_answer_users": count_answer_users,
            # "count_questions_users": count_questions_users,
            "users_obj_count": users_obj_count,
        },
    )
    end_time = time.time()
    total_time = end_time - start_time
    total_time_ms = total_time / 1_000_000_000
    print(f"Template render time: {total_time_ms:.4f} seconds")

    return response


def rating(request):
    text = """ Как увеличивается вклад пользователя
            Его ответ принят как решение: +10 очков
            Его ответ нравится: +3 очка """
    return HttpResponse(text)


def correct(request, **kwargs):
    """Поставить отметку ответу 'корректный'"""

    if not request.user.is_authenticated:
        return HttpResponse()
    if request.method == "POST":
        answer_id = kwargs["answer_id"]
        answer_obj = Answer.objects.get(id=answer_id)
        if (
            request.user != answer_obj.question.autor
            or answer_obj.autor == request.user
        ):
            return HttpResponse()

        new_correct = Answer.objects.get(id=answer_id)
        new_correct.correct = True
        new_correct.save()

    return JsonResponse({"success": True, "a": "good-answer"})


# ======================================================
def type_(search):
    """Без особого смысла"""

    def wrapper(*args, **kwargs):
        res1 = search(*args, **kwargs)
        if not isinstance(res1, (int)):
            return res1
        return 0

    return wrapper


# ======================================================


# @type_
def search(request, **kwargs):
    """Поиск по слову в вопросе"""

    print(kwargs["search"])

    try:
        search = kwargs["search"]
        # print(search, "<<<<<<<<<<<<<<<<<<<<<<")
        question = Question.objects.all()
        title_question = {}

        for title in question:
            title_question[title.id] = title.title.split(" ")

        for key, val in title_question.items():
            if search in val:
                sentence = " ".join(val)
                print(sentence)
                return HttpResponse(key)
        return HttpResponse()

    except Exception as e:
        print(e, "<<<< ------------- E --- def search()")
    return render(request, "question.html")


def increase_counter(request, **kwargs):
    """Поставить,убрать like"""

    print("пришло - 1")
    if not request.user.is_authenticated:
        return HttpResponse()
    answer_id = kwargs.get("answer_id")

    if request.method == "POST":
        try:
            answer = Answer.objects.get(id=answer_id)

            proverka = Rection.objects.filter(answer=answer, user=request.user)
            # proverka = Rection.objects.filter(answer=answer, user=answer.autor)
            if proverka.exists():
                proverka.delete()
                reac_count = answer.rection_set.count()
                # удалить уведомление
                # print(request.user)
                # print(answer.autor)
                # print(answer.id)

                x = Notification.objects.filter(
                    sender=request.user,
                    recipient=answer.autor,
                    notification_type="like",
                    # related_object_id=answer.id,
                    related_object_id=answer.question.id,
                ).delete()
                print(x)
                # Notification.objects.get(id=notification_id).delete()
                return JsonResponse({"success": True, "answer": reac_count})

            elif request.user == answer.autor:
                return HttpResponse("Щас")

            Rection.objects.create(answer=answer, user=request.user).save()
            # Rection.objects.create(answer=answer, user=answer.autor).save()
            reac_count = answer.rection_set.count()

            # Запись в модель уведомлений
            Notification.objects.create(
                sender=request.user,
                recipient=answer.autor,
                notification_type="like",
                # related_object_id=answer.id,
                related_object_id=answer.question.id,
            )

            print(reac_count, "<--------- reac_count")
            print(answer.id, "<-------- answer.id")
            print(answer.question.id, "<-------- answer.question.id ")
            return JsonResponse({"success": True, "answer": reac_count})

        except Exception as e:
            print(e)
        except ObjectDoesNotExist:
            ...

    return HttpResponse()


def answer_update_delete(request, **kwargs):
    """Редактировать,удалить ответ"""

    try:

        data = kwargs.get("choice")
        answer_id = kwargs.get("answer_id")

        if data == "ans_update":
            answer_obj = Answer.objects.get(id=answer_id)
            context = {"quest": answer_obj.question, "answer": answer_obj.text}
            return render(request, "questions.html", context)

        elif data == "ans_delete":
            answer_obj = Answer.objects.get(id=answer_id).delete()
            # убрать уведомление
            try:
                Notification.objects.get(
                    sender=request.user,
                    recipient=answer_obj.question.autor,
                    choices="answer",
                ).delete()
            except Exception as e:
                print(e)
            try:
                Notification.objects.get(
                    sender=request.user,
                    recipient=answer_obj.question.autor,
                    choices="like",
                ).delete()
            except Exception as e:
                print(e)
            return redirect(f"/user/{request.user}/")

    except Exception as e:
        print(e, "< === def answer_update_delete(request, **kwargs):")
        return redirect(f"/user/{request.user}/")


def index(request, **kwargs):
    """Главная страница - все вопросы"""

    try:
        page = kwargs.get("num")
        # print(page)

        if page is not None:
            try:
                page = int(page)
                if page < 2:
                    raise ValueError()
            except Exception as e:
                print(e)
                return redirect("all_users")
        else:
            page = 1

        answers = (
            Answer.objects.all()
            .values("question_id")
            .annotate(total=Count("question_id"))
        )
        # ИСПРАВИТЬ
        all_question = Question.objects.all()

        num_pages = int(
            math.ceil(len(all_question) / main.settings.LIMIT_OF_USERS_ON_PAGE)
        )
        users_per_page = main.settings.LIMIT_OF_USERS_ON_PAGE

        paginator = Paginator(all_question, users_per_page)  # Создаем пагинатор
    except Exception as e:
        print(e)

    if num_pages <= 15:
        start = 1
        end = num_pages + 1
    else:
        start = max(1, page - 5)
        end = min(page + 5, num_pages + 1)

        # Корректировка диапазона, если он выходит за пределы допустимых значений
        if end - start < 10:
            if start == 1:
                end = 11
            elif end == num_pages + 1:
                end = num_pages - 9
    if page > 5:
        page_range = range(page - 5, min(page + 5, paginator.num_pages + 1))
    else:
        page_range = range(1, min(page + 10, paginator.num_pages + 1))

    try:
        sorted_users = paginator.page(page)
    except PageNotAnInteger:
        sorted_users = paginator.page(1)
    except EmptyPage:
        sorted_users = paginator.page(paginator.num_pages)

    context = {
        "page_number": page,
        "pages_range": page_range,
        # "pages_range": range(1, num_pages + 1),
        "all_question": sorted_users,
        "answers": answers,
        # "notific": notific,
    }
    # print(page, page_range, sorted_users)

    return render(request, "main/index_main.html", context)


# =================================================================


class EmployeeService:
    _model = "name_model"

    def add(self, **kwargs):
        return self._model.objects.create(**kwargs)

    def get_all(self):
        return self._model.objects.all()

    def get_by_id(self, pk: int):
        return self._model.objects.get(pk=pk)

    def delete_by_id(self, pk: int):
        employee = self._model.objects.get(pk=pk)
        return employee.delete()


service = EmployeeService()

# view.py
# from service import service
# ===========================================================


# t = Teg.objects.all()
#     for i in t:
#         i.name = i.name.replace("#", "").replace(",", "").replace('"', "")
#         i.save()
