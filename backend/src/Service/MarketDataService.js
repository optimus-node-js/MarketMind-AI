const axios = require('axios');
const config = require('../../config/api-config.json');
const ApiLog = require('../Model/ApiLogModel');

// Enhanced rate limit checker that queries MongoDB
const checkRateLimit = async (apiConfig, symbol) => {
  const currentTime = new Date();
  const { limit, reset_time } = apiConfig.rate_limit;

  // Calculate the start time for the interval
  const intervalStartTime = new Date(currentTime - reset_time);

  // Query MongoDB to count requests made in this interval
  const recentLogs = await ApiLog.aggregate([
    { $match: { apiName: apiConfig.base_url, symbol: symbol, "requestLogs.time": { $gte: intervalStartTime } } },
    { $unwind: "$requestLogs" },
    { $match: { "requestLogs.time": { $gte: intervalStartTime } } },
    { $count: "requests_made" }
  ]);

  return (recentLogs[0] ? recentLogs[0].requests_made : 0) < limit;
};

// Enhanced getAvailableApi function to use MongoDB data
const getAvailableApi = async (symbol) => {
  const apis = config.market_data;
  for (let key in apis) {
    if (await checkRateLimit(apis[key], symbol)) {
      return apis[key];
    }
  }
  return null; // No available API within rate limits
};

const logApiHit = async (apiName, symbol, status) => {
  try {
    const logEntry = {
      time: new Date(),
      status: status
    };

    const existingLog = await ApiLog.findOne({ apiName: apiName, symbol: symbol });

    if (existingLog) {
      // Push the new log into the requestLogs array
      existingLog.requestLogs.push(logEntry);
      await existingLog.save();
    } else {
      // Create a new log entry
      const apiLog = new ApiLog({
        apiName: apiName,
        symbol: symbol,
        requestLogs: [logEntry]
      });
      await apiLog.save();
    }
  } catch (error) {
    console.error('Error logging API hit:', error);
  }
};

// Function to fetch data from Alpha Vantage
const fetchAlphaVantageData = async (symbol) => {
  const apiKey = config.market_data.alpha_vantage.api_key;
  const url = `${config.market_data.alpha_vantage.base_url}?function=TIME_SERIES_INTRADAY&symbol=${symbol}&interval=1min&apikey=${apiKey}`;

  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching Alpha Vantage data:', error);
    throw error;
  }
};

// Function to fetch data from Finnhub
const fetchFinnhubData = async (symbol) => {
  const apiKey = config.market_data.finnhub.api_key;
  const url = `${config.market_data.finnhub.base_url}/quote?symbol=${symbol}&token=${apiKey}`;

  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching Finnhub data:', error);
    throw error;
  }
};

// Function to fetch data from Polygon.io
const fetchPolygonData = async (symbol) => {
  const apiKey = config.market_data.polygon.api_key;
  const url = `${config.market_data.polygon.base_url}/aggs/ticker/${symbol}/prev?apiKey=${apiKey}`;

  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching Polygon data:', error);
    throw error;
  }
};

// Main function to fetch data from all APIs
const fetchMarketData = async (symbol, requestType = 'defaultType') => {
  const api = await getAvailableApi(symbol, requestType);

  if (!api) {
    throw new Error('Rate limit exceeded on all available APIs.');
  }

  const endpoint = api.endpoints[requestType] || api.endpoints['defaultType']; // Fallback to default if undefined

  try {
    const url = `${api.base_url}${endpoint.url}?symbol=${symbol}&apikey=${api.api_key}`;
    const response = await axios.get(url);
    await logApiHit(api.base_url, symbol, response.status);
    return response.data;
  } catch (error) {
    await logApiHit(api.base_url, symbol, 500);
    console.error('Error fetching market data:', error);
    throw error;
  }
};




module.exports = {
  fetchMarketData,
  fetchAlphaVantageData,
  fetchFinnhubData,
  fetchPolygonData,
  checkRateLimit,
  getAvailableApi,
};
