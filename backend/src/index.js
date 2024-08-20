const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const mongoose = require('mongoose');
const marketDataRouter = require('./Router/MarketDataRouter');
const angelOneRouter = require('./Router/AngelOneRouter');

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

app.use('/api', marketDataRouter);
app.use('/api/angelone', angelOneRouter);

const PORT = process.env.PORT || 5000;

app.get('/', (req, res) => {
  res.send('MarketMind AI Backend');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
