const mongoose = require('mongoose');

const HitLogSchema = new mongoose.Schema({
  time: { type: Date, default: Date.now },
  status: { type: Number, required: true }
});

const ApiLogSchema = new mongoose.Schema({
  apiName: { type: String, required: true },
  symbol: { type: String, required: true },
  requestLogs: [HitLogSchema]
});

const ApiLog = mongoose.model('ApiLog', ApiLogSchema);

module.exports = ApiLog;
