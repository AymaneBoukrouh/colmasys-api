from tests.utils.user import add_test_student
from tests.utils.class_ import add_test_class, get_class_by_filters
from colmasys.models import Account
import sqlalchemy
import faker
import random

async def create_test_data():
    fake = faker.Faker()

    ###############
    ### Classes ###
    ###############

    classes = (
        await add_test_class(major='AP', year=1, group=1, academic_year='2020/2021'),
        await add_test_class(major='AP', year=1, group=2, academic_year='2020/2021'),
        await add_test_class(major='AP', year=1, group=3, academic_year='2020/2021'),
        await add_test_class(major='AP', year=1, group=4, academic_year='2020/2021'),
        await add_test_class(major='GC', year=1, group=1, academic_year='2020/2021'),
        await add_test_class(major='AP', year=2, group=1, academic_year='2020/2021'),
        await add_test_class(major='AP', year=2, group=2, academic_year='2020/2021'),
        await add_test_class(major='GC', year=2, group=1, academic_year='2020/2021'),
        await add_test_class(major='IIR', year=3, group=1, academic_year='2020/2021'),
        await add_test_class(major='IIR', year=3, group=2, academic_year='2020/2021'),
        await add_test_class(major='GC', year=3, group=1, academic_year='2020/2021'),
        await add_test_class(major='IFA', year=3, group=1, academic_year='2020/2021')
    )

    ################
    ### Students ###
    ################

    for class_ in classes:
        if (class_.major != 'IIR') and (class_.group != 2):
            for _ in range(random.randint(20, 35)):
                gender = random.choice(['M', 'F'])
                if gender == 'M':
                    firstname = fake.first_name_male()
                    lastname = fake.last_name_male()
                    gender = Account.Gender.male
                else:
                    firstname = fake.first_name_female()
                    lastname = fake.last_name_female()
                    gender = Account.Gender.female

                try:
                    await add_test_student(
                        username = f'T{random.randint(10000, 99999)}', firstname = firstname, lastname = lastname, email = f'{lastname.upper()}_{firstname.upper()}@emsi-edu.ma',
                        birthdate = f'{fake.date(fake.date(pattern="%d/%m"))}/{random.randint(1999, 2004)}', gender = gender, class_ = class_
                    )
                
                except sqlalchemy.exc.IntegrityError:
                    pass # ignore duplicate entries
                except ValueError:
                    pass # ignore invalid date (29th of february in non-leap year)

    
    class_3iir_g2_20202021 = await get_class_by_filters(major='IIR', year=3, group=2, academic_year='2021/2022')

    students_3iir_g2_20202021 = (
        ('Aymane', 'Boukrouh', 'M'), ('Achraf Zakaria', 'El Assali', 'M'), ('Maissae', 'Amzghar', 'F'),
        ('Safae', 'Berrouhou', 'F'), ('Hicham', 'Bouhamid', 'M'), ('Zakaria', 'El Hajri', 'M'),
        ('Samir', 'El Asri', 'M'), ('Taha', 'Hayani', 'M'), ('Farah', 'Matallaoui', 'F'),
        ('Yousra', 'Tribak', 'F'), ('Abdekarim', 'Yemlahi', 'M'), ('Hamza', 'Bakhti', 'M'),
        ('Chaimae', 'Loukili', 'F'), ('Mehdi', 'El Houari', 'M'), ('Lina', 'Mcaouri Fatihi', 'F')
    )

    for firstname, lastname, gender in students_3iir_g2_20202021:
        if gender == 'M':
            gender = Account.Gender.male
        else:
            gender = Account.Gender.female
 
        try:
            await add_test_student(
                username = f'T{random.randint(10000, 99999)}', firstname = firstname, lastname = lastname, email = f'{lastname.upper()}_{firstname.upper()}@emsi-edu.ma',
                birthdate = f'{fake.date(fake.date(pattern="%d/%m"))}/{random.randint(1999, 2004)}', gender = gender, class_ = class_3iir_g2_20202021
            )
                
        except sqlalchemy.exc.IntegrityError:
            pass # ignore duplicate entries
        except ValueError:
            pass # ignore invalid date (29th of february in non-leap year)
