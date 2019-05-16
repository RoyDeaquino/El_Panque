import unittest
from products import PanqueModels


class ProductosTest(unittest.TestCase):

    def test_create_product(self):
        products = PanqueModels('a','a','es')
        pastel = {
            'key': 1, 'name': 'Pastel de Cajeta 3', 'description': 'Pastel de tres leches sabor cajeta con nuez arriba.',
                  'cost': 300, 'size': '20 personas', 'stock': 5}
        products.create_product(
            'Pastel de Cajeta 3', 'Pastel de tres leches sabor cajeta con nuez arriba.', 300, '20 personas', 5, '/home/jintan/PycharmProjects/El_Panque/pin.png')

        self.assertEqual(products.read_product('Pastel de Cajeta '),
                         pastel)

    def read_product(self):
        """{'key': 1, 'name': 'Pastel de cajeta completo', 'description': 'PAstel de tres leches sabor cajeta decorado con crema batida, nuez y tiras de cajeta. Ideal para 20 o 30 personas.'}
            {'key': 1, 'name': 'Gelatina frambuesa chica', 'description': 'Gelatina sabor frambuesa y yogurth natural individual.'}
            {'key': 1, 'name': 'Pastel de cajeta completo', 'description': 'PAstel de tres leches sabor cajeta decorado con crema batida, nuez y tiras de cajeta. Ideal para 20 o 30 personas.'}
        """
        products = PanqueModels()
        p = products.read_product('Pastel de Cajeta')
        p2 = products.read_product('Test')
        p3 = products.read_product('pan')
        print(p)
        print(p2)
        print(p3)


if __name__ == '__main__':
    unittest.main()
