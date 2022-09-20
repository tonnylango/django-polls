from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
#from django.http import Http404

from .models import Question, Choice

# Create your views here.
'''def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list,}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
	"""try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not Exist")
	return render(request, 'polls/detail.html', {'question': question})"""
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question':question})'''

'''ListView and DetailView abstract the concept of "display a list of objects" and "display a detail page for a particular type of object".'''
from django.utils import timezone

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		'''Return the last five published questions.'''
		#return Question.objects.order_by('-pub_date')[:5]
		#Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing Questions whose pub_date is less than or equal to- that is earlier than or equal to- timezone.now
		q = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
		return q

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_query(self):
		"""
		Excludes any questions that arent published yet.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())
	
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'	

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#Redisplay the question voting form.
		return render(request, 'polls/detail.html', {'question':question, 'error_message':"You didn't select a choice"})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))