const graphql = require("graphql");
const userService = require("../services/userService");

// queries
module.exports.queries = {
  getUser: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "getUser",
      fields: {
        id: { type: graphql.GraphQLString },
        name: { type: graphql.GraphQLString },
        mail: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      id: { type: graphql.GraphQLString }
    },
    // data returned for this query
    resolve: function(_, { id }) {
      return userService.getUserById(id).then(result => {
        return result;
      });
    }
  }
};

// mutations
module.exports.mutations = {
  saveUser: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "saveUser",
      fields: {
        id: { type: graphql.GraphQLString },
        name: { type: graphql.GraphQLString },
        mail: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      id: { type: graphql.GraphQLString },
      name: { type: graphql.GraphQLString },
      mail: { type: graphql.GraphQLString },
      password: { type: graphql.GraphQLString }
    },
    // data returned for this query
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
