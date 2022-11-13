import uuid
from models.models import Log
from datetime import datetime


class LogService(object):
    def add_one(self, method, url, headers, request):
        log_obj = Log(
            log_id=str(uuid.uuid4()),
            method=method,
            url=url,
            headers=headers,
            request=request,
        )
        result = log_obj.save()
        return result

    def update_one(self, id, response, status_code):
        log_obj = Log.objects.filter(log_id=id).first()
        start = log_obj.created_at.strftime("%s")
        end = datetime.now().strftime("%s")
        diff = int(end) - int(start)
        log_obj.response = response
        log_obj.status_code = status_code
        log_obj.elapse_time = diff
        log_obj.save()
