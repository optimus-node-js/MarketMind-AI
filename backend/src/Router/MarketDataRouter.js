const express = require('express');
const router = express.Router();
const { getMarketData } = require('../Controller/MarketDataController');

router.get('/market-data', getMarketData);

module.exports = router;
