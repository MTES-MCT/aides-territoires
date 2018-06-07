import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { withInfo } from "@storybook/addon-info";
import GraphQLError from "../components/ui/GraphQLError";

storiesOf("GraphQLError", module).add(
  "GraphQLError",
  withInfo(`
   Display details about encountered GraphQLErrors from react-apollo this.props.data.error
  `)(() => (
    <GraphQLError
      error={{
        message: "GraphQL a rencontré une erreur"
      }}
    />
  ))
);
