from django.db import models

def tf_response_default():
    return {"predictions": "none"}

class Request(models.Model):
    request = models.TextField()
    response = models.JSONField("TfResponse", default=tf_response_default)
    request_time = models.DateTimeField()
    response_time = models.DateTimeField()

    def __str__(self):
        return self.request
