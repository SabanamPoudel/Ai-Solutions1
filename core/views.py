import random
import json
import urllib.parse
import urllib.request

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils import timezone

from content.models import AIService, Article, Event, EventImage, ChatbotResponse
from enquiries.models import Enquiry
from feedback.models import Feedback
from enquiries.forms import EnquiryForm
from feedback.forms import FeedbackForm


def _bool_from_post(value, default=True):
    if value is None:
        return default
    return value == 'true'


# ─────────────────────────────────────────────
#  PUBLIC PAGES
# ─────────────────────────────────────────────

def index(request):
    services = AIService.objects.filter(is_active=True)[:6]
    articles = Article.objects.filter(status='published')[:3]
    approved_feedback = Feedback.objects.filter(status='Approved').order_by('-submitted_at')[:5]
    return render(request, 'index.html', {
        'services': services,
        'articles': articles,
        'approved_feedback': approved_feedback,
    })


def services(request):
    all_services = AIService.objects.filter(is_active=True)
    return render(request, 'services.html', {'services': all_services})


def articles(request):
    published_articles = Article.objects.all().order_by('-created_at')
    return render(request, 'articles.html', {'articles': published_articles})


def events(request):
    upcoming = Event.objects.filter(is_upcoming=True).prefetch_related('gallery_images').order_by('event_date')
    past = Event.objects.filter(is_upcoming=False).prefetch_related('gallery_images').order_by('-event_date')[:6]
    return render(request, 'events.html', {'upcoming_events': upcoming, 'past_events': past})


def contact(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'form': EnquiryForm(), 'success': True})
        return render(request, 'contact.html', {'form': form, 'success': False})
    initial = {}
    event_title = request.GET.get('event', '').strip()
    event_date = request.GET.get('date', '').strip()
    event_location = request.GET.get('location', '').strip()
    if event_title:
        initial['subject'] = f'Registration for {event_title}'
        message = f'I would like to register for {event_title}.'
        details = []
        if event_date:
            details.append(f'Date: {event_date}')
        if event_location:
            details.append(f'Location: {event_location}')
        if details:
            message += '\n\n' + '\n'.join(details)
        initial['message'] = message
    return render(request, 'contact.html', {'form': EnquiryForm(initial=initial)})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            approved = Feedback.objects.filter(status='Approved').order_by('-submitted_at')
            return render(request, 'feedback.html', {
                'form': FeedbackForm(),
                'success': True,
                'approved_feedback': approved,
            })
        approved = Feedback.objects.filter(status='Approved').order_by('-submitted_at')
        return render(request, 'feedback.html', {'form': form, 'approved_feedback': approved})

    approved = Feedback.objects.filter(status='Approved').order_by('-submitted_at')
    return render(request, 'feedback.html', {'form': FeedbackForm(), 'approved_feedback': approved})


def case_studies(request):
    return render(request, 'case-studies.html')


# ─────────────────────────────────────────────
#  AUTHENTICATION
# ─────────────────────────────────────────────

@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    error_code = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        recaptcha_response = request.POST.get('g-recaptcha-response', '').strip()

        if not recaptcha_response:
            error_code = 'captcha'
        elif not settings.RECAPTCHA_SECRET_KEY:
            error_code = 'captcha_config'
        else:
            payload = urllib.parse.urlencode({
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response,
            }).encode('utf-8')
            request_obj = urllib.request.Request(
                'https://www.google.com/recaptcha/api/siteverify',
                data=payload,
                method='POST'
            )
            try:
                with urllib.request.urlopen(request_obj, timeout=10) as response:
                    recaptcha_result = json.loads(response.read().decode('utf-8'))
            except Exception:
                recaptcha_result = {'success': False}

            if not recaptcha_result.get('success'):
                error_code = 'captcha'
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None and user.is_staff:
                    login(request, user)
                    return redirect('admin_dashboard')
                error_code = 'credentials'

    return render(request, 'admin-login.html', {
        'error_code': error_code,
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
    })


@never_cache
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# ─────────────────────────────────────────────
#  ADMIN DASHBOARD
# ─────────────────────────────────────────────

