const axios = require('axios');
const config = require('../../config/api-config.json');

const getAlphaVantageData = async (req, res) => {
  const symbol = req.params.symbol;
  const url = `${config.market_data.alpha_vantage.base_url}?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${process.env.ALPHA_VANTAGE_API_KEY}`;
  
  try {
    const response = await axios.get(url);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching data from Alpha Vantage:', error);
    res.status(500).send('Server Error');
  }
};

module.exports = {
  getAlphaVantageData
};
