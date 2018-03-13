import React from "react";
import SearchForm from "./SearchForm";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";

storiesOf("SearchForm", module).add("SearchForm", () => (
  <SearchForm
    suggestions={[]}
    onSearchSubmit={action("onSearchSubmit")}
    onSearchChange={action("onSearchChange")}
  />
));
