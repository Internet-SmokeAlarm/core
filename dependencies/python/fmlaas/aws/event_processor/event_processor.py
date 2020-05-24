from abc import abstractmethod


class EventProcessor:

    @abstractmethod
    def process_event(self, json_data):
        """
        Process an event.

        :param json_data: dict. Event data that needs to be processed
        """
        raise NotImplementedError("process_event() not implemented")
