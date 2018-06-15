const crypto = require("crypto");
const jwt = require("jsonwebtoken");
const roles = require("../config/permissions").roles;
const allPermissions = require("../config/permissions").permissions;
const User = require("../mongoose/User");
const ForbiddenError = "Forbidden";

// generate a hashpassword :
// console.log(hashPassword("your_password"));

module.exports = {
  getUserByPassword,
  getJwt,
  getUserFromJwt,
  userHasPermission,
  permissionDenied,
  getRoleById
};

function hashPassword(password) {
  return crypto
    .createHmac("sha256", process.env.PASSWORD_HASH_SECRET)
    .update(password)
    .digest("hex");
}

function getUserByPassword(email, password) {
  return User.findOne({ email, password: hashPassword(password) });
}

function getJwt(user) {
  return new Promise((resolve, reject) => {
    jwt.sign(
      {
        id: user.id,
        email: user.email
      },
      process.env.JWT_SECRET,
      {
        expiresIn: "1 days"
      },
      (err, res) => {
        err ? reject(err) : resolve(res);
      }
    );
  });
}

async function getUserFromJwt(token) {
  const { id } = await new Promise((resolve, reject) => {
    jwt.verify(token, process.env.JWT_SECRET, {}, (err, res) => {
      err ? reject(err) : resolve(res);
    });
  });

  return User.findById(id);
}

/**
 * Vérifie si un utilisateur a une permission donnée.
 * @param {*} user
 */
function userHasPermission(user, permissionId = "") {
  if (!user || !user._id || user.roles.length === 0) {
    return false;
  }
  const userPermissions = getPermissionsFromRoles(user.roles);
  console.log(
    "permission",
    permissionId,
    JSON.stringify(userPermissions, 0, 2)
  );
  if (permissionExists(permissionId)) {
    console.log("error : la permission " + permissionId + " n'existe pas");
    return false;
  }
  // on vérifie que cette permission existe puis que l'utilisateur
  // possède bien cette permission sur l'un des rôles qui lui sont attribués
  if (userPermissions.includes(permissionId)) {
    return true;
  }
  console.log("OH NO !");
  return false;
}

function permissionDenied() {
  throw new Error(ForbiddenError);
}

function permissionExists(permissionId) {
  allPermissions.forEach(permission => {
    if (permission.id === permissionId) {
      return true;
    }
  });
  return false;
}

function getRoleById(roleId) {
  let matchedRole = null;
  roles.forEach(role => {
    if (role.id === roleId) {
      matchedRole = role;
    }
  });
  return matchedRole;
}
// un utilisateur peut avoir plusieurs roles
// et chaque role contient une liste de permission.
// Ce qui nous intéresse c'est la liste de toutes les permissions, tous roles
// de l'utilisateur confondus
function getPermissionsFromRoles(rolesIds = []) {
  let permissions = [];
  rolesIds.forEach(roleId => {
    const role = getRoleById(roleId);
    if (role && role.permissions.length > 0) {
      permissions = [...permissions, ...role.permissions];
    }
  });
  const dedupedPermissions = Array.from(new Set(permissions));
  return dedupedPermissions;
}
