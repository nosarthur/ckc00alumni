from pathlib import Path
import sqlite3

from django.core.management.base import BaseCommand
from django.conf import settings

from cities_light.models import City, Country, Region
from api.models import MyUser, Division, Tag


tags = ['software', 'professor', 'law', 'finance', 'incubator', 'research',
        'parent-1.0', 'parent-2.0', 'parent-3.0',
        'block-chain', 'biotech',
        'runner',
        ]
division_props = {'mixed': 9, 'litart': 2, 'science': 3, 'eduexp': 1}


def _dict_factory(cursor, row):
    """
    Convert sqlite3 database row into `dict`
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Command(BaseCommand):
    help = ('Initialize database, including populating the Division table, '
            'Tag table, and converting user information from the old database.')

    def _init_tag(self):
        Tag.objects.all().delete()
        Tag.objects.bulk_create(Tag(name=t) for t in tags)

    def _init_user(self):
        old_db = Path(settings.BASE_DIR) / 'old-db.sqlite'
        if old_db.exists():
            MyUser.objects.all().delete()
            db = sqlite3.connect(old_db)
            db.row_factory = _dict_factory
            c = db.cursor()
            c.execute('select name, sex, city, state, class_type, class_id, '
                      'email, site from users;')
            users = c.fetchall()
            nos = MyUser.objects.create(
                    email='zhou.dong@gmail.com',
                    first_name='Dong',
                    last_name='Zhou',
                    gender='m',
                    is_superuser=True,
                    is_staff=True,
                        )
            nos.set_password('a')
            nos.save()
            usa = Country.objects.get(name='United States')
            canada = Country.objects.get(name='Canada')
            for u in users:
                print(u)
                if u['email'] and u['email'] != 'zhou.dong@gmail.com':
                    first, last = u['name'].split()
                    try:
                        n = int(u['class_id'])
                    except (TypeError, ValueError):  # expedu has only 1 class
                        n = 1
                    d = Division.objects.get(name=u['class_type'], number=n)
                    mu = MyUser(first_name=first, last_name=last, gender=u['sex'],
                                email=u['email'], homepage=u['site'], division=d,
                                referred_by=nos,
                                )
                    # set city
                    if mu.get_full_name() == 'Yuxiao Hu':
                        mu.city = City.objects.get(name='Waterloo', country=canada)
                    elif mu.get_full_name() == 'Jing Wu':
                        mu.city = City.objects.get(name='Toronto', country=canada)
                    elif mu.get_full_name() == 'Qian You':
                        # typo in the old database
                        mu.city = City.objects.get(name='Los Angeles', country=usa)
                    elif mu.get_full_name() in {'Cunzhen Huang', 'Zhenjia Meng'}:
                        mu.city = City.objects.get(name='Washington, D.C.', country=usa)
                    elif mu.get_full_name() in {'Jie Chen', 'Bo Wang'}:
                        pass  # for some reason, (Yorktown Heights, Stanford) are not in the database
                    else:
                        state = Region.objects.get(geoname_code=u['state'], country=usa)
                        city_name = u['city']
                        if city_name == 'New York':
                            city_name = 'New York City'
                        mu.city = City.objects.get(name=city_name, region=state)
                    if mu.city:
                        mu.country = mu.city.country
                    mu.save()

    def _init_division(self):
        Division.objects.all().delete()
        for name, count in division_props.items():
            for n in range(1, count+1):
                div = Division(name=name, number=n)
                div.save()

    def handle(self, *args, **options):
        self._init_tag()
        self._init_division()
        self._init_user()
