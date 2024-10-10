#!/bin/bash

# Paths
compile_commands_json="build/compile_commands.json"

# Function to run clang-tidy on each file
run_clang_tidy() {
    local file=$1
    echo "Running clang-tidy on $file with $compile_commands_json"

    # Add -warnings-as-errors=* to treat all warnings as errors
    clang-tidy "$file" \
      --export-fixes=- \
      -p "$compile_commands_json" \
      --warnings-as-errors="*" \
      --header-filter=".*" \
      --quiet
}

# Find all .cpp, .hpp, .c, and .h files recursively in the src directory
find src -name '*.cpp' -o -name '*.c' | while read -r file; do
    run_clang_tidy "$file"
done
