"""
payments.py — Invoice and payment management.

GET    /api/payments/invoices            List invoices (admin/teacher = all; student = own)
GET    /api/payments/invoices/{id}       Invoice detail
POST   /api/payments/invoices            Create invoice (admin)
PUT    /api/payments/invoices/{id}       Update invoice (admin)
DELETE /api/payments/invoices/{id}       Delete invoice if unpaid (admin)
POST   /api/payments/invoices/{id}/pay  Record payment (admin)
GET    /api/payments/my                  Own invoices + payments (student)
GET    /api/payments/summary             Summary stats (admin)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import security

router = APIRouter()

VALID_STATUSES = {"unpaid", "paid", "overdue", "waived"}
VALID_METHODS = {"cash", "card", "bank_transfer", "waived"}


class InvoiceCreate(BaseModel):
    student_id: int
    title: str
    description: Optional[str] = None
    amount: float
    due_date: Optional[datetime] = None


class InvoiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None


class PaymentCreate(BaseModel):
    amount_paid: float
    payment_method: str
    reference: Optional[str] = None


def _invoice_dict(inv: models.Invoice):
    return {
        "id": inv.id,
        "student_id": inv.student_id,
        "student_name": inv.student.name if inv.student else None,
        "title": inv.title,
        "description": inv.description,
        "amount": inv.amount,
        "due_date": str(inv.due_date) if inv.due_date else None,
        "status": inv.status,
        "created_at": str(inv.created_at),
        "payments": [
            {
                "id": p.id,
                "amount_paid": p.amount_paid,
                "payment_method": p.payment_method,
                "reference": p.reference,
                "paid_at": str(p.paid_at),
            }
            for p in inv.payments
        ],
    }


@router.get("/summary")
def payment_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    all_invoices = db.query(models.Invoice).all()
    total_collected = sum(
        p.amount_paid
        for inv in all_invoices
        for p in inv.payments
    )
    outstanding = sum(inv.amount for inv in all_invoices if inv.status == "unpaid")
    now = datetime.utcnow()
    overdue_count = sum(
        1 for inv in all_invoices
        if inv.status == "unpaid" and inv.due_date and inv.due_date < now
    )
    return {
        "total_collected": total_collected,
        "outstanding": outstanding,
        "overdue_count": overdue_count,
        "total_invoices": len(all_invoices),
    }


@router.get("/my")
def my_invoices(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("student")),
):
    invoices = db.query(models.Invoice).filter(
        models.Invoice.student_id == current_user.id
    ).order_by(models.Invoice.created_at.desc()).all()
    return [_invoice_dict(inv) for inv in invoices]


@router.get("/invoices")
def list_invoices(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if current_user.role == "student":
        invoices = db.query(models.Invoice).filter(
            models.Invoice.student_id == current_user.id
        ).all()
    elif current_user.role in ("admin", "teacher"):
        invoices = db.query(models.Invoice).all()
    else:
        raise HTTPException(403, "Insufficient permissions")
    return [_invoice_dict(inv) for inv in invoices]


@router.get("/invoices/{invoice_id}")
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(404, "Invoice not found")
    if current_user.role == "student" and inv.student_id != current_user.id:
        raise HTTPException(403, "Not your invoice")
    return _invoice_dict(inv)


@router.post("/invoices")
def create_invoice(
    data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    student = db.query(models.User).filter(models.User.id == data.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(400, "Student not found")
    inv = models.Invoice(
        student_id=data.student_id,
        title=data.title,
        description=data.description,
        amount=data.amount,
        due_date=data.due_date,
        status="unpaid",
        created_by=current_user.id,
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return {"id": inv.id, "title": inv.title}


@router.put("/invoices/{invoice_id}")
def update_invoice(
    invoice_id: int,
    data: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(404, "Invoice not found")
    if data.title is not None:
        inv.title = data.title
    if data.description is not None:
        inv.description = data.description
    if data.amount is not None:
        inv.amount = data.amount
    if data.due_date is not None:
        inv.due_date = data.due_date
    if data.status is not None:
        if data.status not in VALID_STATUSES:
            raise HTTPException(400, f"status must be one of: {VALID_STATUSES}")
        inv.status = data.status
    db.commit()
    return {"ok": True}


@router.delete("/invoices/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(404, "Invoice not found")
    if inv.status != "unpaid":
        raise HTTPException(400, "Can only delete unpaid invoices")
    db.delete(inv)
    db.commit()
    return {"ok": True}


@router.post("/invoices/{invoice_id}/pay")
def record_payment(
    invoice_id: int,
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.require_role("admin")),
):
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(404, "Invoice not found")
    if data.payment_method not in VALID_METHODS:
        raise HTTPException(400, f"payment_method must be one of: {VALID_METHODS}")
    payment = models.Payment(
        invoice_id=invoice_id,
        paid_by=inv.student_id,
        amount_paid=data.amount_paid,
        payment_method=data.payment_method,
        reference=data.reference,
        recorded_by=current_user.id,
    )
    db.add(payment)
    # Update invoice status
    total_paid = sum(p.amount_paid for p in inv.payments) + data.amount_paid
    if total_paid >= inv.amount or data.payment_method == "waived":
        inv.status = "paid"
    db.commit()
    db.refresh(payment)
    return {"id": payment.id, "invoice_status": inv.status}
