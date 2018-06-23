const { GraphQLString, GraphQLList } = require("graphql");
const { getAllMenus, getMenuById } = require("../../config/menus");
const types = require("../types");

module.exports = {
  allMenus: {
    type: new GraphQLList(types.Menu),
    resolve: (_, args, context) => {
      return getAllMenus(context.user);
    }
  },
  menu: {
    type: types.Menu,
    args: {
      id: {
        type: GraphQLString
      }
    },
    resolve: (_, { id }, { user }) => {
      return getMenuById(id, user);
    }
  }
};
