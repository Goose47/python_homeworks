import dataclasses
import math
import time
import typing as tp

from vkapi import session, config
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    access_token = config.VK_CONFIG['access_token']
    v = config.VK_CONFIG['version']

    query = f'/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&count={count}&offset={offset}&v={v}'
    response = session.get(query).json()['response']

    friends_response = FriendsResponse(response['count'], response['items'])

    return friends_response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    access_token = config.VK_CONFIG['access_token']
    v = config.VK_CONFIG['version']

    if not count:
        count = 0

    if target_uid:
        query = f'/friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uid={target_uid}&order={order}&count={count}&offset={offset}&v={v}'
        return session.get(query).json()['response']

    friends_response = []
    requests_number = int(math.ceil(len(target_uids) / 100))
    for i in range(requests_number):
        query = f'/friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uids={target_uids}&order={order}&count={count}&offset={100 * i}&v={v}'
        response = session.get(query).json()['response']

        for friend in response:
            element = {'id': friend['id'], 'common_friends': friend['common_friends'],
                       'common_count': friend['common_count']}
            friends_response.append(MutualFriends(element))
        if i % 3 == 0:
            time.sleep(1)

    return friends_response
