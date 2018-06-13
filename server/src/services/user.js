const crypto = require("crypto");
const { promisify } = require("util");
const jwt = require("jsonwebtoken");

const User = require("../mongoose/User");

module.exports = {
  getUserByPassword,
  getJwt,
  getUserFromJwt
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
