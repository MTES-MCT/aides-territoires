import React from "react";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import SearchForm from "../components/ui/SearchForm";
import { withInfo } from "@storybook/addon-info";

storiesOf("SearchForm", module).add(
  "SearchForm",
  withInfo()(() => (
    <div style={{ padding: "2rem" }}>
      <SearchForm
        value="hello"
        onSubmit={action("form submitted")}
        onChange={action("input value changed")}
        placeholder="Entrez un code postal, une ville, un département ou une région"
      />
    </div>
  ))
);
