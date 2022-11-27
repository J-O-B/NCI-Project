from django.shortcuts import render

def page_not_found(request, exception):
  return render(request, 'errorpage.html', status=404)