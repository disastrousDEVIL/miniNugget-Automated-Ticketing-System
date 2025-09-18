# test_complaint_classifier.py
from image_extractor import classify_and_validate,extract_image_text

def run_tests():
    # Test case 1: Extract items from image
    items = extract_image_text("https://drive.google.com/uc?export=view&id=1frcH2XKsTqgE66AJaazRkb-NMS7lhJ2V")
    print("Test 1 - Extracted Items:", items)  # Expected: ["fries", "Coca-Cola"]

    # Test case 2: Classify and validate with a match
    confidence, status = classify_and_validate(
        "https://drive.google.com/uc?export=view&id=1frcH2XKsTqgE66AJaazRkb-NMS7lhJ2V",
        ["fries"]
    )
    print("Test 2 - With Match:", confidence, status)  # Expected: 0.3, "yes"

    # Test case 3: Classify and validate with no match
    confidence, status = classify_and_validate(
        "https://drive.google.com/uc?export=view&id=1frcH2XKsTqgE66AJaazRkb-NMS7lhJ2V",
        ["pizza"]
    )
    print("Test 3 - No Match:", confidence, status)  # Expected: 0.95, "yes"

if __name__ == "__main__":
    run_tests()
