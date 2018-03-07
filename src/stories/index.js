import React from "react";
import "bulma/css/bulma.css";

import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { linkTo } from "@storybook/addon-links";

import { Button, Welcome } from "@storybook/react/demo";
import PageLoader from "../features/app/components/presentationals/pageLoader/PageLoader";
import Header from "../features/app/components/presentationals/header/Header";
import SearchForm from "../features/search/components/presentationals/searchForm/SearchForm";
import SearchFormContainer from "../features/search/components/containers/searchFormContainer/SearchFormContainer";

storiesOf("Header", module).add("Header", () => <Header />);
storiesOf("PageLoader", module).add("PageLoader without text", () => (
  <PageLoader />
));
storiesOf("PageLoader", module).add("PageLoader with text", () => (
  <PageLoader>Chargement en cours ...</PageLoader>
));

storiesOf("SearchForm", module).add("SearchForm", () => (
  <SearchForm
    suggestions={[]}
    onSearchSubmit={action("onSearchSubmit")}
    onSearchChange={action("onSearchChange")}
  />
));

storiesOf("SearchFormContainer", module).add(
  "SearchForm with autocompletion via API",
  () => <SearchFormContainer onSearchSubmit={action("onSearchSubmit")} />
);
