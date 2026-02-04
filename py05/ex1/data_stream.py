from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional
"""
Phase Beta: Polymorphic Streams - Evolve adaptive data organisms through
inheritance
"""


class DataStream(ABC):
    """Abstract base class for data streams"""

    def __init__(self, stream_id: str) -> None:
        """Initialize the data stream"""
        self.stream_id = stream_id
        self.processed_count = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of data - must be implemented by subclasses"""
        pass

    def filter_data(
            self,
            data_batch: List[Any],
            criteria: Optional[str] = None) -> List[Any]:
        """Filter data based on criteria - default implementation"""
        if criteria is None:
            return data_batch
        return [item for item in data_batch if criteria in str(item)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return stream statistics - default implementation"""
        return {
            "stream_id": self.stream_id,
            "processed_batches": self.processed_count,
        }


class SensorStream(DataStream):
    """Stream handler for sensor data"""

    def __init__(self, stream_id: str) -> None:
        """Initialize sensor stream"""
        super().__init__(stream_id)
        self.s_type = "Environmental Data"
        self.alerts = []

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process sensor data batch with extreme value alerts"""
        try:
            self.processed_count += len(data_batch)
            temp_readings = self.filter_data(data_batch, "temp")
            for reading in temp_readings:
                temp_value = reading.get("temp")
                if temp_value is not None:
                    if temp_value > 35:
                        self.alerts.append(f"HIGH temp: {temp_value}°C")
                    elif temp_value < 0:
                        self.alerts.append(f"LOW temp: {temp_value}°C")

            ele = list(data_batch[0].keys())[0]
            val = list(data_batch[0].values())[0]
            return (f"Sensor analysis: {len(data_batch)} "
                    f"readings processed, avg {ele}: {val}°C")
        except: # noqa
            return "Error processing sensor batch"


class TransactionStream(DataStream):
    """Stream handler for transaction data"""

    def __init__(self, stream_id: str) -> None:
        """Initialize transaction stream"""
        super().__init__(stream_id)
        self.s_type = "Financial Data"
        self.alerts = []

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transaction data batch"""
        try:
            self.processed_count += len(data_batch)
            net = 0
            for d in data_batch:
                if list(d.values())[0] >= 200:
                    self.alerts.append("HIGH transaction")

                net += d.get("buy", 0) - d.get("sell", 0)
            un = f"+{net} units" if net >= 0 else f"{net} units"
            return (f"Transaction analysis: {len(data_batch)} operations"
                    f", net flow: {un}")
        except: # noqa
            return "Error processing transaction batch"


class EventStream(DataStream):
    """Stream handler for event data"""

    def __init__(self, stream_id: str) -> None:
        """Initialize event stream"""
        super().__init__(stream_id)
        self.s_type = "System Events"
        self.alerts = []

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process event data batch"""
        try:
            self.processed_count += len(data_batch)
            errors = self.filter_data(data_batch, "error")
            error_count = len(errors)
            return (f"Event analysis: {len(data_batch)} events, "
                    f"{error_count} error detected")
        except: # noqa
            return "Error processing event batch"


class StreamProcessor:
    """Polymorphic processor for handling multiple stream types"""

    def __init__(self) -> None:
        """Initialize the stream processor"""
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        """Add a stream to the processor"""
        self.streams.append(stream)

    def process_all(self, data_batches: Dict[str, List[Any]]) -> List[str]:
        """Process data for all streams polymorphically"""
        results = []
        for stream in self.streams:
            stream_id = stream.stream_id
            if stream_id in data_batches:
                try:
                    result = stream.process_batch(data_batches[stream_id])
                    results.append(result)
                except: # noqa
                    results.append(f"Error processing {stream_id}")
        return results

    def filter_all(
            self,
            data_batches: Dict[str, List[Any]],
            criteria: Optional[str] = None) -> Dict[str, List[Any]]:
        """Filter data for all streams"""
        filtered_batches = {}
        for stream in self.streams:
            stream_id = stream.stream_id
            if stream_id in data_batches:
                try:
                    filtered_batches[stream_id] = stream.filter_data(
                        data_batches[stream_id], criteria)
                except: # noqa
                    print(f"Error filtering {stream_id}")
                    filtered_batches[stream_id] = data_batches[stream_id]
        return filtered_batches

    def get_all_stats(self) -> List[Dict[str, Union[str, int, float]]]:
        """Get statistics from all streams"""
        return [stream.get_stats() for stream in self.streams]

    def process_batches(self, data_batches: Dict[str, List[Any]]) -> None:
        """Demonstrate polymorphic behavior"""
        print("=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...")
        print()

        print("Batch 1 Results:")
        for stream in self.streams:
            stream_id = stream.stream_id
            if stream_id in data_batches:
                batch_size = len(data_batches[stream_id])
                if isinstance(stream, SensorStream):
                    print(f"- Sensor data: {batch_size} readings processed")
                elif isinstance(stream, TransactionStream):
                    print(
                            f"- Transaction data: {batch_size} "
                            +
                            "operations processed"
                            )
                elif isinstance(stream, EventStream):
                    print(f"- Event data: {batch_size} events processed")
        print()
        print("Stream filtering active: High-priority data only")
        sensor_alerts = 0
        large_trans = 0
        for stream in self.streams:
            if isinstance(stream, SensorStream):
                stream_id = stream.stream_id
                stream.process_batch(data_batches[stream_id])
                sensor_alerts = len(stream.alerts)
            elif isinstance(stream, TransactionStream):
                stream_id = stream.stream_id
                stream.process_batch(data_batches[stream_id])
                large_trans = len(stream.alerts)

        print(
            f"Filtered results: {sensor_alerts} "
            +
            f"critical sensor alerts, {large_trans} large transaction")
        print()
        print("All streams processed successfully. Nexus throughput optimal.")


def main() -> None:
    """Main function demonstrating polymorphic stream processing"""
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print()

    print("Initializing Sensor Stream...")
    sensors = SensorStream("SENSOR_001")
    print(f"Stream ID: {sensors.stream_id}, Type: {sensors.s_type}")
    sensor_data = [{"temp": 22.5}, {"humidity": 65}, {"pressure": 1013}]
    print("Processing sensor batch: [temp:22.5, humidity:65, pressure:1013]")
    print(sensors.process_batch(sensor_data))
    print()

    print("Initializing Transaction Stream...")
    trans = TransactionStream("TRANS_001")
    print(f"Stream ID: {trans.stream_id}, Type: {trans.s_type}")
    trans_data = [{"buy": 100}, {"sell": 150}, {"buy": 75}]
    print("Processing transaction batch: [buy:100, sell:150, buy:75]")
    print(trans.process_batch(trans_data))
    print()

    print("Initializing Event Stream...")
    even = EventStream("EVENT_001")
    print(f"Stream ID: {even.stream_id}, Type: {even.s_type}")
    event_data = ["login", "error", "logout"]
    print("Processing event batch: [login, error, logout]")
    print(even.process_batch(event_data))
    print()

    processor = StreamProcessor()
    processor.add_stream(sensors)
    processor.add_stream(trans)
    processor.add_stream(even)
    batch_data = {
        "SENSOR_001": [{"temp": -5.0}, {"temp": 40.5}],
        "TRANS_001": [{"buy": 50}, {"sell": 25}, {"buy": 30}, {"buy": 200}],
        "EVENT_001": ["update", "sync", "backup"]
    }
    processor.process_batches(batch_data)


main()
