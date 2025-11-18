import os
import shutil
import urllib.parse
from django.conf import settings
from django.db import connections
from django.contrib import messages
from django.http import FileResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.shortcuts import (
    render,
    redirect,
)
from ..models import BackupHistory


@login_required
def backup(request):
    history = BackupHistory.objects.all().order_by('-date')
    context = {
        'history': history,
    }
    return render(request, 'main/backup.html', context)


@login_required
@require_POST
def create_backup(request):
    db_name = settings.DATABASES['default']['NAME']
    try:
        conn = connections[
            settings.DATABASES['default']['NAME']
        ]
        if isinstance(conn, DatabaseWrapper):
            conn.close()
    except Exception:
        pass

    temp_backup_dir = os.path.join(
        settings.BASE_DIR,
        'backups',
    )
    os.makedirs(temp_backup_dir, exist_ok=True)

    description_raw = request.POST.get(
        'description',
        'پشتیبان‌گیری دستی',
    ).strip()

    try:
        backup_instance = BackupHistory.objects.create(
            description=description_raw,
        )

        unique_filename_part = str(backup_instance.uid)
        server_filename = f"{unique_filename_part}.sqlite3"
        temp_backup_path = os.path.join(temp_backup_dir, server_filename)
        download_filename = f"{unique_filename_part}.sqlite3"

        shutil.copy2(db_name, temp_backup_path)

        file_handle = open(temp_backup_path, 'rb')
        response = FileResponse(
            file_handle,
            content_type='application/x-sqlite3',
        )

        encoded_filename = urllib.parse.quote(download_filename)
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'

        def file_cleanup():
            file_handle.close()
            try:
                os.remove(temp_backup_path)
            except OSError as e: ...

        response.close = file_cleanup

        return response

    except Exception as e:
        if 'backup_instance' in locals():
            backup_instance.delete()

        messages.error(
            request,
            f'خطا در ایجاد و دانلود بک‌آپ: {str(e)}',
        )
        return redirect('backup_history')