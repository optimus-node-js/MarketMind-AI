const express = require('express');
const router = express.Router();
const { getAlphaVantageData } = require('../Controller/MarketDataController');

router.get('/market-data/:symbol', getAlphaVantageData);

module.exports = router;
