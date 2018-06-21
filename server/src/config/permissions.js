const roles = [
  {
    id: "admin",
    label: "Admin",
    permissions: ["create_aide", "delete_any_aide", "edit_any_aide"]
  },
  {
    id: "contributeur",
    label: "Contributeur",
    permissions: ["create_aide", "delete_own_aide", "edit_own_aide"]
  }
];

const permissions = [
  {
    id: "create_aide",
    label: "Créer une aide"
  },
  {
    id: "edit_any_aide",
    label: "Créer une aide"
  },
  {
    id: "delete_any_aide",
    label: "Supprimer un aide"
  },
  {
    id: "delete_own_aide",
    label: "Supprimer ses propres aides",
    resolver: (user, args) => {
      const { aide } = args;
      if (!aide.auteur) return false;
      if (user.id === aide.auteur.id) {
        return true;
      }
      return false;
    }
  },
  {
    id: "edit_own_aide",
    label: "éditer ses propres aides",
    resolver: (user, args) => {
      const { aide } = args;
      if (!aide.auteur) return false;
      if (user.id === aide.auteur.id) {
        console.log(user.id, aide.auteur.id);
        return true;
      }
      return false;
    }
  }
];

module.exports = { roles, permissions };
