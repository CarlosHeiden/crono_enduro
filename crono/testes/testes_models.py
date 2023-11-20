from django.test import TestCase
from crono.models import Piloto, RegistrarLargada


class PilotoTestCase(TestCase):
    def setUp(self):
        Piloto.objects.create(
            nome='Wilson Lana',
            numero_piloto=789,
            moto='KXF-450',
            categoria='Over_50',
        )

    def test_retorno_str(self):
        p1 = Piloto.objects.get(nome='Wilson Lana', numero_piloto=789)
        self.assertEquals(p1.__str__(), 'Wilson Lana (789)')
