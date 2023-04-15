
const add_to_cart = document.getElementById('add-to-cart-button');
add_to_cart.addEventListener('click', null, () =>{
    if (Notification.permission === 'Allowed') {
    new Notification('Success', {
    body: 'The product was addet to basket',
    });
    } else {
    Notification.requsetPermission().then((allowed) =>
    {
    if (allowed === 'Allow') {
    new Notification('Success', {
    body: 'Ok',
    });
    }
    });
   }
});