from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    """Abstract base class for data streams"""
    
    def __init__(self, stream_id: str) -> None:
        """Initialize the data stream"""
        self.stream_id = stream_id
        self.processed_count = 0
        self.total_items = 0
    
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of data - must be implemented by subclasses"""
        pass
    
    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        """Filter data based on criteria - default implementation"""
        if criteria is None:
            return data_batch
        return [item for item in data_batch if criteria in str(item)]
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return stream statistics - default implementation"""
        return {
            "stream_id": self.stream_id,
            "processed_batches": self.processed_count,
            "total_items": self.total_items
        }


class SensorStream(DataStream):
    """Stream handler for sensor data"""
    
    def __init__(self, stream_id: str) -> None:
        """Initialize sensor stream"""
        super().__init__(stream_id)
        self.total_value = 0.0
        self.min_value = float('inf')
        self.max_value = float('-inf')
    
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process sensor data batch"""
        try:
            numeric_data = [float(item) for item in data_batch if isinstance(item, (int, float))]
            
            if not numeric_data:
                return f"Sensor {self.stream_id}: No valid numeric data"
            
            batch_sum = sum(numeric_data)
            batch_avg = batch_sum / len(numeric_data)
            batch_min = min(numeric_data)
            batch_max = max(numeric_data)
            
            self.total_value = self.total_value + batch_sum
            self.total_items = self.total_items + len(numeric_data)
            self.processed_count = self.processed_count + 1
            
            if batch_min < self.min_value:
                self.min_value = batch_min
            if batch_max > self.max_value:
                self.max_value = batch_max
            
            return f"Sensor {self.stream_id}: Processed {len(numeric_data)} readings, avg={batch_avg:.2f}, range=[{batch_min:.2f}, {batch_max:.2f}]"
        
        except Exception as e:
            return f"Sensor {self.stream_id}: Error processing batch - {str(e)}"
    
    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        """Filter sensor data based on threshold"""
        if criteria is None:
            return data_batch
        
        try:
            threshold = float(criteria)
            return [item for item in data_batch if isinstance(item, (int, float)) and item > threshold]
        except:
            return super().filter_data(data_batch, criteria)
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return sensor stream statistics"""
        base_stats = super().get_stats()
        base_stats.update({
            "stream_type": "Sensor",
            "total_value": self.total_value,
            "min_reading": self.min_value if self.min_value != float('inf') else 0,
            "max_reading": self.max_value if self.max_value != float('-inf') else 0,
            "avg_reading": self.total_value / self.total_items if self.total_items > 0 else 0
        })
        return base_stats


class TransactionStream(DataStream):
    """Stream handler for transaction data"""
    
    def __init__(self, stream_id: str) -> None:
        """Initialize transaction stream"""
        super().__init__(stream_id)
        self.total_amount = 0.0
        self.transaction_count = 0
    
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transaction data batch"""
        try:
            valid_transactions = []
            batch_total = 0.0
            
            for item in data_batch:
                if isinstance(item, dict) and "amount" in item:
                    amount = float(item["amount"])
                    valid_transactions.append(item)
                    batch_total = batch_total + amount
                elif isinstance(item, (int, float)):
                    valid_transactions.append(item)
                    batch_total = batch_total + float(item)
            
            if not valid_transactions:
                return f"Transaction {self.stream_id}: No valid transactions"
            
            self.total_amount = self.total_amount + batch_total
            self.transaction_count = self.transaction_count + len(valid_transactions)
            self.total_items = self.total_items + len(valid_transactions)
            self.processed_count = self.processed_count + 1
            
            avg_transaction = batch_total / len(valid_transactions)
            
            return f"Transaction {self.stream_id}: Processed {len(valid_transactions)} transactions, total=${batch_total:.2f}, avg=${avg_transaction:.2f}"
        
        except Exception as e:
            return f"Transaction {self.stream_id}: Error processing batch - {str(e)}"
    
    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        """Filter transactions based on minimum amount"""
        if criteria is None:
            return data_batch
        
        try:
            min_amount = float(criteria)
            filtered = []
            for item in data_batch:
                if isinstance(item, dict) and "amount" in item:
                    if float(item["amount"]) >= min_amount:
                        filtered.append(item)
                elif isinstance(item, (int, float)) and float(item) >= min_amount:
                    filtered.append(item)
            return filtered
        except:
            return super().filter_data(data_batch, criteria)
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return transaction stream statistics"""
        base_stats = super().get_stats()
        base_stats.update({
            "stream_type": "Transaction",
            "total_amount": self.total_amount,
            "transaction_count": self.transaction_count,
            "avg_transaction": self.total_amount / self.transaction_count if self.transaction_count > 0 else 0
        })
        return base_stats


