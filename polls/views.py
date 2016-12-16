from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.shortcuts import resolve_url
from .models import Choice, Question
from .forms import QuestionListForm, NewQuestionForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def dispatch(self, request, *args, **kwargs):
        self.sort_search_form = QuestionListForm(request.GET)
        self.sort_search_form.is_valid()
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Question.objects.filter(pub_date__lte=timezone.now())  # author=self.request.user
        if self.sort_search_form.cleaned_data.get('search'):
            queryset = queryset.filter(question_text__icontains=self.sort_search_form.cleaned_data['search'])
        if self.sort_search_form.cleaned_data.get('sort_field'):
            queryset = queryset.order_by(self.sort_search_form.cleaned_data['sort_field'])[:5]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sort_search_form'] = self.sort_search_form
        return context


class CreateView(generic.CreateView):
    model = Question
    template_name = 'polls/create.html'
    fields = ('pub_date', 'question_text')

    def dispatch(self, request, *args, **kwargs):
        self.new_question_form = NewQuestionForm(request.POST or None)
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['new_question_form'] = self.new_question_form
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

    def get_success_url(self):  # redirect after create
        return resolve_url('polls:detail', pk=self.object.pk)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    context_object_name = 'question'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render_to_response('polls/detail.html', {
            'question': question,
            'error_message': 'You didn\'t select a choice'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
