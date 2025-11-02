"""End-to-end tests for splurge-tabular package.

These tests validate complete workflows and data processing pipelines
from start to finish, ensuring the package works correctly in real-world scenarios.
"""

import json
import tempfile
from pathlib import Path

from splurge_tabular import (
    SplurgeTabularError,
    SplurgeTabularLookupError,
    SplurgeTabularTypeError,
    SplurgeTabularValueError,
    StreamingTabularDataModel,
    StreamingTabularDataProtocol,
    TabularDataModel,
    TabularDataProtocol,
    ensure_minimum_columns,
    normalize_rows,
    process_headers,
)
from splurge_tabular._vendor.splurge_typer.data_type import DataType


class TestEndToEndWorkflows:
    """Test complete data processing workflows."""

    def test_csv_file_processing_pipeline(self) -> None:
        """Test complete CSV file processing from file to processed data."""
        # Create test CSV data
        csv_data = """name,age,city
John,25,New York
Jane,30,London
Bob,35,Paris"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_data)
            csv_path = f.name

        try:
            # Process file through complete pipeline
            result = Path(csv_path).read_text()

            # Parse CSV (simplified parsing for test)
            lines = result.split("\n")
            headers = lines[0].split(",")
            rows = [line.split(",") for line in lines[1:] if line.strip()]

            # Process headers
            processed_header_data, _column_names = process_headers([headers], header_rows=1)
            # Normalize rows
            normalized_rows = normalize_rows(rows, skip_empty_rows=True)

            # Ensure minimum columns
            ensure_minimum_columns(normalized_rows, 2)

            # Create data model
            model = TabularDataModel([processed_header_data[0]] + normalized_rows)
            # Validate final result
            assert len(model.column_names) == 3
            assert model.row_count == 3
            assert model.column_names == ["name", "age", "city"]
            assert list(model)[0] == ["John", "25", "New York"]

        finally:
            Path(csv_path).unlink()

    def test_json_file_processing_pipeline(self) -> None:
        """Test complete JSON file processing pipeline."""
        json_data = [
            {"name": "John", "age": 25, "city": "New York"},
            {"name": "Jane", "age": 30, "city": "London"},
            {"name": "Bob", "age": 35, "city": "Paris"},
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(json_data, f)
            json_path = f.name

        try:
            # Read and parse JSON
            result = json.loads(Path(json_path).read_text())

            # Convert to tabular format
            if isinstance(result, list) and result:
                headers = list(result[0].keys())
                rows = [[str(item.get(h, "")) for h in headers] for item in result]

                # Process through pipeline
                processed_header_data, column_names = process_headers([headers], header_rows=1)
                normalized_rows = normalize_rows(rows, skip_empty_rows=True)
                ensure_minimum_columns(normalized_rows, 2)

                model = TabularDataModel([processed_header_data[0]] + normalized_rows)

                assert len(model.column_names) == 3
                assert model.row_count == 3
                assert model.column_names == ["name", "age", "city"]

        finally:
            Path(json_path).unlink()

    def test_large_dataset_streaming_processing(self) -> None:
        """Test processing of large datasets using streaming model."""
        # Create large dataset
        headers = ["col1", "col2", "col3", "col4", "col5"]
        large_rows = [
            [f"row{i}_val{j}" for j in range(5)]
            for i in range(1000)  # 1000 rows
        ]

        # Process with streaming model
        data_stream = iter([[headers] + large_rows])
        streaming_model = StreamingTabularDataModel(data_stream)

        # Validate streaming iteration
        row_count = 0
        for row in streaming_model:
            assert len(row) == 5
            row_count += 1

        assert row_count == 1000

        # Test dict iteration
        # Create new streaming model for dict iteration
        data_stream2 = iter([[headers] + large_rows])
        streaming_model2 = StreamingTabularDataModel(data_stream2)
        dict_count = 0
        for row_dict in streaming_model2.iter_rows():
            assert isinstance(row_dict, dict)
            assert set(row_dict.keys()) == set(headers)
            dict_count += 1

        assert dict_count == 1000

    def test_error_handling_in_complete_workflow(self) -> None:
        """Test error handling in complete data processing workflow."""

        # Test minimum columns requirement - this doesn't raise, it pads
        single_column_row = ["a"]
        padded_row = ensure_minimum_columns(single_column_row, 2)
        assert len(padded_row) == 2

    def test_typed_view_complete_workflow(self) -> None:
        """Test complete typed view workflow from raw data to typed access."""
        # Raw data with mixed types
        raw_data = [
            ["Name", "Age", "Salary", "Active"],
            ["Alice", "28", "75000.50", "true"],
            ["Bob", "35", "82000", "false"],
        ]

        # Create model and convert to typed
        model = TabularDataModel(raw_data)
        typed_model = model.to_typed()

        # Verify type inference
        assert typed_model.column_type("Age") == DataType.INTEGER
        assert typed_model.column_type("Salary") == DataType.FLOAT
        assert typed_model.column_type("Active") == DataType.BOOLEAN

        # Verify typed access
        for row in typed_model.iter_rows():
            assert isinstance(row["Age"], int)
            assert isinstance(row["Salary"], float)
            assert isinstance(row["Active"], bool)

    def test_multiple_header_rows_workflow(self) -> None:
        """Test processing data with multiple header rows."""
        data = [
            ["Personal Info", "", "Employment", ""],
            ["Name", "Age", "Company", "Salary"],
            ["Alice", "28", "Tech Corp", "75000"],
        ]

        model = TabularDataModel(data, header_rows=2)
        # Multiple header rows are merged with underscores
        assert model.column_names == ["Personal Info_Name", "Age", "Employment_Company", "Salary"]
        assert model.row_count == 1
        # Verify merged headers were processed correctly
        assert model.row(0) == {
            "Personal Info_Name": "Alice",
            "Age": "28",
            "Employment_Company": "Tech Corp",
            "Salary": "75000",
        }

    def test_empty_row_handling_workflow(self) -> None:
        """Test empty row handling in complete workflow."""
        data = [
            ["Name", "Age"],
            ["Alice", "28"],
            ["", ""],  # Empty row
            ["Bob", "35"],
        ]

        # Test skipping empty rows
        model_skip = TabularDataModel(data, skip_empty_rows=True)
        assert model_skip.row_count == 2

        # Test preserving empty rows
        model_keep = TabularDataModel(data, skip_empty_rows=False)
        assert model_keep.row_count == 3

    def test_comprehensive_exception_handling_workflow(self) -> None:
        """Test exception handling in complete workflows."""
        # Test type errors
        try:
            TabularDataModel("not a list")  # type: ignore[arg-type]
        except SplurgeTabularTypeError as e:
            assert hasattr(e, "details")
            assert e.details.get("param") == "data"

        # Test value errors
        try:
            TabularDataModel([])
        except SplurgeTabularValueError as e:
            assert e.details.get("param") == "data"

        # Test lookup errors
        model = TabularDataModel([["Name"], ["Alice"]])
        try:
            model.column_index("Missing")
        except SplurgeTabularLookupError as e:
            assert "name" in e.details or "column" in e.details

    def test_chunked_streaming_workflow(self) -> None:
        """Test streaming model with multiple chunks."""

        def create_chunked_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
            yield [["Charlie", "22"], ["Diana", "31"]]
            yield [["Eve", "29"]]

        streaming_model = StreamingTabularDataModel(create_chunked_stream())

        rows = list(streaming_model)
        assert len(rows) == 5
        assert rows[0] == ["Alice", "28"]
        assert rows[-1] == ["Eve", "29"]

    def test_stream_reset_workflow(self) -> None:
        """Test resetting stream buffer and re-reading with new iterator."""

        # Create a stream generator function that can be called multiple times
        def create_stream():
            yield [["name", "age"], ["Alice", "28"], ["Bob", "35"]]

        # First read
        model1 = StreamingTabularDataModel(create_stream())
        first_read = list(model1)
        assert len(first_read) == 2

        # Reset clears buffer and resets state, but requires new iterator to re-read
        model1.reset_stream()
        assert len(model1._buffer) == 0  # Buffer cleared
        assert not model1._is_initialized  # State reset

        # Create new model with new iterator to simulate re-reading
        model2 = StreamingTabularDataModel(create_stream())
        second_read = list(model2)
        assert first_read == second_read

    def test_protocol_compliance_workflow(self) -> None:
        """Test that models correctly implement protocols."""
        data = [["Name", "Age"], ["Alice", "28"]]

        # Test TabularDataModel protocol compliance
        memory_model = TabularDataModel(data)
        assert isinstance(memory_model, TabularDataProtocol)

        # Test StreamingTabularDataModel protocol compliance
        streaming_model = StreamingTabularDataModel(iter([data]))
        assert isinstance(streaming_model, StreamingTabularDataProtocol)

        # Test protocol-based duck typing
        def process_tabular_data(model: TabularDataProtocol) -> list[str]:
            return model.column_names

        assert process_tabular_data(memory_model) == ["Name", "Age"]

    def test_unicode_data_workflow(self) -> None:
        """Test processing data with Unicode characters."""
        data = [
            ["姓名", "年齢", "都市"],  # Chinese column names
            ["アリス", "28", "東京"],  # Japanese data
            ["Боб", "35", "Москва"],  # Cyrillic data
        ]

        model = TabularDataModel(data)
        assert model.column_names == ["姓名", "年齢", "都市"]
        assert model.cell_value("姓名", 0) == "アリス"

    def test_type_inference_complete_workflow(self) -> None:
        """Test complete type inference workflow."""
        # Data with various types
        data = [
            ["ID", "Name", "Age", "Salary", "Active", "Date"],
            ["1", "Alice", "28", "75000.50", "true", "2024-01-01"],
            ["2", "Bob", "35", "82000", "false", "2024-02-15"],
        ]

        model = TabularDataModel(data)
        typed = model.to_typed()

        # Verify inferred types
        assert typed.column_type("ID") == DataType.INTEGER
        assert typed.column_type("Name") == DataType.STRING
        assert typed.column_type("Age") == DataType.INTEGER
        assert typed.column_type("Salary") == DataType.FLOAT
        assert typed.column_type("Active") == DataType.BOOLEAN
        # Date is inferred as DATE type
        assert typed.column_type("Date") == DataType.DATE

    def test_column_access_patterns_workflow(self) -> None:
        """Test various column access patterns in workflow."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        # Test column index lookup
        assert model.column_index("Name") == 0
        assert model.column_index("Age") == 1

        # Test column values
        names = model.column_values("Name")
        assert names == ["Alice", "Bob"]

        # Test cell value
        assert model.cell_value("Age", 0) == "28"

        # Test row access methods
        row_dict = model.row(0)
        assert row_dict == {"Name": "Alice", "Age": "28"}

        row_list = model.row_as_list(0)
        assert row_list == ["Alice", "28"]

        row_tuple = model.row_as_tuple(0)
        assert row_tuple == ("Alice", "28")

    def test_memory_vs_streaming_model_comparison(self) -> None:
        """Compare memory and streaming models for the same data."""
        headers = ["name", "value", "category"]
        rows = [
            ["item1", "100", "A"],
            ["item2", "200", "B"],
            ["item3", "300", "A"],
            ["item4", "400", "C"],
        ]

        # Create both models
        memory_model = TabularDataModel([headers] + rows)
        data_stream = iter([[headers] + rows])
        streaming_model = StreamingTabularDataModel(data_stream)

        # Compare basic properties
        assert len(memory_model.column_names) == len(streaming_model.column_names)
        assert memory_model.column_names == streaming_model.column_names

        # Compare row counts
        memory_rows = list(memory_model)
        streaming_rows = list(streaming_model)

        assert len(memory_rows) == len(streaming_rows)
        for mem_row, stream_row in zip(memory_rows, streaming_rows, strict=False):
            assert mem_row == stream_row

        # Test dict iteration consistency
        memory_dicts = list(memory_model.iter_rows())
        # Create new streaming model for dict iteration
        data_stream2 = iter([[headers] + rows])
        streaming_model2 = StreamingTabularDataModel(data_stream2)
        streaming_dicts = list(streaming_model2.iter_rows())

        assert len(memory_dicts) == len(streaming_dicts)
        for mem_dict, stream_dict in zip(memory_dicts, streaming_dicts, strict=False):
            assert mem_dict == stream_dict

    def test_data_transformation_pipeline(self) -> None:
        """Test complete data transformation pipeline."""
        # Start with raw data
        raw_data = [
            ["Name", "Age", "City"],
            ["john doe", "25", "new york"],
            ["jane smith", "30", "london"],
            ["bob johnson", "", "paris"],  # Missing age
        ]

        headers = [h.lower() for h in raw_data[0]]
        rows = raw_data[1:]

        # Process through normalization
        normalized_rows = normalize_rows(rows, skip_empty_rows=True)

        # Fill missing values
        for row in normalized_rows:
            if not row[1]:  # Empty age
                row[1] = "0"

        # Validate and create model
        ensure_minimum_columns(normalized_rows, 2)

        model = TabularDataModel([headers] + normalized_rows)

        # Verify transformations
        assert model.column_names == ["name", "age", "city"]
        assert model.row_count == 3
        rows_list = list(model)
        assert rows_list[2][1] == "0"  # Missing age filled

    def test_file_format_conversion_workflow(self) -> None:
        """Test converting between different file formats."""
        # Start with CSV-like data
        csv_data = """product,price,category
Widget A,19.99,Electronics
Widget B,29.99,Tools
Widget C,9.99,Books"""

        # Parse CSV
        lines = csv_data.strip().split("\n")
        headers = lines[0].split(",")
        rows = [line.split(",") for line in lines[1:]]

        # Create model
        model = TabularDataModel([headers] + rows)

        # Convert to JSON format
        json_data = []
        for row_dict in model.iter_rows():
            # Convert price to float
            row_dict["price"] = float(row_dict["price"])
            json_data.append(row_dict)

        # Validate JSON structure
        assert len(json_data) == 3
        assert json_data[0]["product"] == "Widget A"
        assert json_data[0]["price"] == 19.99
        assert json_data[0]["category"] == "Electronics"

    def test_batch_processing_workflow(self) -> None:
        """Test processing multiple files in batch."""
        # Create multiple test files
        test_files = []
        base_data = [
            ["id", "value"],
            ["1", "100"],
            ["2", "200"],
        ]

        for i in range(3):
            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
                # Modify data slightly for each file
                modified_rows = base_data.copy()
                modified_rows[1][1] = str(100 * (i + 1))  # Different values
                modified_rows[2][1] = str(200 * (i + 1))

                for row in modified_rows:
                    f.write(",".join(row) + "\n")

                test_files.append(f.name)

        try:
            # Process all files
            results = []
            for file_path in test_files:
                content = Path(file_path).read_text()

                lines = content.strip().split("\n")
                headers = lines[0].split(",")
                rows = [line.split(",") for line in lines[1:]]

                model = TabularDataModel([headers] + rows)
                results.append(model)

            # Validate batch results
            assert len(results) == 3
            for i, model in enumerate(results):
                assert len(list(model)) == 2
                # Check that values were modified correctly
                expected_value1 = str(100 * (i + 1))
                expected_value2 = str(200 * (i + 1))
                rows_list = list(model)
                assert rows_list[0][1] == expected_value1
                assert rows_list[1][1] == expected_value2

        finally:
            # Clean up
            for file_path in test_files:
                Path(file_path).unlink()


