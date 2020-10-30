from django.test import Client, TestCase

from .models import Transaction, CustomUser

# Create your tests here.

class financeTests(TestCase):

    def setUp(self):

        #Client
        self.client = Client()
        
        # Create Transactions
        nathan = CustomUser.objects.first()
        t1 = Transaction.objects.create(user=nathan, user_id=1, stock='V', name='Visa', price=100, shares=1, buysell='BUY')
        t2 = Transaction.objects.create(user=nathan, user_id=1, stock='SBUX', name='Starbucks', price=100, shares=1, buysell='BUY')
        t3 = Transaction.objects.create(user=nathan, user_id=1, stock='AAPL', name='Apple', price=100, shares=1, buysell='BUY')

        # Create Users
        CustomUser.objects.create(username='nathan')
        CustomUser.objects.create(username='wayne')
        CustomUser.objects.create(username='geri')
        CustomUser.objects.create(username='john')


    def test_transaction_count(self):
        t = Transaction.objects.filter(user_id=1)
        self.assertEqual(t.count(), 3)

    def test_user_count(self):
        u = CustomUser.objects.all()
        self.assertEqual(u.count(), 4)

    def test_buy_returns_200(self): 
        response = self.client.get('/stocks/buy/')
        self.assertEqual(response.status_code, 200)

    def test_quoted_template(self):
        url = ('/stocks/quote/')
        symbol = 'V' 
        response = self.client.post(url, symbol)
        self.assertTemplateUsed(response, 'stocks/quoted.html')
        