class EventStream(DataStream):
    """Stream handler for event data"""
    
    def __init__(self, stream_id: str) -> None:
        """Initialize event stream"""
        super().__init__(stream_id)
        self.event_types = {}
        self.critical_count = 0
    
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process event data batch"""
        try:
            valid_events = []
            critical_events = 0
            
            for item in data_batch:
                event_str = str(item)
                valid_events.append(event_str)
                
                event_upper = event_str.upper()
                if "ERROR" in event_upper or "CRITICAL" in event_upper or "ALERT" in event_upper:
                    critical_events = critical_events + 1
                
                event_type = "INFO"
                if "ERROR" in event_upper:
                    event_type = "ERROR"
                elif "WARN" in event_upper:
                    event_type = "WARN"
                elif "CRITICAL" in event_upper:
                    event_type = "CRITICAL"
                
                if event_type in self.event_types:
                    self.event_types[event_type] = self.event_types[event_type] + 1
                else:
                    self.event_types[event_type] = 1
            
            self.critical_count = self.critical_count + critical_events
            self.total_items = self.total_items + len(valid_events)
            self.processed_count = self.processed_count + 1
            
            return f"Event {self.stream_id}: Processed {len(valid_events)} events, {critical_events} critical"
        
        except Exception as e:
            return f"Event {self.stream_id}: Error processing batch - {str(e)}"
    
    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        """Filter events based on severity level"""
        if criteria is None:
            return data_batch
        
        criteria_upper = criteria.upper()
        return [item for item in data_batch if criteria_upper in str(item).upper()]
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return event stream statistics"""
        base_stats = super().get_stats()
        base_stats.update({
            "stream_type": "Event",
            "critical_events": self.critical_count,
            "event_types": str(self.event_types)
        })
        return base_stats


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
    
    def filter_all(self, data_batches: Dict[str, List[Any]], criteria: Optional[str] = None) -> Dict[str, List[Any]]:
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
    print("=== CODE NEXUS - POLYMORPHIC DATA STREAMS ===")
    
    print()
    print("Initializing Stream Processor...")
    processor = StreamProcessor()
    
    print("Creating specialized streams...")
    sensor_stream = SensorStream("SENSOR-001")
    transaction_stream = TransactionStream("TXN-001")
    event_stream = EventStream("EVENT-001")
    
    processor.add_stream(sensor_stream)
    processor.add_stream(transaction_stream)
    processor.add_stream(event_stream)
    print(f"Registered {len(processor.streams)} streams")
    
    print()
    print("=== Batch Processing Demo ===")
    
    data_batches = {
        "SENSOR-001": [23.5, 24.1, 22.8, 25.3, 23.9],
        "TXN-001": [{"amount": 99.99}, {"amount": 149.50}, {"amount": 75.25}],
        "EVENT-001": ["INFO: System started", "ERROR: Connection failed", "WARN: Low memory"]
    }
    
    print("Processing batches for all streams...")
    results = processor.process_all(data_batches)
    for result in results:
        print(result)
    
    print()
    print("=== Filtering Demo ===")
    print("Filtering sensor data (threshold > 24.0)...")
    filtered_batches = processor.filter_all(data_batches, "24.0")
    if "SENSOR-001" in filtered_batches:
        print(f"Filtered sensor data: {filtered_batches['SENSOR-001']}")
    
    print()
    print("Filtering events (ERROR level)...")
    event_batches = {"EVENT-001": data_batches["EVENT-001"]}
    filtered_events = event_stream.filter_data(event_batches["EVENT-001"], "ERROR")
    print(f"Filtered events: {filtered_events}")
    
    print()
    print("=== Stream Statistics ===")
    all_stats = processor.get_all_stats()
    for stats in all_stats:
        print(f"Stream: {stats['stream_id']} ({stats.get('stream_type', 'Unknown')})")
        print(f"  Processed batches: {stats['processed_batches']}")
        print(f"  Total items: {stats['total_items']}")
        if "avg_reading" in stats:
            print(f"  Average reading: {stats['avg_reading']:.2f}")
        if "total_amount" in stats:
            print(f"  Total amount: ${stats['total_amount']:.2f}")
        if "critical_events" in stats:
            print(f"  Critical events: {stats['critical_events']}")
    
    print()
    print("=== Polymorphic Processing Demo ===")
    print("Processing second batch through same interface...")
    
    second_batch = {
        "SENSOR-001": [26.2, 27.5, 25.8],
        "TXN-001": [250.00, 125.50, 399.99],
        "EVENT-001": ["INFO: Backup complete", "CRITICAL: Disk full", "INFO: Task finished"]
    }
    
    results = processor.process_all(second_batch)
    for result in results:
        print(result)
    
    print()
    print("Stream processing complete. Nexus systems operational.")


main()
