const express = require('express');
const router = express.Router();
const {
  placeOrder,
  modifyOrder,
  cancelOrder,
  getLtpData,
  getQuote,
  getCandleData
} = require('../Controller/AngelOneController');

router.post('/order/place', placeOrder);
router.post('/order/modify', modifyOrder);
router.post('/order/cancel', cancelOrder);
router.get('/market/ltp', getLtpData);
router.get('/market/quote', getQuote);
router.get('/market/candle', getCandleData);

module.exports = router;