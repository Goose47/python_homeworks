import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    current_year = dt.date.today().year
    friends = get_friends(user_id=user_id, fields=['bdate'])

    ages = []

    for friend in friends.items:
        try:
            date = dt.datetime.strptime(friend['bdate'], '%d.%m.%Y')
            age = current_year - date.year
            ages.append(age)
        except ValueError:
            pass
        except KeyError:
            pass

    if len(ages) == 0:
        return None

    return statistics.mean(ages)
