from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from decouple import config
import shutil
import os

from my_email.send_mail import send_mail_
from main.models import User, Image
from ..forms import ImageForm

EMAIL = config("EMAIL_HOST_USER")


def delete_folder(folder_path):
    """Удалить текущую папку uuid перед созданием новой"""

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Папка '{folder_path}' успешно удалена.")
    else:
        print(f"Папка '{folder_path}' не существует.")


def image_upload_view(request):
    """Загрузка фото пользователя"""

    def save_image_url_user(img_obj):
        User.objects.filter(
            username=request.user.username,
        ).update(image_url=str(img_obj)[23:59])

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img_obj = Image.objects.filter(user_id=request.user)
            if img_obj is not None:
                img_obj.delete()

            image = form.save(commit=False)
            image.user = request.user
            image.save()

            img_obj = form.instance
            #
            print(form.cleaned_data["image"], "<<< ----------")

            if form.cleaned_data["image"] is None:
                messages.success(request, "Нет файла")
                return render(request, "load_img.html", {"form": form})
            # =================================================================

            # Получить имя папки для удаления
            # перед созданием новой (uuid)

            user_obj = User.objects.filter(username=request.user.username).first()
            dir_uuid = user_obj.image_url

            # Если нет папки,то создать новую
            if dir_uuid == "":
                save_image_url_user(img_obj.image)
                return redirect("user_profile", request.user.username)

            # Если есть папка,получить полный путь
            folder_path = f"static/profile/picture/{dir_uuid}"
            delete_folder(folder_path)

            save_image_url_user(img_obj.image)

            # При отсутствии настроек почты
            try:
                message = form.cleaned_data["image"]
                send_mail_("Фото", EMAIL, message)
            except:
                ...

        return redirect("user_profile", request.user.username)
    else:
        form = ImageForm()
    return render(request, "load_img.html", {"form": form})
