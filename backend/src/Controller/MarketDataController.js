const axios = require('axios');
const config = require('../../config/api-config.json');
const { fetchMarketData } = require('../Service/MarketDataService');


const getMarketData = async (req, res) => {
  const symbol = req.params.symbol;

  try {
    const data = await fetchMarketData(symbol);
    res.json(data);
  } catch (error) {
    res.status(500).send('Error fetching market data');
  }
};

module.exports = {
  getMarketData
};
