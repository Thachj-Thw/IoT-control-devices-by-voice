class AutoSetup:
    def __init__(self, client, topics):
        self._client = client
        self._topics = topics
        self._methods = {
            "ON": self._on_turn_on,
            "OFF": self._on_turn_off,
            "CHECK": self._on_check
            }
        self._client.on_message(self._on_message)
        for topic in self._topics.keys():
            self._client.subscribe(topic)

    def _on_message(self, topic, message, *args, **kwargs):
        try:
            msg = self._methods[message.decode("utf-8")](self._topics[topic.decode("utf-8")])
            self._client.publish(msg)
        except KeyError:
            self._client.publish("ERROR")

    def _on_turn_on(self, pin):
        value = pin.value()
        if value == 0:
            pin.value(1)
            return "SUCCESS"
        return "IS TURN ON"

    def _on_turn_off(self, pin):
        value = pin.value()
        if value == 1:
            pin.value(0)
            return "SUCCESS"
        return "IS TURN OFF"

    def _on_check(self, pin):
        value = pin.value()
        if value == 0:
            return "OFF"
        return "ON"
