import getConfig from "next/config";
import { GraphQLClient } from "graphql-request";
const { publicRuntimeConfig } = getConfig();
const client = new GraphQLClient(publicRuntimeConfig.GRAPHQL_URL);
export default client;
