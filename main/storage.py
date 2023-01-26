from django.core.files.storage import FileSystemStorage
import os,time,random

class FieldStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(FieldStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(10000, 99999)
        name = os.path.join(d, fn + ext)
        return super(FieldStorage, self)._save(name, content)