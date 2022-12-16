import ast
from datetime import datetime
from typing import List, Dict

import sympy as sym

from abc import ABC, abstractmethod
from .models import Antenna, Message


class AbstractMessage(ABC):

    @abstractmethod
    def get_message(self, distance):
        """
            Args: messages (string):
            mensajes recibidos en cada antena
            Returns: message (string):
            mensaje original
        """

    @abstractmethod
    def create_message(self, data_):
        """
        :param data_: Dict
        :return:
        """


class AbstractCalculateLocalization(ABC):
    @abstractmethod
    def get_location(self, distance):
        """
        Args:
            distances (float):
            distancias entre la antena y el origen del
        mensaje
            Returns:
            (x, y):
            coordenadas x, y del origen del mensaje
        """


class MassiveMessageReceived(AbstractMessage):

    def get_message(self, messages: List):
        len_message = len(messages[0]['message'])
        complete_message = ["" for x in range(len_message)]
        for data_ in messages:
            self.create_message(data_=data_)
            message = data_['message']
            for i in range(len_message):
                if message[i] != "":
                    complete_message[i] = message[i]
        return ' '.join(complete_message)

    def create_message(self, data_: Dict):
        now = datetime.now()
        name = data_['name']
        antenna = Antenna.objects.get(name=name)
        Message.objects.create(
            antenna=antenna,
            message=data_['message'],
            distance=data_['distance'],
            created_at=now
        )


class MessageReceivedByPart(AbstractMessage):

    def get_first_messsage(self, name: str):
        values = Message.objects.filter(
            antenna__name=name
        ).values(
            'message',
            'created_at__date'
        ).order_by('created_at')
        if not values.exists():
            return None
        values = values.last()
        return ast.literal_eval(values.get('message')), values.get('created_at__date')

    def get_messages(self, name: str, message_created: datetime.date):
        antennas = Antenna.objects.exclude(
            name=name
        )
        result = list()
        for antenna in antennas:
            values = Message.objects.filter(
                antenna=antenna,
                created_at__date=message_created
            ).values(
                'message'
            ).order_by('created_at')
            if not values.exists():
                return None
            values = values.last()
            result.append(ast.literal_eval(values.get('message')))
        return result

    def get_message(self, messages: List):
        antenna_name = messages[0]['name']
        first_message, message_created = \
            self.get_first_messsage(name=antenna_name)
        if first_message is None:
            return ""
        messages = self.get_messages(
            name=antenna_name,
            message_created=message_created
        )
        if messages is None:
            return ' '.join(first_message)
        len_message = len(first_message)
        complete_message = ["" for _ in range(len_message)]
        messages.append(first_message)
        for message in messages:
            for i in range(len_message):
                if message[i] != "":
                    complete_message[i] = message[i]
        return ' '.join(complete_message)

    def create_message(self, data_: Dict):
        now = datetime.now()
        name = data_['name']
        antenna = Antenna.objects.get(name=name)
        Message.objects.create(
            antenna=antenna,
            message=data_['message'],
            distance=data_['distance'],
            created_at=now
        )


class CalculateLocalization:

    def get_coordinates(self, antennas_data: List):
        coordinates_data = list()
        for data_ in antennas_data:
            new_data = dict()
            new_data['d'] = data_['distance']
            name = data_['name']
            antenna = Antenna.objects.get(name=name)
            new_data['x'] = antenna.x_localization
            new_data['y'] = antenna.y_localization
            coordinates_data.append(new_data)
        return coordinates_data

    def get_intersection(
            self,
            first_point: Dict,
            second_point: Dict
    ):
        x1 = first_point['x']
        y1 = first_point['y']
        d1 = first_point['d']
        x2 = second_point['x']
        y2 = second_point['y']
        d2 = second_point['d']
        x, y = sym.symbols('x,y')
        eq1 = sym.Eq((x - x1) ** 2 + (y - y1) ** 2, d1)
        eq2 = sym.Eq((x - x2) ** 2 + (y - y2) ** 2, d2)
        result = sym.solve([eq1, eq2], (x, y))
        return result

    def get_common_intersections(
            self,
            first_coordinates: List,
            second_coordinates: List
    ):
            new_coordinates = list()
            for i in first_coordinates:
                for j in second_coordinates:
                    if j == j:
                        new_coordinates.append(i)
            return new_coordinates

    def get_coordinates_from_points(
            self,
            first_point: Dict,
            second_point: Dict,
            third_point: Dict
    ):
        first_i = self.get_intersection(
            first_point, second_point
        )
        second_i = self.get_intersection(
            first_point, third_point
        )
        user_c = self.get_common_intersections(
            first_i, second_i
        )
        third_intersection = self.get_intersection(
            second_point, third_point
        )
        user_c = self.get_common_intersections(
            user_c,
            third_intersection
        )
        return user_c[0]


class CalculateMassiveLocalization(
    AbstractCalculateLocalization,
    CalculateLocalization
):

    def get_location(self, distances: List):
        coordinates = self.get_coordinates(distances)
        first_point = coordinates[0]
        second_point = coordinates[1]
        third_point = coordinates[2]
        return self.get_coordinates_from_points(
            first_point=first_point,
            second_point=second_point,
            third_point=third_point
        )


class CalculateLocalizationPart(
    AbstractCalculateLocalization,
    CalculateLocalization
):

    def get_first_point(self, name: str):
        values = Message.objects.filter(
            antenna__name=name
        ).values(
            'antenna__x_localization',
            'antenna__y_localization',
            'distance',
            'created_at__date'
        ).order_by('created_at')
        if not values.exists():
            return None
        values = values.last()
        return dict(
            d=values.get('distance'),
            x=values.get('antenna__x_localization'),
            y=values.get('antenna__y_localization'),
            created_at=values.get('created_at__date')
        )

    def get_two_points(
            self,
            name: str,
            message_created: datetime.date
    ):
        antennas = Antenna.objects.exclude(
            name=name
        )
        result = list()
        for antenna in antennas:
            values = Message.objects.filter(
                antenna=antenna,
                created_at__date=message_created
            ).values(
                'antenna__x_localization',
                'antenna__y_localization',
                'distance'
            ).order_by('created_at')
            if not values.exists():
                return None
            values = values.last()
            dict_values = dict(
                d=values.get('distance'),
                x=values.get('antenna__x_localization'),
                y=values.get('antenna__y_localization')
            )
            result.append(dict_values)
        return result

    def get_location(self, distances: List):
        antenna_name = distances[0]['name']
        first_point = self.get_first_point(name=antenna_name)
        if first_point is None:
            return 0, 0
        message_created = first_point.pop('created_at')
        two_points = self.get_two_points(
            name=antenna_name,
            message_created=message_created
        )
        if two_points is None:
            return 0, 0
        second_point = two_points[0]
        third_point = two_points[1]
        return self.get_coordinates_from_points(
            first_point=first_point,
            second_point=second_point,
            third_point=third_point
        )
