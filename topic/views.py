from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from master.views import master_required
from orbit.models import Orbit
from .models import Topic, Question, Answer
from .forms import TopicForm, QuestionForm, AnswerForm
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
@master_required
def topic_list(request):
    topics = Topic.get_optimized_queryset().all()

    # Filter by orbit if provided
    orbit_filter = request.GET.get('orbit')
    if orbit_filter:
        topics = topics.filter(orbit_id=orbit_filter)

    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        topics = topics.filter(is_active=True)
    elif status_filter == 'inactive':
        topics = topics.filter(is_active=False)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        topics = topics.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(about__nickname__icontains=search_query) |
            models.Q(about__firstname__icontains=search_query) |
            models.Q(about__lastname__icontains=search_query)
        )

    orbits = Orbit.objects.all()

    context = {
        'topics': topics,
        'orbits': orbits,
        'current_orbit': orbit_filter,
        'current_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'topics/topic_list.html', context)


@master_required
def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            messages.success(request, f'Topic "{topic.title}" created successfully!')
            return redirect('topics:topic_list')
    else:
        form = TopicForm()

    context = {
        'form': form,
        'title': 'Create New Topic'
    }
    return render(request, 'topics/topic_form.html', context)


@master_required
def topic_update(request, slug):
    topic = get_object_or_404(Topic, slug=slug)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save()
            messages.success(request, f'Topic "{topic.title}" updated successfully!')
            return redirect('topics:topic_list')
    else:
        form = TopicForm(instance=topic)

    context = {
        'form': form,
        'topic': topic,
        'title': f'Edit Topic: {topic.title}'
    }
    return render(request, 'topics/topic_form.html', context)


@master_required
def topic_detail(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    questions = topic.questions.all().order_by('order')

    context = {
        'topic': topic,
        'questions': questions,
    }
    return render(request, 'topics/topic_detail.html', context)


@master_required
def topic_delete(request, slug):
    topic = get_object_or_404(Topic, slug=slug)

    if request.method == 'POST':
        topic_title = topic.title
        topic.delete()
        messages.success(request, f'Topic "{topic_title}" deleted successfully!')
        return redirect('topics:topic_list')

    context = {
        'topic': topic
    }
    return render(request, 'topics/topic_confirm_delete.html', context)


@master_required
def topic_activate(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    topic.activate()
    messages.success(request, f'Topic "{topic.title}" activated successfully!')
    return redirect('topics:topic_list')


@master_required
def topic_deactivate(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    topic.deactivate()
    messages.success(request, f'Topic "{topic.title}" deactivated successfully!')
    return redirect('topics:topic_list')


@master_required
def question_create(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.topic = topic
            question.save()
            messages.success(request, f'Question added successfully!')
            return redirect('topics:topic_detail', slug=topic_slug)
    else:
        form = QuestionForm()

    context = {
        'form': form,
        'topic': topic,
        'title': f'Add Question to: {topic.title}'
    }
    return render(request, 'topics/question_form.html', context)


@master_required
def question_update(request, topic_slug, question_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    question = get_object_or_404(Question, id=question_id, topic=topic)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, f'Question updated successfully!')
            return redirect('topics:topic_detail', slug=topic_slug)
    else:
        form = QuestionForm(instance=question)

    context = {
        'form': form,
        'topic': topic,
        'question': question,
        'title': f'Edit Question: {topic.title}'
    }
    return render(request, 'topics/question_form.html', context)


@master_required
def question_delete(request, topic_slug, question_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    question = get_object_or_404(Question, id=question_id, topic=topic)

    if request.method == 'POST':
        question.delete()
        messages.success(request, f'Question deleted successfully!')
        return redirect('topics:topic_detail', slug=topic_slug)

    context = {
        'topic': topic,
        'question': question
    }
    return render(request, 'topics/question_confirm_delete.html', context)


@master_required
def question_detail(request, topic_slug, question_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    question = get_object_or_404(Question, id=question_id, topic=topic)
    answers = question.answers.all().order_by('order')

    context = {
        'topic': topic,
        'question': question,
        'answers': answers,
    }
    return render(request, 'topics/question_detail.html', context)


@master_required
def answer_create(request, topic_slug, question_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    question = get_object_or_404(Question, id=question_id, topic=topic)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, f'Answer added successfully!')
            return redirect('topics:question_detail', topic_slug=topic_slug, question_id=question_id)
    else:
        form = AnswerForm()

    context = {
        'form': form,
        'topic': topic,
        'question': question,
        'title': f'Add Answer to Question'
    }
    return render(request, 'topics/answer_form.html', context)


@master_required
def answer_update(request, topic_slug, question_id, answer_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    question = get_object_or_404(Question, id=question_id, topic=topic)
    answer = get_object_or_404(Answer, id=answer_id, question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Answer updated successfully!')
            return redirect('topics:question_detail', topic_slug=topic_slug, question_id=question_id)
    else:
        form = AnswerForm(instance=answer)

    context = {
        'form': form,
        'topic': topic,
        'question': question,
        'answer': answer,
        'title': f'Edit Answer'
    }
    return render(request, 'topics/answer_form.html', context)


@master_required
def answer_delete(request, topic_slug, question_id, answer_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    question = get_object_or_404(Question, id=question_id, topic=topic)
    answer = get_object_or_404(Answer, id=answer_id, question=question)

    if request.method == 'POST':
        answer.delete()
        messages.success(request, f'Answer deleted successfully!')
        return redirect('topics:question_detail', topic_slug=topic_slug, question_id=question_id)

    context = {
        'topic': topic,
        'question': question,
        'answer': answer
    }
    return render(request, 'topics/answer_confirm_delete.html', context)
