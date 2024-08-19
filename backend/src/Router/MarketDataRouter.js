const express = require('express');
const router = express.Router();
const { getMarketData } = require('../Controller/MarketDataController');

router.get('/market-data/:symbol', getMarketData);

module.exports = router;
