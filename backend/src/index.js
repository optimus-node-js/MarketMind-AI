const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const marketDataRouter = require('./Router/MarketDataRouter');

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api', marketDataRouter);

const PORT = process.env.PORT || 5000;

app.get('/', (req, res) => {
  res.send('MarketMind AI Backend');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
