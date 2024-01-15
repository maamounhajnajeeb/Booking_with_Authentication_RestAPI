// payment.js

async function processPayment(clientSecret) {
    const stripe = Stripe('pk_test_51NkkK1Feq4GSqlxQgeZEDgdKlidDxGI9Lq2zxnHEo7yCwnVbRKKWlTwnU6AswGazL6ZSCuWXgePMi85GUpO6oydE002UjlqE77');

    const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: await stripe.createToken('person', {
                number: '6200000000000005',
                exp_month: '12',
                exp_year: '2030',
                cvc: '123',
            }),
        },
    });

    if (result.error) {
        console.error(result.error.message);
    } else {
        window.location.href = '/success/';
    }
}
