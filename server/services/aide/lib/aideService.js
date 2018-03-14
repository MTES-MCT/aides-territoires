const aideModel = require("../mongoose/aideModel");

module.exports = {
  getAideById: id => {
    return aideModel.findById(id);
  },
  saveAide: params => {
    if (!params.id) {
      const user = new aideModel(params);
      return user.save();
    }
    if (params.id) {
      return aideModel.findOneAndUpdate({ _id: params.id }, params);
    }
  }
};
