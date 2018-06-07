import React from "react";
import TextSuggestions from "../../components/ui/TextSuggestions";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { Form, Field } from "react-final-form";

const suggestions = [
  { label: "suggestion 1", value: "suggestion_1" },
  { label: "suggestion 2", value: "suggestion_2" },
  { label: "suggestion 3", value: "suggestion_3" }
];

storiesOf("Final form", module).add("TextSuggestions", () => (
  <TextSuggestions suggestions={suggestions} />
));
