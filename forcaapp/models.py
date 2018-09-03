from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Partida(models.Model):
	userId = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name='id-user', default=0)
	allTrue = models.BooleanField(default=False, verbose_name='final')
	image = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name='image', default=1)
	state = models.BooleanField(default=True, verbose_name='estado')
	dica = models.CharField(max_length=150, verbose_name='dica')

	def __str__(self):
		return 'partida'
	  
	class Meta:
		verbose_name = 'partida'
		verbose_name_plural = 'partidas'

class Profile(models.Model):
	userName = models.CharField(max_length=150, verbose_name='userName')
	userId = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name='id-user', default=0)
	Individualpontos = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name='pointsI', default=0)

	def __str__(self):
		return ('User' + str(self.userId))
	  
	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'

class Palavra(models.Model):
	palavra = models.CharField(max_length=150, verbose_name='palavra')
	dica = models.CharField(max_length=150, verbose_name='dica')

	def __str__(self):
		return self.palavra
	  
	class Meta:
		verbose_name = 'palavra'
		verbose_name_plural = 'palavras'

class Letras(models.Model):
	letra = models.CharField(max_length=150, verbose_name='letra')
	partidaId = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name='id-partida', default=0)
	visible = models.BooleanField(default=False, verbose_name='visivel')

	def __str__(self):
		return self.letra
	  
	class Meta:
		verbose_name = 'letra'
		verbose_name_plural = 'letras'