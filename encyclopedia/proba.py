import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


_, filenames = default_storage.listdir("entries")

print(type(filenames))