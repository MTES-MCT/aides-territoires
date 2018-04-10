import { GraphQLClient } from "graphql-request";
const client = new GraphQLClient(process.env.REACT_APP_GRAPHCMS_API_URL);
export default client;