class TestPerformanceScenarios:
    """Test performance characteristics and large data handling."""

    def test_large_file_processing_memory_usage(self) -> None:
        """Test memory usage with large datasets."""
        # Create moderately large dataset
        headers = [f"col_{i}" for i in range(10)]
        large_rows = [
            [f"row_{row}_col_{col}" for col in range(10)]
            for row in range(5000)  # 5000 rows
        ]

        # Test memory model with large data
        memory_model = TabularDataModel([headers] + large_rows)

        # Validate data integrity
        assert len(list(memory_model)) == 5000
        assert len(memory_model.column_names) == 10

        # Test access patterns
        all_rows = list(memory_model)
        first_row = all_rows[0]
        last_row = all_rows[-1]
        middle_row = all_rows[2500]

        assert first_row[0] == "row_0_col_0"
        assert last_row[0] == "row_4999_col_0"
        assert middle_row[0] == "row_2500_col_0"

    def test_streaming_model_memory_efficiency(self) -> None:
        """Test that streaming model handles large data efficiently."""
        headers = ["a", "b", "c"]
        # Create data that would be memory intensive if loaded all at once
        large_rows = [[f"val_{i}_{j}" for j in range(3)] for i in range(10000)]

        streaming_model = StreamingTabularDataModel(iter([[headers] + large_rows]))

        # Test streaming access
        count = 0
        for row in streaming_model:
            assert len(row) == 3
            count += 1

        assert count == 10000

        # Test dict streaming
        # Create new streaming model for dict iteration
        data_stream2 = iter([[headers] + large_rows])
        streaming_model2 = StreamingTabularDataModel(data_stream2)
        dict_count = 0
        for row_dict in streaming_model2.iter_rows():
            assert set(row_dict.keys()) == set(headers)
            dict_count += 1

        assert dict_count == 10000


