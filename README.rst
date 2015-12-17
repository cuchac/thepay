=======
ThePay
=======

Library for accesing ThePay payment gateway from python

.. image:: https://badge.fury.io/py/thepay.svg
    :target: http://badge.fury.io/py/thepay
.. image:: https://travis-ci.org/cuchac/thepay.svg?branch=master
    :target: https://travis-ci.org/cuchac/thepay
.. image:: https://coveralls.io/repos/cuchac/thepay/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/cuchac/thepay?branch=master
    
========
Example
========
Configure ThePay account
------------------------
.. code-block:: python
    from thepay.config import Config
    config = Config()
    config.setCredentials(12345, 12345, 'abcdefg12345', 'abcdefg12345')  # Credentials from ThePay account settings

List available payment methods
------------------------------
.. code-block:: python
    from thepay.dataApi import DataApi
    payments = DataApi(config).getPaymentMethods()

print methods as radio buttons with images

.. code-block:: python
    <div>
        {% for payment in payments %}
         <div class="payment-method">
            <input type="radio" name="payment_method" value="{{ payment.id }}" id="payment_{{ payment.id }}">
            <label for="payment_{{ payment.id }}" title="{{ payment.name }}">
               <img src='http://www.thepay.cz/gate/images/logos/public/209x127/{{ payment.id }}.png' alt="{{ payment.name }}">
            </label>
         </div>
        {% endfor %}
    </div>

Redirect user to ThePay - create payment
----------------------------------------
.. code-block:: python
    from thepay.payment import Payment
    
    payment = Payment(config)
    
    payment.setValue(321)
    payment.setMethodId(13) # ID of payment method from above
    payment.setCustomerEmail('test@test.te)
    payment.setDescription('Order 123 payment')
    payment.setReturnUrl('https://example.com/payment')  # where user will be redirected after payment
    payment.setMerchantData(123)  # Any custom data - not visible to user
    
    payment.getCreateUrl()  # Redirect user to this URL to begin payment

Check incomming payment
-----------------------
This code should be run on `returnUrl` from above code

.. code-block:: python
    return_payment = ReturnPayment(config)
    return_payment.parseData(self.request.GET)  # Pass all GET received data in form of dict()
    
    if not return_payment.checkSignature():
        return False  # Invalid payment signature
    
    return_payment.getMerchantData()  # -> 123
    payment.getValue()  # -> 321
    payment.getStatus()  # Order status

Order statuses
 - 2 = STATUS_OK
 - 3 = STATUS_CANCELED
 - 4 = STATUS_ERROR
 - 6 = STATUS_UNDERPAID
 - 7 = STATUS_WAITING
 - 9 = STATUS_CARD_DEPOSIT

========
License
========
LGPL