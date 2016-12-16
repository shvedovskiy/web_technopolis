from django import forms


class QuestionListForm(forms.Form):
    search = forms.CharField(required=False)
    sort_field = forms.ChoiceField(choices=(('id', 'Identifier'),
                                            ('pub_date', 'Publication date'),
                                            ('question_text', 'Text')))


class NewQuestionForm(forms.Form):
    question_text = forms.CharField(widget=forms.Textarea)
    pub_date = forms.DateTimeField(widget=forms.widgets.DateTimeBaseInput)
