from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
import random
from django.urls import reverse_lazy

from . import models, forms

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class CreateMatch(generic.ListView):
	model = models.Partida
	#form_class = forms.CreateMatchForm
	#success_url = reverse_lazy('match')
	template_name = 'confirm.html' 
	def post(self, form):
		if(models.Partida.objects.all()):
			idPartida = models.Partida.objects.get(userId=self.request.user.pk).id
			if models.Partida.objects.get(userId=self.request.user.pk).state == False:
				models.Partida.objects.filter(userId=self.request.user.pk).delete()
				models.Letras.objects.filter(partidaId = idPartida).delete()
				partida = models.Partida.objects.create(userId=self.request.user.pk, dica='')
				partida.save()
			else:
				return HttpResponseRedirect('/inmatch/')
		else:
				partida = models.Partida.objects.create(userId=self.request.user.pk, dica='')
				partida.save()

		if models.Profile.objects.filter(userId=self.request.user.pk):
			pass
		else:
			profile = models.Profile.objects.create(userId=self.request.user.pk, userName= self.request.user.username)
			profile.save()
		return HttpResponseRedirect('/inmatch/')
		
class Ranking(generic.ListView):
	model = models.Profile
	template_name = 'ranking.html'
	def get_queryset(self):

		users = models.Profile.objects.all()
		UserPerPoints = []
		objs = []
		for x in users:
			UserPerPoints.append(x.Individualpontos)
		UserPerPoints = list(set(UserPerPoints))
		UserPerPoints.sort(reverse=True)
		for y in UserPerPoints:
			if models.Profile.objects.filter(Individualpontos=y) not in objs:
				objs.append(models.Profile.objects.filter(Individualpontos=y))
		
		print(UserPerPoints)
		return objs


class CreateWord(generic.CreateView):
	model = models.Palavra
	#form_class = forms.CreateMatchForm
	success_url = reverse_lazy('home')
	template_name = 'create-word.html'
	fields = ('palavra','dica',)

