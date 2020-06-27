from django.conf import settings
from django.template.loader import render_to_string
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site


# Create your models here.


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    view = models.IntegerField(default=0)
    author = models.CharField(max_length=100)
    slug = models.CharField(max_length=200)
    timeStamp = models.DateTimeField(blank=True)
    series_name = models.CharField(max_length=200, default="okay")

    def __str__(self):
        return self.title + ' by ' + self.author

    def send_mail(self, request):
        content = self.content
        title = self.title
        slug = self.slug
        series_name = self.series_name
        confirmed_subscribers = Subscriber.objects.values_list('email').filter(confirmed=True)

        if request.method == 'POST':
            for sub in confirmed_subscribers:
                # subject = "New Blog on '" + title + "' @ AM-Blogs!!"
                # message = render_to_string('new_post.html',{
                #     'title': title,
                #     'content': content,
                #     'slug': slug,
                #     'series_name': series_name,
                # })
                current_site = get_current_site(request)
                subject = "New Blog - '" + title + "' @ AM-Blogs!!"
                message = render_to_string('new_post.html', {
                    'title': title,
                    'content': content,
                    'slug': slug,
                    'series_name': series_name,
                    'domain': current_site.domain,
                })
                emailsub = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    sub,
                )
                emailsub.fail_silently = True
                emailsub.send()

            return redirect('Home')


class Series(models.Model):
    sno = models.AutoField(primary_key=True)
    series_name = models.CharField(max_length=200)
    ser_slug = models.CharField(max_length=200, default="okay")
    ser_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.series_name

    class Meta:
        verbose_name_plural = "Series"


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:12] + "....." + " by " + self.user.first_name


class Subscriber(models.Model):
    email = models.EmailField()
    confirmed = models.BooleanField(default=False)
    timeStamp = models.DateTimeField(auto_now_add=True)
    subscriber_count = models.IntegerField(default=0)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed == True else "") + "confirmed)"
