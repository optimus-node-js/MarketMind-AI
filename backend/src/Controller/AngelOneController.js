const { callAngelOneApi } = require('../Service/MarketDataService');

const placeOrder = async (req, res) => {
  try {
    const data = await callAngelOneApi('placeOrder', req.body.symbol, req.body);
    res.json(data);
  } catch (error) {
    res.status(500).send('Error placing order');
  }
};

const modifyOrder = async (req, res) => {
  try {
    const data = await callAngelOneApi('modifyOrder', req.body.symbol, req.body);
    res.json(data);
  } catch (error) {
    res.status(500).send('Error modifying order');
  }
};

const cancelOrder = async (req, res) => {
  try {
    const data = await callAngelOneApi('cancelOrder', req.body.symbol, req.body);
    res.json(data);
  } catch (error) {
    res.status(500).send('Error cancelling order');
  }
};

const getLtpData = async (req, res) => {
  try {
    const data = await callAngelOneApi('getLtpData', req.query.symbol, {});
    res.json(data);
  } catch (error) {
    res.status(500).send('Error fetching LTP data');
  }
};

const getQuote = async (req, res) => {
  try {
    const data = await callAngelOneApi('getQuote', req.query.symbol, {});
    res.json(data);
  } catch (error) {
    res.status(500).send('Error fetching quote');
  }
};

const getCandleData = async (req, res) => {
  try {
    const data = await callAngelOneApi('getCandleData', req.query.symbol, {});
    res.json(data);
  } catch (error) {
    res.status(500).send('Error fetching candle data');
  }
};

module.exports = {
  placeOrder,
  modifyOrder,
  cancelOrder,
  getLtpData,
  getQuote,
  getCandleData
};