class TestErrorRecoveryWorkflows:
    """Test error recovery and resilience in complete workflows."""

    def test_partial_failure_recovery(self) -> None:
        """Test recovering from partial failures in batch processing."""
        # Create mix of valid and invalid files
        valid_data = ["id,value", "1,100", "2,200"]
        invalid_data = ["id,value", "1,abc", "2,def"]  # Non-numeric values

        files_data = [valid_data, invalid_data, valid_data]

        temp_files = []
        try:
            # Create temporary files
            for data in files_data:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
                    f.write("\n".join(data))
                    temp_files.append(f.name)

            # Process files with error handling
            successful_models = []
            failed_files = []

            for file_path in temp_files:
                try:
                    content = Path(file_path).read_text()

                    lines = content.strip().split("\n")
                    headers = lines[0].split(",")
                    rows = [line.split(",") for line in lines[1:]]

                    # Try to convert values to numbers (this will fail for invalid data)
                    for row in rows:
                        row[1] = float(row[1])

                    model = TabularDataModel([headers] + rows)
                    successful_models.append(model)

                except (ValueError, SplurgeTabularError) as e:
                    failed_files.append((file_path, str(e)))

            # Validate results
            assert len(successful_models) == 2  # Two valid files
            assert len(failed_files) == 1  # One invalid file

            # Check successful models
            for model in successful_models:
                assert len(list(model)) == 2
                assert model.column_names == ["id", "value"]

        finally:
            for file_path in temp_files:
                Path(file_path).unlink()
