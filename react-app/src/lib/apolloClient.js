import { ApolloClient } from "apollo-client";
import { HttpLink } from "apollo-link-http";
import { setContext } from "apollo-link-context";
import { InMemoryCache } from "apollo-cache-inmemory";
import { getToken } from "./auth";
import config from "../config";

const defaultOptions = {
  watchQuery: {
    fetchPolicy: "network-only",
    errorPolicy: "ignore"
  },
  query: {
    fetchPolicy: "network-only",
    errorPolicy: "all"
  }
};

const httpLink = new HttpLink({
  uri: config.REACT_APP_AIDES_TERRITOIRES_API_URL
});

// ce middleware est chargé d'envoyé à chaque requête GraphQL
// notre token JWT stocké en local storage, permettant ainsi
// d'authentifié les requêtes auprès du serveur
const authMiddleware = setContext(async (operation, { headers }) => {
  try {
    const token = getToken();
    if (!token) return { ...headers };

    return {
      headers: {
        ...headers,
        authorization: `Bearer ${token}`
      }
    };
  } catch (err) {
    console.error(err);
    return headers;
  }
});

const client = new ApolloClient({
  // By default, this client will send queries to the
  //  `/graphql` endpoint on the same host
  // Pass the configuration option { uri: YOUR_GRAPHQL_API_URL } to the `HttpLink` to connect
  // to a different host
  link: authMiddleware.concat(httpLink),
  cache: new InMemoryCache(),
  defaultOptions
});

export default client;
