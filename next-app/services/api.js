import config from "./config";
import { GraphQLClient } from "graphql-request";
const client = new GraphQLClient(config.GRAPHQL_URL);
export default client;
