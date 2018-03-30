import getConfig from "next/config";
import { GraphQLClient } from "graphql-request";
const { publicRuntimeConfig } = getConfig();
console.log("url", publicRuntimeConfig.GRAPHCMS_API_URL);
const client = new GraphQLClient(publicRuntimeConfig.GRAPHCMS_API_URL);
export default client;
