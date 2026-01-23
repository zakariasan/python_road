from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
    """Abstract base class for data processors"""

    @abstractmethod
    def process(self, data: Any) -> str:
        """Process the data and return result string"""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate if data is appropriate for this processor"""
        pass

    def format_output(self, result: str) -> str:
        """Format the output string - can be overridden"""
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """Processor for numeric data"""

    def validate(self, data: Any) -> bool:
        """Validate numeric data"""
        try:
            for item in data:
                float(item)
            print("Validation: Numeric data verified")
            return True
        except: # noqa
            print("Validation: Numeric data Not verified")
            return False

    def process(self, data: Any) -> str:
        """Process numeric data"""
        if self.validate(data):
            total = 0
            count = 0
            for item in data:
                total = total + item
                count = count + 1

            avg = total / count
            return f"Processed {count} numeric values, sum={total}, avg={avg}"

    def format_output(self, result: str) -> str:
        """Format numeric output"""
        return f"Output: {result}"


class TextProcessor(DataProcessor):
    """Processor for text data"""

    def validate(self, data: Any) -> bool:
        """Validate text data"""
        try:
            str(data)
            print("Validation: Text data verified")
            return True
        except: # noqa
            print("Validation: Invalid text data")
            return False

    def process(self, data: Any) -> str:
        """Process text data"""
        if self.validate(data):
            char_count = 0
            for _ in data:
                char_count += 1

            cnt = 0
            in_word = False

            for ch in data:
                if ch != ' ':
                    if not in_word:
                        cnt += 1
                        in_word = True
                else:
                    in_word = False
            out = f"Processed text: {char_count} characters"
            last = f", {cnt} words"
            return out + last

    def format_output(self, result: str) -> str:
        """Format text output"""
        return f"Output: {result}"


class LogProcessor(DataProcessor):
    """Processor for log entries"""

    def validate(self, data: Any) -> bool:
        """Validate log data"""
        try:
            str(data)
            data_upper = data
            if ("ERROR" in data_upper
                    or
                    "WARN" in data_upper
                    or
                    "INFO" in data_upper
                    or
                    "DEBUG" in data_upper):
                print("Validation: Log entry verified")
                return True
            return False
        except: # noqa
            return False

    def process(self, data: Any) -> str:
        """Process log data"""
        if self.validate(data):
            if "ERROR" in data:
                level = "ERROR"
                tag = "[ALERT]"
            elif "WARN" in data:
                level = "WARN"
                tag = "[WARNING]"
            elif "INFO" in data:
                level = "INFO"
                tag = "[INFO]"
        else:
            level = "DEBUG"
            tag = "[DEBUG]"

        if ":" in data:
            parts = data.split(":", 1)
            message = parts[1].strip()
        else:
            message = data

        return f"{tag} {level} level detected: {message}"

    def format_output(self, result: str) -> str:
        """Format log output"""
        return f"Output: {result}"


def main() -> None:
    """Main function demonstrating polymorphic data processing"""
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print()
    print("Initializing Numeric Processor...")
    numeric_proc = NumericProcessor()
    data = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    result = numeric_proc.process(data)
    print(numeric_proc.format_output(result))

    print()
    print("Initializing Text Processor...")
    text_proc = TextProcessor()
    print('Processing data: "Hello Nexus World"')
    result = text_proc.process("Hello Nexus World")
    print(text_proc.format_output(result))
    print()
    print("Initializing Log Processor...")
    log_proc = LogProcessor()
    print('Processing data: "ERROR: Connection timeout"')
    result = log_proc.process("ERROR: Connection timeout")
    print(log_proc.format_output(result))

    print()
    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")

    processors: List[DataProcessor] = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]

    test_data: List[Any] = [
        [1, 2, 3],
        "Hello World!",
        "INFO: System ready"
    ]

    result_num = 1
    for processor, data in zip(processors, test_data):
        result = processor.process(data)
        print(f"Result {result_num}: {result}")
        result_num = result_num + 1

    print()
    print("Foundation systems online. Nexus ready for advanced streams.")


main()
