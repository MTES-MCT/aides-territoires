import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { withInfo } from "@storybook/addon-info";
import SearchFormAidesTerritoires from "../components/ui/SearchFormAidesTerritoires";

storiesOf("SearchFormAidesTerritoires", module).add(
  "SearchFormAidesTerritoires",
  withInfo()(() => (
    <div style={{ padding: "2rem" }}>
      <SearchFormAidesTerritoires
        onSubmit={action("form submitted")}
        onClick={action("suggestion clicked")}
      />
    </div>
  ))
);
