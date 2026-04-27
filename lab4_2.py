#=========================================================== FASADA ===========================================================
"""
1. Przygotować klasę fasady, która upraszcza operacje na plikach (zapis, odczyt, usuwanie), ukrywając niskopoziomowe operacje (otwarcie, zamknięcie).
2. Zaimplementować fasadę dla biblioteki graficznej, która zapewnia prostszy interfejs do skalowania, zmiany kolorów i kompresji obrazów.
3. Utworzyć fasadę do obsługi systemu kolejek (np. RabbitMQ, Kafka), która ułatwia wysyłanie i odbieranie wiadomości poprzez wspólny interfejs.
"""

#============================================================== 1 ==============================================================

import os

class FileFacade:
    @staticmethod
    def write(file_path: str, content: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def read(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def delete(file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)
    

#============================================================== 2 ==============================================================

class ImageScaler:
    def scale(self, filename: str, percent: int) -> str:
        return f"Scaled {filename} to {percent}%"

class ColorConverter:
    def convert(self, filename: str, color_space: str) -> str:
        return f"Converted {filename} to {color_space}"

class ImageCompressor:
    def compress(self, filename: str, level: str) -> str:
        return f"Compressed {filename} to {level}"

class GraphicsFacade:
    def __init__(self) -> None:
        self._scaler = ImageScaler()
        self._converter = ColorConverter()
        self._compressor = ImageCompressor()

    def process_web_image(self, filename: str) -> list[str]:
            return [
                self._scaler.scale(filename, 50),
                self._converter.convert(filename, "RGB"),
                self._compressor.compress(filename, "Web")
            ]
    
    
#============================================================== 3 ==============================================================


class ConnectionManager:
    def connect(self, url: str) -> None: 
        pass

    def disconnect(self) -> None: 
        pass

class ChannelManager:
    def create_channel(self) -> None: 
        pass

class QueueManager:
    def declare(self, queue_name: str) -> None: 
        pass

class Publisher:
    def publish(self, queue_name: str, message: str) -> None: 
        pass

class Consumer:
    def consume(self, queue_name: str) -> str:
        return "Message payload"

class MessageQueueFacade:
    def __init__(self, broker_url: str) -> None:
        self._conn = ConnectionManager()
        self._chan = ChannelManager()
        self._queue = QueueManager()
        self._pub = Publisher()
        self._sub = Consumer()
        
        self._conn.connect(broker_url)
        self._chan.create_channel()

    def send_message(self, queue_name: str, message: str) -> None:
        self._queue.declare(queue_name)
        self._pub.publish(queue_name, message)

    def receive_message(self, queue_name: str) -> str:
        self._queue.declare(queue_name)
        return self._sub.consume(queue_name)
        
    def close(self) -> None:
        self._conn.disconnect()
    

if __name__ == "__main__":
    FileFacade.write("test.txt", "Data")
    FileFacade.read("test.txt")
    FileFacade.delete("test.txt")

    editor = GraphicsFacade()
    editor.process_web_image("image.png")

    queue = MessageQueueFacade("amqp://localhost")
    queue.send_message("jobs", "Task 1")
    queue.receive_message("jobs")
    queue.close()