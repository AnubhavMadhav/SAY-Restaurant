from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Contact, Post, BlogComment, Series, Subscriber
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from blog.templatetags import extras
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .tokens import generate_token


# Create your views here.

def index(request):
    return render(request, 'say/index.html')


# def blogHome(request):
#     allPosts = Post.objects.all()
#     context = {'allPosts': allPosts}
#     return render(request, 'blog/blogHome.html', context)
#
#
# def blogPost(request, slug):
#     post = Post.objects.filter(slug=slug).first()
#     post.view = post.view + 1
#     post.save()
#     comments = BlogComment.objects.filter(post=post, parent=None)
#     replies = BlogComment.objects.filter(post=post).exclude(parent=None)
#     replyDict = {}
#     for reply in replies:
#         if reply.parent.sno not in replyDict.keys():
#             replyDict[reply.parent.sno] = [reply]
#         else:
#             replyDict[reply.parent.sno].append(reply)
#     context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
#     return render(request, 'blog/blogPost.html', context)


def about(request):
    return HttpResponse("Hi")

def menu(request):
    return HttpResponse("menu")

def order(request):
    return HttpResponse("order")

def contact(request):
    # messages.success(request, 'Get in touch with me!!')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if name == '':
            messages.error(request, "You must enter your name!!")
        elif email == '':
            messages.error(request, "Please enter your email!!")
        elif phone == '':
            messages.error(request, "Please enter your phone number!!")
        elif content == '':
            messages.error(request, "Please enter your message!!")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been conveyed!!")

            subject = "Contact from AM-Blogs!!"
            message = contact.name + " " + contact.email + " says " + contact.content
            from_email = settings.EMAIL_HOST_USER
            to_list = ["anubhavmadhav20@gmail.com", "201851024@iiitvadodara.ac.in"]

            send_mail(subject, message, from_email, to_list, fail_silently=True)

            subject2 = "Message from AM-Blogs!!"
            message2 = "Hello " + contact.name + ". " + " Your message has been conveyed to Anubhav Madhav. He will try to respond as soon as possible."
            from_email2 = settings.EMAIL_HOST_USER
            to_list2 = [contact.email]

            send_mail(subject2, message2, from_email2, to_list2, fail_silently=True)

    return render(request, 'blog/contact.html')


def search(request):
    query = request.GET['query']
    if len(query) > 70:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    context = {'allPosts': allPosts, 'query': query}
    return render(request, 'blog/search.html', context)


def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def handleSignup(request):

    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # fname = request.POST.get['fname']
        # lname = request.POST.get['lname']
        # address1 = request.POST.get['address1']
        # address2 = request.POST.get['address2']
        # city = request.POST.get['city']
        # contact = request.POST.get['contact']
        # email = request.POST.get['email']
        # pass1 = request.POST.get['pass1']
        # pass2 = request.POST.get['pass2']

        # Check for erroneous inputs

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('index')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('index')


        # Check if username already exists

        # Check if email already exists

        myuser = User.objects.create_user(email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to SAY-Restaurant!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to SAY-Restaurant!! \nThank you for visiting our website. We'll surely serve you at our best. We hope you'll love our services.\nWe have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @SAY-Restaurant!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        # template = render_to_string('email_confirmation.html', {'name': myuser.first_name })

        # email = EmailMessage(
        #     'Confirm your Email @ AM-Blogs!!',
        #     template,
        #     settings.EMAIL_HOST_USER,
        #     [myuser.email],

        # )
        # email.fail_silently = True
        # email.send()

        # name = myuser.first_name

        # send_mail(
        # 'Confirm your Email @ AM-Blogs!!',
        # get_template('email_confirmation.html').render(
        # Context({
        #    'name': name,
        # })
        # ),
        # settings.EMAIL_HOST_USER,
        # [myuser.email],
        # fail_silently = True
        # )

        return redirect('index')

    else:
        return HttpResponse("404- Not Found")


def handleLogin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=email, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully!!")
            return redirect('index')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('index')

    return HttpResponse("404")  # if request method is not 'post'


def handleLogout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('Home')

    # return HttpResponse("Logged Out")


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted!!")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(request, "Your reply has been posted!!")

    return redirect(f"/{post.slug}")


def series(request):
    allseries = Series.objects.all()
    print(allseries)
    context = {'allseries': allseries}
    return render(request, 'blog/series.html', context)


# series slug should be equal to series_name of the post in order to render properly

def series_list(request, ser_slug):
    ser_post = Series.objects.filter(ser_slug=ser_slug).values()
    ser_post_done = Post.objects.filter(series_name=ser_slug).values()

    for ser in ser_post_done:
        if ser_slug == ser['series_name']:
            series_name = ser['series_name']
            slug_final = ser['slug']
            context = {'ser_post_done': ser_post_done, 'slug_final': slug_final, 'series_name': series_name}
            return render(request, 'blog/series_list.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('Home')
    else:
        return render(request, 'activation_failed.html')


def subscribe(request):
    if request.method == 'POST':
        email = request.POST['emailsubscribe']

        subscriber = Subscriber(email=email)

        if Subscriber.objects.filter(email=email).exists():
            messages.error(request,
                           "This email is already registered!! We have already sent a confirmation email to this address, please search in your mailbox.")
            return redirect('Home')

        subscriber.save()
        messages.success(request, "A confirmation email has been sent to you!! Please confirm your email.")

        current_site = get_current_site(request)
        email_subject = "Subscribe your Email @ AM-Blogs!!"
        message = render_to_string('subscription_confirmation.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(subscriber.pk)),
            'token': generate_token.make_token(subscriber)
        })
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [subscriber.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('Home')


def subscriber_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        subscriber = Subscriber.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Subscriber.DoesNotExist):
        subscriber = None

    if subscriber is not None and generate_token.check_token(subscriber, token):
        subscriber.confirmed = True
        # subscriber.subscriber_count += 1
        subscriber.save()
        # print(subscriber.subscriber_count)
        messages.success(request, "Your Email has been Registered!!")
        return redirect('Home')
    else:
        # subscriber.delete()
        return render(request, 'subscription_failed.html')