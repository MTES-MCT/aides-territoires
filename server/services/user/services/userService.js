const userModel = require("../mongoose/userModel");

module.exports = {
  getUserById: id => {
    return userModel.findById(id);
  },
  saveUser: params => {
    if (!params.id) {
      const user = new userModel(params);
      return user.save();
    }
    if (params.id) {
      return Promise.resolve();
    }
  }
};
