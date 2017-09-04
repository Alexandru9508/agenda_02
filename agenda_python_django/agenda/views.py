# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils import timezone


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import AddEvent
# from django.core.mail import send_mail
from .forms import SignUpForm, CreateEventForm
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views import generic




@login_required
def home(request):
    all_event = AddEvent.objects.filter(
        data_ultimei_modificari__lte=timezone.now()).order_by(
        '-data_ultimei_modificari')
    paginator = Paginator(all_event, 3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'contacts': contacts})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = foor.cleaned_data['email']
            # username = form.cleaned_data['username']

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def create_event(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.author = request.user
            event.data_ultimei_modificari = timezone.now()
            event.save()
    form = CreateEventForm()
    return render(request, 'create_event.html', {'form': form})


# class IndexView(generic.ListView):
#     template_name = 'index.html'
#     context_object_name = 'all_event'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return AddEvent.objects.all()


# class DetailView(generic.DetailView):
#     model = AddEvent
#     template_name = 'detail.html'
