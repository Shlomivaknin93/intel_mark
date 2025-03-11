import schedule
import time
from datetime import datetime
from twilio.rest import Client
import requests

class IntelUpdateTracker:
    def __init__(self):
        # Configuration - Replace these with your actual credentials
        self.ALPHA_VANTAGE_API_KEY = '8XCGM88YUDQH7H5J'
        self.TWILIO_ACCOUNT_SID = 'AC76276cb81528c89a8b654a96cc31cc70'
        self.TWILIO_AUTH_TOKEN = '1e06b623d736dc1d15ec04ffee6f2147'
        self.TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Sandbox WhatsApp number
        self.RECIPIENT_WHATSAPP_NUMBER = 'whatsapp:+972502245810'

    def get_stock_information(self):
        """Retrieve current stock information for Intel from Alpha Vantage."""
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=INTC&apikey={self.ALPHA_VANTAGE_API_KEY}'
        try:
            response = requests.get(url)
            data = response.json().get("Global Quote", {})
            current_price = data.get("05. price", "N/A")
            market_cap = "Unavailable in Alpha Vantage"
            return {'price': current_price, 'market_cap': market_cap}
        except Exception as e:
            return {'price': 'Error', 'market_cap': str(e)}

    def get_company_news(self):
        """Fetch recent news about Intel from Alpha Vantage."""
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=INTC&apikey={self.ALPHA_VANTAGE_API_KEY}'
        try:
            response = requests.get(url)
            news_data = response.json()
            news_headlines = []
            for article in news_data.get('feed', [])[:3]:
                news_headlines.append({'title': article.get('title', 'No title'), 'summary': article.get('summary', 'No summary')})
            return news_headlines
        except Exception as e:
            return [{'title': 'Error fetching news', 'summary': str(e)}]

    def get_management_changes(self):
        """Simulate checking for management changes."""
        return [
            "CEO Pat Gelsinger continues to lead strategic transformation",
            "CFO changes or board member updates would be listed here"
        ]

    def get_technology_updates(self):
        """Simulate checking for new technologies."""
        return [
            "Continued focus on advanced semiconductor manufacturing",
            "Developments in AI chip technologies",
            "Progress on new process node technologies"
        ]

    def send_whatsapp_message(self, message):
        """Send WhatsApp message using Twilio Sandbox."""
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                from_=self.TWILIO_WHATSAPP_NUMBER,
                body=message,
                to=self.RECIPIENT_WHATSAPP_NUMBER
            )
            print("Message sent successfully!")
        except Exception as e:
            print(f"Error sending message: {e}")

    def generate_daily_report(self):
        """Compile and send daily Intel update."""
        stock_info = self.get_stock_information()
        news = self.get_company_news()
        management_changes = self.get_management_changes()
        tech_updates = self.get_technology_updates()

        report = f"\U0001F4CA Intel Daily Update - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        report += "\U0001F4B9 Stock Information:\n"
        report += f"Current Price: ${stock_info['price']}\n"
        report += f"Market Cap: {stock_info['market_cap']}\n\n"
        report += "\U0001F4F0 Recent News:\n"
        for article in news:
            report += f"- {article['title']}\n"
        report += "\n\U0001F465 Management Updates:\n"
        for change in management_changes:
            report += f"- {change}\n"
        report += "\n\U0001F680 Technology Developments:\n"
        for tech in tech_updates:
            report += f"- {tech}\n"

        self.send_whatsapp_message(report)


def job():
    tracker = IntelUpdateTracker()
    tracker.generate_daily_report()


# Schedule the job for 9:00 AM Israel time every day
schedule.every().day.at("09:00").do(job)

print("Scheduler is running...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
