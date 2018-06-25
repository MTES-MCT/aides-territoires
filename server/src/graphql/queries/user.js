const types = require("../types");
const { GraphQLID, GraphQLObjectType, GraphQLString } = require("graphql");
const {
  getPermissionsFromRoles,
  userHasRole,
  permissionDenied,
  hashPassword
} = require("../../services/user");

// query pour le user actuellement connecté
module.exports = {
  user: {
    type: types.User,
    args: {
      id: {
        type: GraphQLID
      }
    },
    resolve: (_, args, { user }) => {
      const result = {
        id: user.id,
        name: user.name,
        roles: user.roles,
        email: user.email,
        // on ajoute les permissions, qui peuvent être parfois utiles en front
        // pour afficher ou pas certains élements de l'UI
        // exemple : this.props.user.permission.includes('publish_aide') && <Component />
        // !DEPRECATED certaines permissions ont besoin d'un argument
        // !seule la fonction userHasPermission() permet une vérification complète
        permissions: getPermissionsFromRoles(user.roles)
      };
      return result;
    }
  },
  generatePassword: {
    type: new GraphQLObjectType({
      name: "generatePassword",
      description:
        "générer un hash de password à partir d'un password en clair. ",
      fields: {
        hash: { type: GraphQLString }
      }
    }),
    args: {
      password: {
        type: GraphQLString
      }
    },
    resolve: (_, { password }, { user }) => {
      if (!userHasRole(user, "admin")) {
        permissionDenied();
      }
      return { hash: hashPassword(password) };
    }
  }
};
