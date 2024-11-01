from email_sender import PaymentReceiptService

def test_payment_receipt():
    receipt_service = PaymentReceiptService()
    
    # Example for credit card payment
    credit_card_result = receipt_service.send_payment_receipt(
        customer_email="ryanosmunphoto@gmail.com",
        amount=99.99,
        transaction_id="CC-TEST123",
        payment_method="Credit Card",
        additional_details={
            "Card Type": "Visa",
            "Last 4 Digits": "****1234"
        }
    )
    print(f"Credit Card Receipt sent: {credit_card_result}")
    
    # Example for digital wallet payment
    digital_wallet_result = receipt_service.send_payment_receipt(
        customer_email="ryanosmunphoto@gmail.com",
        amount=50.00,
        transaction_id="DW-TEST456",
        payment_method="Digital Wallet",
        currency="EUR",
        additional_details={
            "Wallet Provider": "PayPal",
            "Account": "user@example.com"
        }
    )
    print(f"Digital Wallet Receipt sent: {digital_wallet_result}")

if __name__ == "__main__":
    test_payment_receipt() 
