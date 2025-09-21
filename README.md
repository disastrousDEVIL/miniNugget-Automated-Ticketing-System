# AI-Powered Food Delivery Ticketing System

An **automated support ticketing system** for food delivery apps, built with **FastAPI**, **LangChain**, and **SQLite**.  
It classifies customer complaints, validates missing-item claims using receipt images, and auto-generates support replies.

---

## 🚀 Features

- **Complaint Classification**  
  AI-powered categorization into:
  - `order_delayed`
  - `items_missing`
  - `agent_rude`
  - `order_not_received`
  - `order_quality_issue`

- **Confidence-Based Resolution**  
  - High confidence → Auto-resolve with predefined replies  
  - Low confidence → Escalate to manual review  

- **Image Validation**  
  Upload receipts or food images to **verify missing item claims**.  

- **Ticket Lifecycle Management**  
  - Submit complaint tickets  
  - Fetch all or pending tickets  
  - Update ticket status  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI  
- **Database:** SQLite (via Peewee ORM)  
- **AI Models:** OpenAI GPT (via LangChain)  
- **Image Validation:** OCR + food item extraction  

---

## 📂 Project Structure

```

.
├── classifier.py         # AI complaint classifier
├── image\_extractor.py    # OCR + food item extractor
├── main.py               # FastAPI app entrypoint
├── models.py             # Database models
├── schemas.py            # API schemas
├── test\_classifier.py    # Simple test cases
├── tickets.db            # SQLite database

````

---

## ⚡ Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/disastrousDEVIL/miniNugget-Automated-Ticketing-System.git
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your OpenAI API Key

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 4. Run the FastAPI Server

```bash
cd backend
uvicorn main:app --reload
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📌 API Endpoints

* `GET /` – Health check
* `POST /submit-ticket` – Submit a new complaint
* `GET /tickets` – Fetch all tickets
* `GET /tickets/pending` – Fetch only pending tickets
* `POST /tickets/{ticket_id}/update` – Update ticket status

---

## 🧪 Testing

Run the test script:

```bash
python test_classifier.py
```

---

## 🤝 Contributing

Contributions welcome! Fork the repo, improve, and make a PR.