# Create your views here.
class inMatch(ListView):
	model = models.Partida
	template_name = 'inpartida.html'
	

	def get_context_data(self, **kwargs):
		global idDica
		kwargs['images'] = models.Partida.objects.all()
		return super(inMatch, self).get_context_data(**kwargs)

	def get_queryset(self):

		if(len(models.Palavra.objects.all()) >= 1):
			global idPartida
			idPartida = idPartida = models.Partida.objects.get(userId=self.request.user.pk).id
			word = []
			for x in models.Palavra.objects.all():
				word.append(x.id)
			wordPos = random.choice(word)
			obj = models.Palavra.objects.filter(id = wordPos) 
			string = str(obj[0])

			if (models.Letras.objects.filter(partidaId = idPartida)):
				pass
			else:
				obj1 = models.Palavra.objects.get(id = wordPos)
				models.Partida.objects.filter(userId=self.request.user.pk).update(dica= obj1.dica)
				for y in list(string):
					p = models.Letras.objects.create(letra=y, partidaId=idPartida)
					p.save()
			global finalTest
			finalTest = None
			allVisible = []
			count = 0
			for x in models.Letras.objects.filter(partidaId=idPartida):
				allVisible.append(x.visible)

			if(all(allVisible)):
				models.Partida.objects.filter(userId=self.request.user.pk).update(allTrue= True, state= False)
				pontosAtual = models.Profile.objects.get(userId=self.request.user.pk).Individualpontos
				pontosAtual +=10
				models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos= pontosAtual)

				return models.Partida.objects.filter(userId=self.request.user.pk)
			
			atualPartida = models.Partida.objects.get(userId=self.request.user.pk)
			if(atualPartida.image == 7):
				models.Partida.objects.filter(userId=self.request.user.pk).update(state= False)
				return models.Partida.objects.filter(userId=self.request.user.pk)
	
			#print(finalTest)
		return models.Letras.objects.filter(partidaId=idPartida)
	
	def post(self, request):
		atualPartida = models.Partida.objects.get(userId=self.request.user.pk)

		if(atualPartida.image == 7):
			models.Partida.objects.filter(userId=self.request.user.pk).update(state= False)
			print('if 2')
			return HttpResponseRedirect('/game-fail/')

		letras = []
		for x in models.Letras.objects.filter(partidaId=idPartida):
			letras.append(x.letra)
		if 'Q' in self.request.POST:
			if('q' in letras):
				obj =  models.Letras.objects.filter(letra='q')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
						return HttpResponseRedirect('/inmatch/')
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)


		elif 'W' in self.request.POST:
			if('w' in letras):
				obj =  models.Letras.objects.filter(letra='w')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'E' in self.request.POST:
			if('e' in letras):
				obj =  models.Letras.objects.filter(letra='e')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'R' in self.request.POST:
			if('r' in letras):
				obj =  models.Letras.objects.filter(letra='r')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'T' in self.request.POST:
			if('t' in letras):
				obj =  models.Letras.objects.filter(letra='t')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)
		elif 'Y' in self.request.POST:
			if('y' in letras):
				obj =  models.Letras.objects.filter(letra='y')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'U' in self.request.POST:
			if('u' in letras):
				obj =  models.Letras.objects.filter(letra='u')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'I' in self.request.POST:
			if('i' in letras):
				obj =  models.Letras.objects.filter(letra='i')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'O' in self.request.POST:
			if('o' in letras):
				obj =  models.Letras.objects.filter(letra='o')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'P' in self.request.POST:
			if('p' in letras):
				obj =  models.Letras.objects.filter(letra='p')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'A' in self.request.POST:
			if('a' in letras):
				obj =  models.Letras.objects.filter(letra='a')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()

			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'S' in self.request.POST:
			if('s' in letras):
				obj =  models.Letras.objects.filter(letra='s')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'D' in self.request.POST:
			if('d' in letras):
				obj =  models.Letras.objects.filter(letra='d')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'F' in self.request.POST:
			if('f' in letras):
				obj =  models.Letras.objects.filter(letra='f')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'G' in self.request.POST:
			if('g' in letras):
				obj =  models.Letras.objects.filter(letra='g')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'H' in self.request.POST:
			if('h' in letras):
				obj =  models.Letras.objects.filter(letra='h')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
						return HttpResponseRedirect('/inmatch/')
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'J' in self.request.POST:
			if('j' in letras):
				obj =  models.Letras.objects.filter(letra='j')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'K' in self.request.POST:
			if('k' in letras):
				obj =  models.Letras.objects.filter(letra='k')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'L' in self.request.POST:
			if('l' in letras):
				obj =  models.Letras.objects.filter(letra='l')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'Ç' in self.request.POST:
			if('ç' in letras):
				obj =  models.Letras.objects.filter(letra='ç')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'Z' in self.request.POST:
			if('z' in letras):
				obj =  models.Letras.objects.filter(letra='z')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'X' in self.request.POST:
			if('x' in letras):
				obj =  models.Letras.objects.filter(letra='x')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'C' in self.request.POST:
			if('c' in letras):
				obj =  models.Letras.objects.filter(letra='c')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'V' in self.request.POST:
			if('v' in letras):
				obj =  models.Letras.objects.filter(letra='v')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'B' in self.request.POST:
			if('b' in letras):
				obj =  models.Letras.objects.filter(letra='b')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		elif 'N' in self.request.POST:
			if('n' in letras):
				obj =  models.Letras.objects.filter(letra='n')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		else:
			if('m' in letras):
				obj =  models.Letras.objects.filter(letra='m')
				for x in obj:
					if(x.visible == False):
						x.visible = True
						x.save()
			else:
				obj =  models.Partida.objects.get(userId=self.request.user.pk)
				image = obj.image
				image = image + 1
				models.Partida.objects.filter(userId=self.request.user.pk).update(image= image)
				obj =  models.Profile.objects.get(userId=self.request.user.pk)
				if(obj.Individualpontos >=1):
					finalPoints = obj.Individualpontos
					finalPoints-=1
					models.Profile.objects.filter(userId=self.request.user.pk).update(Individualpontos=finalPoints)

		return HttpResponseRedirect('/inmatch/')
	



		