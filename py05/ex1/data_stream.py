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

    def __init__(self, stream_id: str, s_type: str) -> None:
        """Initialize sensor stream"""
        super().__init__(stream_id)
        self.s_type = s_type

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process sensor data batch"""
        ele = list(data_batch[0].keys())[0]
        val = list(data_batch[0].values())[0]
        return (f"Sensor analysis: {len(data_batch)} "
                +
                f"readings processed, avg {ele}: {val}°C")


class TransactionStream(DataStream):
    """Stream handler for transaction data"""

    def __init__(self, stream_id: str) -> None:
        """Initialize transaction stream"""
        super().__init__(stream_id)
        self.type = "Financial Data"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transaction data batch"""
        self.processed_count += len(data_batch)
        return f"Transaction analysis: {len(data_batch)} operations"


class EventStream(DataStream):
    """Stream handler for event data"""

    def __init__(self, stream_id: str) -> None:
        """Initialize event stream"""
        super().__init__(stream_id)
        self.type = "System Events"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process event data batch"""
        return f"Event {self.stream_id}: Processed {len(valid_events)} events, {critical_events} critical"
        
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
                result = stream.process_batch(data_batches[stream_id])
                results.append(result)
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
                filtered_batches[stream_id] = stream.filter_data(data_batches[stream_id], criteria)
        return filtered_batches

    def get_all_stats(self) -> List[Dict[str, Union[str, int, float]]]:
        """Get statistics from all streams"""
        return [stream.get_stats() for stream in self.streams]


def main() -> None:
    """Main function demonstrating polymorphic stream processing"""
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    print()
    print("Initializing Sensor Stream...")
    sensors = SensorStream("SENSOR-001", "Environmental Data")
    data = [{"temp": 22.5}, {"humidity": 65}, {"pressure": 1013}]
    res = "["
    for item in data:
        for key, value in item.items():
            res += f"{key}:{value}, "
    res = res[:-2] + "]"
    print(f"Processing sensor batch: {res}")
    print(f"Stream ID: {sensors.stream_id}, Type: {sensors.s_type}")
    print(sensors.process_batch(data))
    print()

    print("Initializing Transaction Stream...")
    trans = TransactionStream("TRANS_001", "Financial Data")

main()
