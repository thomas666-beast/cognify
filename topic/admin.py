from django.contrib import admin
from .models import Topic, Question, Answer


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'about', 'orbit', 'is_active', 'studying_participants_count', 'bosses_count', 'created_at']
    list_filter = ['orbit', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'about__nickname', 'about__firstname', 'about__lastname']
    list_editable = ['is_active']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    filter_horizontal = ['studying_participants', 'bosses']
    inlines = [QuestionInline]

    def studying_participants_count(self, obj):
        return obj.studying_participants.count()

    studying_participants_count.short_description = 'Studying Count'

    def bosses_count(self, obj):
        return obj.bosses.count()

    bosses_count.short_description = 'Bosses Count'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['short_question_text', 'topic', 'is_active', 'order', 'created_at']
    list_filter = ['topic', 'is_active', 'created_at']
    search_fields = ['question_text']
    list_editable = ['is_active', 'order']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['short_answer_text', 'question', 'participant', 'is_admin_generated', 'is_correct', 'order',
                    'created_at']
    list_filter = ['is_correct', 'participant', 'created_at']
    search_fields = ['answer_text', 'question__question_text', 'participant__nickname']
    list_editable = ['is_correct', 'order']
    readonly_fields = ['created_at', 'updated_at']

    def is_admin_generated(self, obj):
        return obj.participant is None

    is_admin_generated.boolean = True
    is_admin_generated.short_description = 'Admin Generated'

