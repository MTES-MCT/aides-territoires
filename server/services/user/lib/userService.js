const model = require("../mongoose/userModel");

module.exports = {
  getUserById: id => {
    return model.findById(id);
  },
  saveUser: params => {
    if (!params.id) {
      const instance = new userModel(params);
      return instance.save();
    }
    if (params.id) {
      return model.findOneAndUpdate({ _id: params.id }, params);
    }
  },
  getAll: params => {
    getAll: params => {
      return model.find({});
    };
  }
};
