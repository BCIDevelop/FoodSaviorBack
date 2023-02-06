from flask_seeder import Seeder
from app.models.categories_model import CategoryModel

class CategorySeeder(Seeder):
    def run(self):
        categories = [
            {
                'name':'Abarrotes',
            },
            {
                'name': 'Frutas y Verduras'            
            },
            {
                'name':'Congelado'
            },
            {
                'name':'No Perecibles'
            },
            {
                'name':'Por definir'
            },
        ]

        for category in categories:
            record=CategoryModel.where(name=category['name']).first()
            if not record:
                print(f'se crea categoria: {category}')
                new_record=CategoryModel.create(**category)
                self.db.session.add(new_record)

