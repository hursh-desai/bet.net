function dynamicallyLoadScript(url) {
    var script = document.createElement("script");  // create a script DOM node
    script.src = url;  // set its src to the provided URL

    document.head.appendChild(script);  // add it to the end of the head section of the page (could change 'head' to 'body' to add it to the end of the body section instead)
}
dynamicallyLoadScript("https://js.braintreegateway.com/web/3.67.0/js/client.min.js");
dynamicallyLoadScript("https://js.braintreegateway.com/web/3.67.0/js/venmo.min.js");
dynamicallyLoadScript("https://js.braintreegateway.com/web/3.67.0/js/data-collector.min.js");
dynamicallyLoadScript("https://js.braintreegateway.com/web/dropin/1.24.0/js/dropin.min.js");
var client_token;

// fetch('/client_token', {}).then(function(response) {response.json().then(function (data) {client_token = data.client_token});});

var button = document.querySelector('#submit-button');

function connect() {
    braintree.dropin.create({
        authorization: client_token,
        container: '#dropin-container',
        venmo: {} 
      }, function (createErr, instance) {
          instance.requestPaymentMethod(function (err, payload) {
          });
      });
}




// Create a client.
// braintree.client.create({
//     authorization: sandbox_5rxzwymq_kkwts8f7djjnh2tx
//   }).then(function (clientInstance) {
//     // Create a Venmo component.
//     return braintree.venmo.create({
//       client: clientInstance
//     });
//   }).then(function (venmoInstance) {
//     // ...
//   }).catch(function (err) {
//     // Handle component creation error
//   });

