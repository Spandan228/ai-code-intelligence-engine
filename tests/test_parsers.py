from parsers.python_parser import PythonParser
import os

def test_extraction():
    parser = PythonParser()
    files = ["sample_test.py", "test_sample.py"]
    
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"File {file_path} not found")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        print(f"\nParsing {file_path}...")
        results = parser.parse_code(code, file_path)
        print(f"Extracted {len(results)} snippets:")
        for res in results:
            print(f"- {res['type']}: {res['name']} at line {res['start_line']}")

if __name__ == "__main__":
    test_extraction()
