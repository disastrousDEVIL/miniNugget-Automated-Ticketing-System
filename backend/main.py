from fastapi import FastAPI
from datetime import datetime, timezone
from schemas import TicketOut,TicketCreate
from models import Ticket
from typing import List
from fastapi import HTTPException
from classifier import classify_ticket
from image_extractor import classify_and_validate
app = FastAPI(title="Nugget Lite by KrishB")

@app.get("/")
def read_root():
    return {"message": "system is running"}

@app.post("/submit-ticket",response_model=TicketOut)
def submit_ticket(ticket: TicketCreate):
    #calling classify_text here to get reply tag and reply text
    classification=classify_ticket(ticket.problem_text)
    print(classification)

    confidence=classification.get("confidence")
    complaint_type=classification.get("type")

    decision="auto" if confidence>=0.65 else "manual"
    status="Resolved" if decision=="auto" else "Pending"

    reply_tag= None
    reply_text= None

    if complaint_type=="order_not_received":
        decision="manual"
        status="Pending"
        reply_text="We are looking into your order. Please wait a little longer."
        reply_tag="delivery_check"
    if complaint_type=="items_missing":
        if ticket.image_url:
            confidence,status=classify_and_validate(str(ticket.image_url),classification.get("extracted_items"))
            decision="auto" if confidence>=0.65 else "manual"
            status="Resolved" if decision=="auto" else "Pending"
            if decision=="auto":
                reply_text="Refund for missing items has been initiated."
                reply_tag="items_price_refund_initiated"
            elif decision=="manual" and status=="yes":
                reply_text="We are looking into your order. Please wait a little longer."
                reply_tag="image_verification_required"
            elif decision=="manual" and status=="no":
                reply_text="Please provide a clear image of the items you received."
                reply_tag="image_required"
        else:
            decision="manual"
            status="Pending"
            reply_text="Please provide a clear image of the items you received."
            reply_tag="image_required"

    if decision=="auto":
        if complaint_type == "order_delayed":
            reply_text = "We apologize for the delay. A 10 % compensation has been initiated."
            reply_tag = "10_percent_initiated"

        elif complaint_type == "agent_rude":

            reply_text = "Sorry for the agents behaviour. We value your feedback."
            reply_tag = "agent_feedback_ack"

        elif complaint_type == "order_quality_issue":
            reply_text = "Sorry the food quality did not meet expectations. We have shared your feedback with the restaurant."
            reply_tag = "quality_feedback_ack"


    new_ticket=Ticket.create(
        user_id=ticket.user_id,
        order_id=ticket.order_id,
        problem_text=ticket.problem_text,
        image_url=str(ticket.image_url) if ticket.image_url else None,
        status=status,
        decision=decision,  
        created_at=datetime.now(timezone.utc),
        restaurant_name=ticket.restaurant_name,  
        reply_tag=reply_tag,
        reply_text=reply_text,
        final_confidence=confidence
    )
    return TicketOut(
        id=new_ticket.id,
        user_id=new_ticket.user_id,
        order_id=new_ticket.order_id,
        problem_text=new_ticket.problem_text,
        image_url=str(new_ticket.image_url) if new_ticket.image_url else None,
        status=new_ticket.status,
        created_at=new_ticket.created_at,
        restaurant_name=new_ticket.restaurant_name,  
        reply_tag=new_ticket.reply_tag,
        reply_text=new_ticket.reply_text
    )


@app.get("/tickets",response_model=List[TicketOut])
def get_tickets():
    tickets=Ticket.select().order_by(Ticket.created_at.desc())
    return [TicketOut(id=t.id,
    user_id=t.user_id,
    order_id=t.order_id,
    problem_text=t.problem_text,
    image_url=str(t.image_url) if t.image_url else None,
    status=t.status,
    created_at=t.created_at,
    restaurant_name=t.restaurant_name,
    reply_tag=t.reply_tag,
    reply_text=t.reply_text
    ) for t in tickets]

@app.get("/tickets/pending",response_model=List[TicketOut])
def get_pending_tickets():
    tickets=Ticket.select().where(Ticket.status=="Pending").order_by(Ticket.created_at.desc())
    return [TicketOut(id=t.id,
    user_id=t.user_id,
    order_id=t.order_id,
    problem_text=t.problem_text,
    image_url=str(t.image_url) if t.image_url else None,
    status=t.status,
    created_at=t.created_at,
    restaurant_name=t.restaurant_name,
    reply_tag=t.reply_tag,
    reply_text=t.reply_text
    ) for t in tickets]

@app.post("/tickets/{ticket_id}/update")
def update_ticket(ticket_id:int,status:str):
    ticket=Ticket.get_or_none(Ticket.id==ticket_id)
    if not ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    ticket.status=status
    ticket.save()

    return {"ok":True,"id":ticket_id,"new_status":status}