@never_cache
@login_required(login_url='/admin-login/')
def admin_dashboard(request):
    # Statistics
    total_enquiries = Enquiry.objects.count()
    pending_enquiries = Enquiry.objects.filter(status='Pending').count()
    total_feedback = Feedback.objects.count()
    approved_feedback = Feedback.objects.filter(status='Approved').count()
    published_articles = Article.objects.filter(status='published').count()
    upcoming_events = Event.objects.filter(is_upcoming=True).count()
    active_services = AIService.objects.filter(is_active=True).count()
    chatbot_responses = ChatbotResponse.objects.filter(is_active=True).count()

    # Tables
    enquiries = Enquiry.objects.all().order_by('-submitted_at')
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    all_articles = Article.objects.all().order_by('-created_at')
    all_events = Event.objects.prefetch_related('gallery_images').all().order_by('event_date')
    upcoming_events_list = Event.objects.filter(is_upcoming=True).prefetch_related('gallery_images').order_by('event_date')
    previous_events_list = Event.objects.filter(is_upcoming=False).prefetch_related('gallery_images').order_by('-event_date')
    all_services = AIService.objects.all()
    chatbot_items = ChatbotResponse.objects.all()

    context = {
        'total_enquiries': total_enquiries,
        'pending_enquiries': pending_enquiries,
        'total_feedback': total_feedback,
        'approved_feedback_count': approved_feedback,
        'published_articles': published_articles,
        'upcoming_events': upcoming_events,
        'active_services': active_services,
        'chatbot_responses': chatbot_responses,
        'enquiries': enquiries,
        'feedbacks': feedbacks,
        'all_articles': all_articles,
        'all_events': all_events,
        'upcoming_events_list': upcoming_events_list,
        'previous_events_list': previous_events_list,
        'all_services': all_services,
        'chatbot_items': chatbot_items,
    }
    return render(request, 'admin-dashboard.html', context)


# ─────────────────────────────────────────────
#  DASHBOARD AJAX ACTIONS
# ─────────────────────────────────────────────

