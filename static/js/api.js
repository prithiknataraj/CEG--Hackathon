// your-script.js

const sdk = require('api')('@verbwire/v1.0#hr2s143dl9hbr7s9');

sdk.auth('pk_live_f575ef3c-5cea-4a9b-ab6c-3c5456dfe774');
sdk.get('/nft/data/transactions', {
  walletAddress: '0x5b441238F1F12263393f0Ff3B1Bd9Da2f2519c60',
  chain: 'ethereum'
})
.then(res => {
  const apiResponseContainer = document.getElementById('apiResponseContainer');
  apiResponseContainer.innerHTML = `<pre>${JSON.stringify(res, null, 2)}</pre>`;
})
.catch(err => console.error(err));