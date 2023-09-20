const axios = require('axios');
const fs = require('fs');

function saveJSONToFile(data, filename) {
  fs.writeFileSync(filename, JSON.stringify(data, null, 2), 'utf-8');
}

let response = null;
new Promise(async (resolve, reject) => {
  try {
    response = await axios.get('https://sandbox-api.coinmarketcap.com/v1/global-metrics/quotes/historical', {
      headers: {
        'X-CMC_PRO_API_KEY': 'c9410819-1b4a-44e3-9ea0-b0d64597bd44',
      },
    });
    if (response.status === 200) {
      const json = response.data;

      // Specify the filename where you want to save the JSON data
      const filename = 'coinmarketcap_data_historical.json';

      // Save the JSON data to a file
      saveJSONToFile(json, filename);

      // Resolve the Promise
      console.log(`JSON data saved to ${filename}`);
      resolve(json);
    } else {
      // Handle non-200 status codes if needed
      console.error(`Error: ${response.status}`);
      reject(`Error: ${response.status}`);
    }
  } catch (ex) {
    console.error(ex);
    reject(ex);
  }
});