@login_required(login_url='/admin-login/')
@require_POST
def update_enquiry_status(request, pk):
    try:
        enquiry = Enquiry.objects.get(pk=pk)
        new_status = request.POST.get('status')
        valid = [s[0] for s in Enquiry.STATUS_CHOICES]
        if new_status in valid:
            enquiry.status = new_status
            enquiry.save()
            return JsonResponse({'success': True, 'status': new_status})
        return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
    except Enquiry.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def update_feedback_status(request, pk):
    try:
        fb = Feedback.objects.get(pk=pk)
        new_status = request.POST.get('status')
        valid = [s[0] for s in Feedback.STATUS_CHOICES]
        if new_status in valid:
            fb.status = new_status
            fb.save()
            return JsonResponse({'success': True, 'status': new_status})
        return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
    except Feedback.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def delete_enquiry(request, pk):
    try:
        Enquiry.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Enquiry.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def delete_feedback(request, pk):
    try:
        Feedback.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Feedback.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def toggle_article_status(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        article.status = 'draft' if article.status == 'published' else 'published'
        article.save()
        return JsonResponse({'success': True, 'status': article.status})
    except Article.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def toggle_event_status(request, pk):
    try:
        event = Event.objects.get(pk=pk)
        event.is_upcoming = not event.is_upcoming
        event.save()
        return JsonResponse({'success': True, 'is_upcoming': event.is_upcoming})
    except Event.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def save_chatbot_response(request, pk):
    try:
        item = ChatbotResponse.objects.get(pk=pk)
        answer = request.POST.get('answer', '').strip()
        if answer:
            item.answer = answer
            item.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Empty answer'}, status=400)
    except ChatbotResponse.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def add_chatbot_response(request):
    question = request.POST.get('question', '').strip()
    answer = request.POST.get('answer', '').strip()
    if not question or not answer:
        return JsonResponse({'success': False, 'error': 'Question and answer are required'}, status=400)
    ChatbotResponse.objects.create(question=question, answer=answer)
    return JsonResponse({'success': True})


@login_required(login_url='/admin-login/')
@require_POST
def delete_chatbot_response(request, pk):
    try:
        item = ChatbotResponse.objects.get(pk=pk)
        item.delete()
        return JsonResponse({'success': True})
    except ChatbotResponse.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def add_article(request):
    title = request.POST.get('title', '').strip()
    category = request.POST.get('category', '').strip() or 'General'
    excerpt = request.POST.get('excerpt', '').strip()
    content = request.POST.get('content', '').strip()
    image_url = request.POST.get('image_url', '').strip()
    status = request.POST.get('status', 'published').strip()
    if not title or not excerpt:
        return JsonResponse({'success': False, 'error': 'Title and excerpt are required'}, status=400)
    if status not in ['draft', 'published']:
        status = 'published'
    Article.objects.create(
        title=title,
        category=category,
        excerpt=excerpt,
        content=content,
        image=request.FILES.get('image'),
        image_url=image_url,
        status=status,
    )
    return JsonResponse({'success': True})


@login_required(login_url='/admin-login/')
@require_POST
def edit_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

    title = request.POST.get('title', '').strip()
    excerpt = request.POST.get('excerpt', '').strip()
    if not title or not excerpt:
        return JsonResponse({'success': False, 'error': 'Title and excerpt are required'}, status=400)

    article.title = title
    article.category = request.POST.get('category', '').strip() or 'General'
    article.excerpt = excerpt
    article.content = request.POST.get('content', '').strip()
    article.image_url = request.POST.get('image_url', '').strip()
    status = request.POST.get('status', article.status).strip()
    if status in ['draft', 'published']:
        article.status = status
    if request.FILES.get('image'):
        article.image = request.FILES['image']
    article.save()
    return JsonResponse({'success': True})


@login_required(login_url='/admin-login/')
@require_POST
def delete_article(request, pk):
    try:
        Article.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Article.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def add_event(request):
    title = request.POST.get('title', '').strip()
    event_type = request.POST.get('event_type', 'Workshop').strip()
    event_date = request.POST.get('event_date', '').strip()
    location = request.POST.get('location', '').strip()
    description = request.POST.get('description', '').strip()
    is_upcoming = _bool_from_post(request.POST.get('is_upcoming'), True)
    if not title or not event_date or not location:
        return JsonResponse({'success': False, 'error': 'Title, date and location are required'}, status=400)
    valid_types = [t[0] for t in Event.EVENT_TYPES]
    if event_type not in valid_types:
        event_type = 'Workshop'
    event = Event.objects.create(
        title=title, event_type=event_type, event_date=event_date,
        location=location, description=description,
        image=request.FILES.get('image'),
        is_upcoming=is_upcoming
    )
    for image in request.FILES.getlist('gallery_images'):
        EventImage.objects.create(event=event, image=image)
    return JsonResponse({'success': True})


@login_required(login_url='/admin-login/')
@require_POST
def edit_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

    title = request.POST.get('title', '').strip()
    event_date = request.POST.get('event_date', '').strip()
    location = request.POST.get('location', '').strip()
    if not title or not event_date or not location:
        return JsonResponse({'success': False, 'error': 'Title, date and location are required'}, status=400)

    event_type = request.POST.get('event_type', event.event_type).strip()
    if event_type not in [t[0] for t in Event.EVENT_TYPES]:
        event_type = 'Workshop'
    event.title = title
    event.event_type = event_type
    event.event_date = event_date
    event.location = location
    event.description = request.POST.get('description', '').strip()
    event.is_upcoming = _bool_from_post(request.POST.get('is_upcoming'), event.is_upcoming)
    if request.FILES.get('image'):
        event.image = request.FILES['image']
    event.save()
    for image in request.FILES.getlist('gallery_images'):
        EventImage.objects.create(event=event, image=image)
    return JsonResponse({'success': True})


@login_required(login_url='/admin-login/')
@require_POST
def delete_event(request, pk):
    try:
        Event.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except Event.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


@login_required(login_url='/admin-login/')
@require_POST
def add_service(request):
    icon = request.POST.get('icon', '').strip() or '🤖'
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    is_active = _bool_from_post(request.POST.get('is_active'), True)
    if not title or not description:
        return JsonResponse({'success': False, 'error': 'Title and description are required'}, status=400)
    AIService.objects.create(
        icon=icon,
        title=title,
        description=description,
        image=request.FILES.get('image'),
        is_active=is_active,
    )
    return JsonResponse({'success': True})


@login_required(login_url='/admin-login/')
@require_POST
def edit_service(request, pk):
    try:
        service = AIService.objects.get(pk=pk)
    except AIService.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    if not title or not description:
        return JsonResponse({'success': False, 'error': 'Title and description are required'}, status=400)
    service.icon = request.POST.get('icon', '').strip() or '🤖'
    service.title = title
    service.description = description
    service.is_active = _bool_from_post(request.POST.get('is_active'), service.is_active)
    if request.FILES.get('image'):
        service.image = request.FILES['image']
    service.save()
    return JsonResponse({'success': True})


@login_required(login_url='/admin-login/')
@require_POST
def delete_service(request, pk):
    try:
        AIService.objects.get(pk=pk).delete()
        return JsonResponse({'success': True})
    except AIService.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


# ─────────────────────────────────────────────
#  CHATBOT QUERY (public AJAX)
# ─────────────────────────────────────────────

@require_POST
def chatbot_query(request):
    question = request.POST.get('question', '').strip().lower()
    if not question:
        return JsonResponse({'answer': "Please type a question and I'll do my best to help."})
    # Search all active chatbot responses
    responses = ChatbotResponse.objects.filter(is_active=True)
    for item in responses:
        if item.question.strip().lower() in question or question in item.question.strip().lower():
            return JsonResponse({'answer': item.answer})
    return JsonResponse({'answer': "Sorry, I don't have an answer for that right now. Please submit an enquiry through the Contact Us page and our team will get back to you."})
