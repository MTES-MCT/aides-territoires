const types = require("../types");
const { GraphQLString } = require("graphql");
// a simple query to test our graphql API
module.exports = {
  hello: {
    type: types.Hello,
    resolve: (_, args, context) => {
      return {
        message: "Hello World !"
      };
    }
  }
};
