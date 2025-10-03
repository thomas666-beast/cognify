from django import forms
from .models import Topic, Question, Answer


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['about', 'studying_participants', 'bosses', 'title', 'description', 'orbit', 'is_active']
        widgets = {
            'about': forms.Select(attrs={
                'class': 'form-select',
                'data-live-search': 'true'
            }),
            'studying_participants': forms.SelectMultiple(attrs={
                'class': 'form-select studying-participants-select',
                'size': '6',
                'data-live-search': 'true'
            }),
            'bosses': forms.SelectMultiple(attrs={
                'class': 'form-select bosses-select',
                'size': '4',
                'data-live-search': 'true'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter topic title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter topic description...',
                'rows': 5
            }),
            'orbit': forms.Select(attrs={
                'class': 'form-select',
                'data-live-search': 'true'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        help_texts = {
            'title': 'Required. At least 5 characters.',
            'description': 'Required. At least 10 characters.',
            'studying_participants': 'Select participants who are studying about this topic.',
            'bosses': 'Select participants who are bosses for this topic.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add CSS classes to make the form more visually appealing
        self.fields['studying_participants'].widget.attrs.update({
            'class': 'form-select studying-participants-select'
        })
        self.fields['bosses'].widget.attrs.update({
            'class': 'form-select bosses-select'
        })

        # Limit studying_participants and bosses to exclude the 'about' participant
        if self.instance and self.instance.pk:
            excluded_pk = self.instance.about.pk
            self.fields['studying_participants'].queryset = self.fields['studying_participants'].queryset.exclude(
                pk=excluded_pk)
            self.fields['bosses'].queryset = self.fields['bosses'].queryset.exclude(pk=excluded_pk)
        elif 'about' in self.data:
            try:
                about_id = self.data.get('about')
                if about_id:
                    self.fields['studying_participants'].queryset = self.fields[
                        'studying_participants'].queryset.exclude(pk=about_id)
                    self.fields['bosses'].queryset = self.fields['bosses'].queryset.exclude(pk=about_id)
            except (ValueError, TypeError):
                pass

        # Add placeholder text for empty choices
        studying_choices = list(self.fields['studying_participants'].choices)
        boss_choices = list(self.fields['bosses'].choices)

        if not studying_choices:
            self.fields['studying_participants'].widget.attrs.update({
                'disabled': 'disabled'
            })

        if not boss_choices:
            self.fields['bosses'].widget.attrs.update({
                'disabled': 'disabled'
            })


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'order', 'is_active']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your question...',
                'rows': 3
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'participant', 'is_correct', 'order']
        widgets = {
            'answer_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your answer...',
                'rows': 2
            }),
            'participant': forms.Select(attrs={
                'class': 'form-select',
                'data-live-search': 'true'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'participant': 'Select the participant who provided this answer. Leave blank for admin-generated answers.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make participant field optional
        self.fields['participant'].required = False
        self.fields['participant'].empty_label = "--- Admin Generated ---"

        # You can limit participants to those studying the topic if needed
        # if 'question' in self.data:
        #     try:
        #         question_id = self.data.get('question')
        #         question = Question.objects.get(id=question_id)
        #         studying_participants = question.topic.studying_participants.all()
        #         self.fields['participant'].queryset = studying_participants
        #     except (ValueError, TypeError, Question.DoesNotExist):
        #         pass
