const graphql = require("graphql");
const aideService = require("../lib/aideService");

// queries
module.exports.queries = {
  getAide: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "getAide",
      fields: {
        id: { type: graphql.GraphQLString },
        title: { type: graphql.GraphQLString },
        description: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      id: { type: graphql.GraphQLString }
    },
    // data returned for this query
    resolve: function(_, { id }) {
      return aideService.getAideById(id).then(result => {
        return result;
      });
    }
  }
};

// mutations
module.exports.mutations = {
  saveAide: {
    // describe our field for this type of entity
    type: new graphql.GraphQLObjectType({
      name: "saveAide",
      fields: {
        id: { type: graphql.GraphQLString },
        title: { type: graphql.GraphQLString },
        description: { type: graphql.GraphQLString }
      }
    }),
    // `args` describes the arguments that our query accepts
    args: {
      title: { type: graphql.GraphQLString },
      description: { type: graphql.GraphQLString }
    },
    // data returned for this query
    resolve: function(_, params) {
      return aideService
        .saveAide(params)
        .then(result => {
          return result;
        })
        .catch(e => console.log(e.message));
    }
  }
};
