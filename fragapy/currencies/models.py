from django.db import models
from django.utils.translation import gettext_lazy as _

class Currency(models.Model):
	code = models.CharField(_('code'), max_length=3)
	name = models.CharField(_('name'), max_length=25)
	symbol = models.CharField(_('symbol'), max_length=4)
	symbol_preceeds = models.BooleanField(_('symbol preceeds'), default=True,
		help_text=_('Is symbol placed before the price value?'))
	decimal_places = models.PositiveSmallIntegerField(_('decimal places'), default=2,
		help_text=_('How many decimal places should be used.'))
	decimal_separator = models.CharField(_('decimal separator'), max_length=1, default='.')
	thousand_separator = models.CharField(_('thousand separator'), max_length=2, default=' ')
	factor = models.DecimalField(_('factor'), max_digits=10, decimal_places=4,
		default=1, help_text=_('Specifies the difference of the currency to '
		'default one.'))
	is_active = models.BooleanField(_('active'), default=True,
		help_text=_('The currency will be available.'))
	is_default = models.BooleanField(_('default'), default=False,
		help_text=_('Make this the default currency.'))

	class Meta:
		verbose_name = _('currency')
		verbose_name_plural = _('currencies')

	def __unicode__(self):
		return self.code

	def save(self, **kwargs):
		if len(Currency.objects.filter(is_default=True)) == 0:
			self.is_default = True
		if self.is_default:
			try:
				default_currency = Currency.objects.get(is_default=True)
			except Currency.DoesNotExist:
				pass
			else:
				default_currency.is_default = False
				default_currency.save()
		super(Currency, self).save(**kwargs)
