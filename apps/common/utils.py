import string
import random

def generate_random_string(length=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choices(chars, k=length))