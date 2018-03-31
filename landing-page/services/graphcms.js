import getConfig from "next/config";
import { GraphQLClient } from "graphql-request";
import cache from "../services/cache";
const { publicRuntimeConfig } = getConfig();
const client = new GraphQLClient(publicRuntimeConfig.GRAPHCMS_API_URL);
const cacheTime = 10000;
// helper to cache result for 10 minutes
client.requestWithCache = (cacheId, query, variables = {}) => {
  if (cache.get(cacheId)) {
    return cache.get(cacheId);
  }
  return client.request(query, variables).then(data => {
    cache.set(cacheId, data, cacheTime);
    return data;
  });
};
export default client;
