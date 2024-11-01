import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

class PaymentReceiptService:
    def __init__(self):
        load_dotenv()
        self.sender_email = os.getenv('GMAIL_USER')
        self.app_password = os.getenv('GMAIL_APP_PASSWORD')
        
    def send_payment_receipt(self, 
                           customer_email: str,
                           amount: float,
                           transaction_id: str,
                           payment_method: str,
                           currency: str = 'USD',
                           additional_details: dict = None):
        try:
            # Setup SMTP connection
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                
                # Create HTML message
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f'Payment Receipt - {transaction_id}'
                msg['From'] = self.sender_email
                msg['To'] = customer_email
                
                # Build receipt details
                transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                payment_details = {
                    'Amount': f'{currency} {amount:.2f}',
                    'Date': transaction_date,
                    'Transaction ID': transaction_id,
                    'Payment Method': payment_method
                }
                
                if additional_details:
                    payment_details.update(additional_details)
                
                # Create HTML content
                html_content = self._generate_html_receipt(payment_details)
                msg.attach(MIMEText(html_content, 'html'))
                
                # Send email
                server.send_message(msg)
                
            return {
                'success': True,
                'transaction_id': transaction_id,
                'timestamp': transaction_date
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'transaction_id': transaction_id
            }
    
    def _generate_html_receipt(self, details: dict) -> str:
        """Generate HTML formatted receipt"""
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="padding: 20px; background-color: #f8f9fa;">
                    <h2 style="color: #333;">Payment Receipt</h2>
                    <div style="background-color: white; padding: 20px; border-radius: 5px;">
        """
        
        for key, value in details.items():
            html += f"""
                        <p style="margin: 10px 0;">
                            <strong>{key}:</strong> {value}
                        </p>
            """
            
        html += """
                    </div>
                    <div style="margin-top: 20px; font-size: 12px; color: #666;">
                        <p>This is an automated receipt. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html