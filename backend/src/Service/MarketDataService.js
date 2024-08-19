const axios = require('axios');
const config = require('../../config/api-config.json');

const checkRateLimit = (apiConfig) => {
  const currentTime = new Date().getTime();
  const { limit, interval, last_hit_time, requests_made, reset_time } = apiConfig.rate_limit;

  // If it's the first request or the interval has passed, reset the counter
  if (!last_hit_time || (currentTime - last_hit_time) > reset_time) {
    apiConfig.rate_limit.last_hit_time = currentTime;
    apiConfig.rate_limit.requests_made = 0;
  }

  // Check if the limit has been exceeded
  if (requests_made >= limit) {
    return false;
  }

  // Increment the request counter
  apiConfig.rate_limit.requests_made += 1;
  return true;
};

const getAvailableApi = () => {
  const apis = config.market_data;
  for (let key in apis) {
    if (checkRateLimit(apis[key])) {
      return apis[key];
    }
  }
  return null; // No available API
};

const fetchMarketData = async (symbol) => {
  const api = getAvailableApi();

  if (!api) {
    throw new Error('Rate limit exceeded on all available APIs.');
  }

  const url = `${api.base_url}?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${api.api_key}`;

  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching market data:', error);
    throw error;
  }
};

module.exports = {
  fetchMarketData
};
