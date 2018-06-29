require("dotenv").config();
const { hashPassword } = require("./services/user");
const password = process.argv[2];
console.log(`ci-dessous le hash pour le password : ${password}`);
console.log(hashPassword(password));
