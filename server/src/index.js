require("dotenv").config();
const express = require("express");
const graphqlHTTP = require("express-graphql");
const cors = require("cors");
const mongoose = require("mongoose");
const logger = require("./services/logger");
const { getUserFromJwt } = require("./services/user");
const schema = require("./graphql/schema");
// mongoose.set("debug", true);

connectToMongodb()
  .then(() => {
    console.log(`connected successfully to ${process.env.MONGODB_URL} ! `);
    startExpressServer();
  })
  .catch(e => console.error(e));

function connectToMongodb() {
  mongoose.Promise = global.Promise;
  return mongoose.connect(process.env.MONGODB_URL);
}

function auth() {
  return async (req, res, next) => {
    try {
      if (!req.headers.authorization) return next();

      const [type, jwt] = req.headers.authorization.split(" ");
      if (type !== "Bearer") return next();

      req.user = await getUserFromJwt(jwt);
      next();
    } catch (err) {
      next(err);
    }
  };
}

function startExpressServer() {
  const app = express();
  app.use(cors());
  app.use(auth());
  app.use(
    "/graphql",
    graphqlHTTP(req => ({
      schema,
      rootValue: {},
      context: {
        user: req.user
      },
      // always display graphiql explorer for now
      graphiql: true,
      formatError: error => {
        return {
          message: error.message,
          stack:
            process.env.NODE_ENV === "development"
              ? error.stack.split("\n")
              : null
        };
      }
    }))
  );

  app.use("/", (req, res) => {
    res.json("server is running. Go to /graphql.");
  });

  const port = process.env.PORT ? process.env.PORT : 8100;

  app.listen(port);
  logger.info(`Running a GraphQL API server at localhost:${port}/graphql`);
}
