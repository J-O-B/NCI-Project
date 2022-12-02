from django.shortcuts import render
import random

def obfuscate():
    num = random.randint(50, 1000)
    chars = 'a' * num
    return chars

def page_not_found(request, exception):
  template = 'errorpage.html'
  context = {
    'obf': obfuscate()
  }
  return render(request, template, context, status=200)
