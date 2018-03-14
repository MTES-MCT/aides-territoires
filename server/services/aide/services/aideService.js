const aideModel = require("../mongoose/aideModel");

module.exports = {
  getAideById: id => {
    return aideModel.findById(id);
  }
};
