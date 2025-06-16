# schema

## Purpose
This subfolder manages schema definitions for logs and data structures.

## Contents
- Files defining schemas for various data formats.

## Interactions
- Provides schema definitions for use in indexing, merging, and summarization tasks.
- Interacts with the `Index` and `merged` subfolders to validate data formats.

## Conventions
- Schema files are written in JSON format.
- Field names and data types are standardized across all schemas.

## Usage
- Use schema files to validate the structure of logs and indexes.
- Example: Run `validate_schema.py` to check if a log file adheres to the schema.

## Notes
- Update schema files whenever new fields are added to logs or indexes.
- Ensure backward compatibility when modifying existing schemas.
