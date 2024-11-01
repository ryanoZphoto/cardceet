from email_sender import PaymentReceiptService

class PaymentProcessor:
    def __init__(self):
        self.receipt_service = PaymentReceiptService()
        
    async def process_payment(self, payment_data: dict):
        try:
            # Process payment with your payment provider
            payment_result = await self._process_with_provider(payment_data)
            
            if payment_result['success']:
                # Send receipt
                receipt_result = self.receipt_service.send_payment_receipt(
                    customer_email=payment_data['email'],
                    amount=payment_data['amount'],
                    transaction_id=payment_result['transaction_id'],
                    payment_method=payment_data['payment_method'],
                    currency=payment_data['currency'],
                    additional_details=payment_result['details']
                )
                
                return {
                    'success': True,
                    'payment_id': payment_result['transaction_id'],
                    'receipt_sent': receipt_result['success']
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)} 