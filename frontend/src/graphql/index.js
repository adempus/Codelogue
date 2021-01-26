import { ApolloClient, InMemoryCache } from "@apollo/client";
import { HttpLink } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import store from "@/store";

const httpLink = new HttpLink({
  uri: "http://127.0.0.1:5001/graphql"
});

const authMiddleware = setContext(() => ({
  headers: {
    authorization: store.getters.getAccessToken
  }
}));

const link = authMiddleware.concat(httpLink);

const apolloClient = new ApolloClient(
  {
    link,
    cache: new InMemoryCache()
  },
  { fetchPolicy: "cache-and-network" }
);

export default apolloClient;
