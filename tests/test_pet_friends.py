from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os
pf = PetFriends()
def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
def test_get_all_pets_with_valid_key(filter=''):
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(api_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
def test_add_new_pet_with_valid_data(name='Sibulba', animal_type='сфинкс',
                                     age='4', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    '''Проверяем возможность удаления питомца'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Sibulba', 'сфинкс', '4', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name='giort', animal_type='несфинкс', age='5'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")
def test_get_api_key_with_wrong_email_and_correct_password(email = invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    #проверяем запрос с валидным емаил и не невалидным паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
def test_add_pet_with_numbers_in_variable_animal_type(name='Sibulba', animal_type='34562', age='4', pet_photo='images/cat.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле порода'

def test_add_pet_with_special_characters_in_variable_animal_type(name='Sibulba', age='4',
                                                                     pet_photo='images/cat.jpg'):

        animal_type = 'Cat%@'
        symbols = '#$%^&*{}|?/><=+_~@'
        symbol = []

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, api_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

        assert status == 200
        for i in symbols:
            if i in result['animal_type']:
                symbol.append(i)
        assert symbol[0] not in result['animal_type'], 'Питомец добавлен с недопустимыми спец.символами'
def test_negative_get_api_key_for_invalid_user(email=valid_email, password=valid_password):

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, "invalid " + password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
    assert status == 403
    assert not ('key' in result)