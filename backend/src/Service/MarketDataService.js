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

const fetchMarketData = async (symbol) => {
  const api = await getAvailableApi(symbol);

  if (!api) {
    throw new Error('Rate limit exceeded on all available APIs.');
  }

  const url = `${api.base_url}?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${api.api_key}`;

  try {
    const response = await axios.get(url);
    await logApiHit(api.base_url, symbol, response.status);
    return response.data;
  } catch (error) {
    await logApiHit(api.base_url, symbol, 500); // Log with error status
    console.error('Error fetching market data:', error);
    throw error;
  }
};



const authenticate = async () => {
    const url = 'https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword';
    const payload = {
      clientcode: '***REDACTED***',
      password: '***REDACTED***',
      totp: '***REDACTED***'
    };
  
    try {
      const response = await axios.post(url, payload, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      return response.data.data.jwtToken; // return the JWT token
    } catch (error) {
      console.error('Error authenticating:', error);
      throw error;
    }
  };
  
  const callAngelOneApi = async (endpoint, symbol, payload) => {
    const jwtToken = await authenticate(); // Get the JWT token
  
    const api = config.market_data.angel_one;
    const url = `${api.base_url}${api.endpoints[endpoint].url}`;
  
    try {
      const response = await axios.post(url, payload, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${jwtToken}` // Use the token here
        }
      });
      await logApiHit(api.base_url + api.endpoints[endpoint].url, symbol, response.status);
      return response.data;
    } catch (error) {
      await logApiHit(api.base_url + api.endpoints[endpoint].url, symbol, 500);
      console.error('Error calling Angel One API:', error);
      throw error;
    }
  };

module.exports = {
  fetchMarketData,
  callAngelOneApi
};
