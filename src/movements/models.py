from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Frequency(models.Model):

    _from = models.IntegerField(
        default=0, verbose_name='From',
        help_text='Frequency from', blank=True, null=True)
    _to = models.IntegerField(
        default=0, verbose_name='To',
        help_text='Frequency to', blank=True, null=True)
    instalments = models.IntegerField(
        default=1, verbose_name='Instalments',
        help_text='Frequency instalments',
        validators=[MinValueValidator(1), MaxValueValidator(1000000000)])
    rule = models.CharField(
        max_length=500, verbose_name='Rule',
        help_text='Frequency rule', blank=True, null=True)

    def __str__(self):
        return self._from + ' - ' + self._to

# Cada 5 meses
# AÑO 1: 01 - 06 - 11
# AÑO 2: 04 - 09
# AÑO 3: 02 - 07 - 12
# AÑO 4: 05 - 10
# AÑO 5: 03 - 08
# AÑO 6: 01 - 06 - 11

# Cada 7 meses
# AÑO 1: 01 - 08
# AÑO 2: 03 - 10
# AÑO 3: 05 - 12
# AÑO 4: 07
# AÑO 5: 02 - 09
# AÑO 6: 04 - 11
# AÑO 7: 06
# AÑO 8: 01 - 08


class Movement(Frequency):
    """
    Movement model
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Movement'
        verbose_name_plural = 'Movements'


months = {

}
