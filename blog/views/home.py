from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models.post import Post

from .. import forms
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER


NUM_OF_POSTS = 5


def home(request, username=None):
    first_name = ''
    last_name = ''
    if username:
        user = User.objects.get(username=username)
        first_name = user.first_name
        last_name = user.last_name
        post_list = Post.objects.filter(user=user)
    else:
        post_list = Post.objects.all()

    post_list = post_list.order_by('-pub_date')

    paginator = Paginator(post_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    posts = paginator.get_page(page)

    return render(request, 'blog/home.html', {'posts': posts,
                                              'first_name': first_name,
                                              'last_name': last_name})

def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Blog backend project'
        message = 'Thank you for subscribing to our website.'
        recepient = str(sub['email'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'blog/success.html', {'recepient': recepient})
    return render(request, 'blog/about.html', {'form':sub})


def contact_us(request):
    return render(request, 'blog/contact.html', {})                                            
