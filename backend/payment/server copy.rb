require 'stripe'
require 'sinatra'

# This is your test secret API key.
Stripe.api_key = 'sk_test_51OuVhfCSYPnK2eFyzZbe7FKC9Gxi5CufWZB3EZaNuuW4I1PjCkejcT4q60jWebqs7vBqulMKMlbv7w5O0nQrU2tR00LpRmftZ7'

set :static, true
set :port, 4242

YOUR_DOMAIN = 'http://localhost:5500'

post '/create-checkout-session' do
  content_type 'application/json'

  session = Stripe::Checkout::Session.create({
    line_items: [{
      # Provide the exact Price ID (e.g. pr_1234) of the product you want to sell
      price: '{{PRICE_ID}}',
      quantity: 1,
    }],
    mode: 'payment',
    success_url: YOUR_DOMAIN + '/success.html',
    cancel_url: YOUR_DOMAIN + '/cancel.html',
  })
  redirect session.url, 303
end