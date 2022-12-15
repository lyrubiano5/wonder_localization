from abc import ABC, abstractmethod


class AbstractMessage(ABC):
    @abstractmethod
    def get_message(self, message):
        pass

    @abstractmethod
    def get_location(self, distance):
        pass


class Message(AbstractMessage):

    def get_location(*distances):
        """

            Args:
            distances (float): distancias entre la antena y el origen del

            mensaje
                Returns:
                    (x, y): coordenadas x, y del origen del mensaje
        """

    def get_message(*messages):
        """

        Args:
            messages (string): mensajes recibidos en cada antena

        Returns:
            message (string): mensaje original
        """

