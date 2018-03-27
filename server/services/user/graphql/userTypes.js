const graphql = require("graphql");
const userService = require("../lib/userService");

module.exports = {
  queries: {},
  mutations: {}
};

// Define the User type
const userType = new graphql.GraphQLObjectType({
  name: "User",
  description: "a single user object",
  fields: {
    id: { type: graphql.GraphQLString },
    name: { type: graphql.GraphQLString },
    mail: { type: graphql.GraphQLString },
    password: { type: graphql.GraphQLString }
  }
});

// queries
module.exports.queries.getUser = {
  type: userType,
  description: "Get a single user by its id",
  args: {
    id: { type: graphql.GraphQLString }
  },
  resolve: function(_, { id }) {
    return userService.getUserById(id).then(result => {
      return result;
    });
  }
};

/*
module.exports.queries.getAllUsers = {
  // describe our field for this type of entity
  type: new graphql.GraphQLObjectType({
    name: "getAllUsers",
    users: [userType]
  }),
  // data returned for this query
  resolve: function(_, { id }) {
    return userService.getAllUsers().then(result => {
      return result;
    });
  }
};
*/

// mutations
module.exports.mutations = {
  saveUser: {
    type: userType,
    args: {
      id: { type: graphql.GraphQLString },
      name: { type: graphql.GraphQLString },
      mail: { type: graphql.GraphQLString },
      password: { type: graphql.GraphQLString }
    },
    resolve: function(_, params) {
      return userService
        .saveUser(params)
        .then(result => {
          return result;
        })
        .catch(e => console.log(e.message));
    }
  }
};
