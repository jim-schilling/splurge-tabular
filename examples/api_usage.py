"""
Comprehensive API Usage Example for splurge-tabular

This example demonstrates the key features and APIs of the splurge-tabular library,
including in-memory and streaming data processing, error handling, and utility functions.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

import json

from splurge_tabular import (
    SplurgeTabularLookupError,
    # Exceptions
    SplurgeTabularTypeError,
    StreamingTabularDataModel,
    TabularDataModel,
    ensure_minimum_columns,
    normalize_rows,
    process_headers,
)


def demo_basic_tabular_data_model():
    """Demonstrate basic TabularDataModel usage."""
    print("=== Basic TabularDataModel Demo ===")

    # Sample data with headers
    data = [
        ["Name", "Age", "City", "Salary"],
        ["Alice Johnson", "28", "New York", "75000"],
        ["Bob Smith", "34", "London", "82000"],
        ["Charlie Brown", "22", "Tokyo", "68000"],
        ["Diana Prince", "31", "Paris", "91000"],
    ]

    # Create model
    model = TabularDataModel(data)

    print(f"Column names: {model.column_names}")
    print(f"Row count: {model.row_count}")
    print(f"Column count: {model.column_count}")

    # Access column information
    print("\nColumn types:")
    for col in model.column_names:
        col_type = model.column_type(col)
        print(f"  {col}: {col_type}")

    # Access data in different ways
    print("\nFirst row as dict:")
    first_row = model.row(0)
    print(json.dumps(first_row, indent=2))

    print("\nFirst row as list:")
    print(model.row_as_list(0))

    print("\nFirst row as tuple:")
    print(model.row_as_tuple(0))

    # Access specific cell
    print(f"\nAlice's age: {model.cell_value('Age', 0)}")

    # Access entire column
    print(f"\nAll cities: {model.column_values('City')}")

    # Iterate over rows
    print("\nIterating over all rows:")
    for i, row_dict in enumerate(model.iter_rows()):
        print(f"Row {i}: {row_dict}")

    # Typed access
    print("\nTyped access demo:")
    typed_model = model.to_typed()
    for row in typed_model.iter_rows():
        print(f"Name: {row['Name']} (type: {type(row['Name'])})")
        print(f"Age: {row['Age']} (type: {type(row['Age'])})")
        break  # Just show first row


def demo_header_processing():
    """Demonstrate header processing with multiple header rows."""
    print("\n=== Header Processing Demo ===")

    # Data with multiple header rows
    data = [
        ["Personal Info", "", "Employment", ""],
        ["Name", "Age", "Company", "Salary"],
        ["Alice Johnson", "28", "Tech Corp", "75000"],
        ["Bob Smith", "34", "Data Inc", "82000"],
    ]

    # Process with 2 header rows
    model = TabularDataModel(data, header_rows=2)

    print(f"Column names: {model.column_names}")
    print(f"Row count: {model.row_count}")

    # Show first row
    print(f"First data row: {model.row(0)}")


def demo_streaming_tabular_data_model():
    """Demonstrate StreamingTabularDataModel for large datasets."""
    print("\n=== Streaming TabularDataModel Demo ===")

    # Create a data stream (simulating chunks from a large file)
    def create_data_stream():
        # First chunk with headers
        yield [
            ["Name", "Age", "City", "Salary"],
            ["Alice Johnson", "28", "New York", "75000"],
            ["Bob Smith", "34", "London", "82000"],
        ]
        # Second chunk
        yield [
            ["Charlie Brown", "22", "Tokyo", "68000"],
            ["Diana Prince", "31", "Paris", "91000"],
            ["Eve Wilson", "29", "Sydney", "78000"],
        ]

    # Create streaming model
    streaming_model = StreamingTabularDataModel(create_data_stream())

    print(f"Column names: {streaming_model.column_names}")
    print(f"Column count: {streaming_model.column_count}")

    # Process stream
    print("\nProcessing stream:")
    row_count = 0
    for row in streaming_model:
        print(f"Row {row_count}: {row}")
        row_count += 1

    print(f"Total rows processed: {row_count}")


def demo_error_handling():
    """Demonstrate error handling and validation."""
    print("\n=== Error Handling Demo ===")

    # Test invalid data structure
    try:
        invalid_data = "not a list"
        TabularDataModel(invalid_data)
    except SplurgeTabularTypeError as e:
        print(f"Type error caught: {e}")

    # Test column not found
    try:
        data = [["Name", "Age"], ["Alice", "25"]]
        model = TabularDataModel(data)
        model.column_values("NonExistentColumn")
    except SplurgeTabularLookupError as e:
        print(f"Column error caught: {e}")

    # Test row index out of range
    try:
        data = [["Name", "Age"], ["Alice", "25"]]
        model = TabularDataModel(data)
        model.cell_value("Name", 10)  # Use cell_value which has bounds checking
    except SplurgeTabularLookupError as e:
        print(f"Row error caught: {e}")


def demo_utility_functions():
    """Demonstrate utility functions."""
    print("\n=== Utility Functions Demo ===")

    # Test minimum columns check
    print("\nMinimum columns check:")
    data_with_few_columns = [["Name"], ["Alice"]]
    padded_data = ensure_minimum_columns(data_with_few_columns, min_columns=2)
    print(f"Padded data: {padded_data}")

    # Test header processing utility
    print("\nHeader processing:")
    header_data = [["First", "Second"], ["Name", "Age"]]
    processed_headers, column_names = process_headers(header_data, header_rows=2)
    print(f"Processed headers: {processed_headers}")
    print(f"Column names: {column_names}")

    # Test row normalization
    print("\nRow normalization:")
    uneven_rows = [["Alice", "25", "NY"], ["Bob", "30"], ["Charlie", "22", "LA", "Extra"]]
    normalized = normalize_rows(uneven_rows, skip_empty_rows=False)
    print(f"Original: {uneven_rows}")
    print(f"Normalized: {normalized}")


def demo_advanced_features():
    """Demonstrate advanced features like filtering and transformation."""
    print("\n=== Advanced Features Demo ===")

    # Sample data
    data = [
        ["Name", "Age", "Department", "Salary"],
        ["Alice", "28", "Engineering", "75000"],
        ["Bob", "34", "Sales", "82000"],
        ["Charlie", "22", "Engineering", "68000"],
        ["Diana", "31", "HR", "91000"],
        ["Eve", "29", "Engineering", "78000"],
    ]

    model = TabularDataModel(data)

    # Filter rows (manual iteration)
    print("Engineering department employees:")
    for row_dict in model.iter_rows():
        if row_dict["Department"] == "Engineering":
            print(f"  {row_dict['Name']}: {row_dict['Salary']}")

    # Calculate statistics
    salaries = [int(row["Salary"]) for row in model.iter_rows()]
    print("\nSalary statistics:")
    print(f"  Average: ${sum(salaries) / len(salaries):.2f}")
    print(f"  Min: ${min(salaries)}")
    print(f"  Max: ${max(salaries)}")

    # Typed access with custom type configs
    print("\nTyped access with custom configs:")
    typed_model = model.to_typed()
    for row in typed_model.iter_rows():
        print(f"  {row['Name']}: Age={row['Age']} (type: {type(row['Age'])})")
        break  # Just show first


def main():
    """Run all demonstrations."""
    print("Splurge Tabular Library - Comprehensive API Usage Example")
    print("=" * 60)

    demo_basic_tabular_data_model()
    demo_header_processing()
    demo_streaming_tabular_data_model()
    demo_error_handling()
    demo_utility_functions()
    demo_advanced_features()

    print("\n" + "=" * 60)
    print("Demo completed! Check the output above for all features.")


if __name__ == "__main__":
    main()
