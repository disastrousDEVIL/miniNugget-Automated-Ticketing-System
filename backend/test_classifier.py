from classifier import classify_ticket
tests = [
    "My order came 40 minutes late",
    "The fries and coke were missing from my order",
    "The delivery guy was extremely rude",
    "I didn’t receive my food at all",
    "The packaging was torn and food was cold"  # edge case (should go to agent/manual)
]

for t in tests:
    result = classify_ticket(t)
    print(f"Complaint: {t}")
    print("Result:", result)
    print("-" * 50)
