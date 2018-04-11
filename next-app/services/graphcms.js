import config from "./config";
import { GraphQLClient } from "graphql-request";
const client = new GraphQLClient(config.GRAPHCMS_API_URL);
export default client;
