import React from "react";
import Select from "../../components/ui/finalForm/Select";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { Form, Field } from "react-final-form";

const options = [
  { label: "option 1", value: "option_1" },
  { label: "option 2", value: "option_2" },
  { label: "option 3", value: "option_3" },
  { label: "option 4", value: "option_4" }
];

storiesOf("Final form", module).add("Select", () => (
  <Form
    onSubmit={() => {
      action("submitted");
    }}
    render={({ handleSubmit, submitting, pristine, values, errors, form }) => (
      <form onSubmit={handleSubmit}>
        <Field
          options={options}
          name="Select"
          component={Select}
          label="Select"
        />
      </form>
    )}
  />
));

storiesOf("Final form", module).add("Select multiple", () => (
  <Form
    onSubmit={() => {
      action("submitted");
    }}
    render={({ handleSubmit, submitting, pristine, values, errors, form }) => (
      <form onSubmit={handleSubmit}>
        <p>ajouter une classe "is-multiple" pour rendre le select multiple</p>
        <Field
          className="is-multiple"
          options={options}
          name="Select multiple"
          component={Select}
          label="Select"
        />
      </form>
    )}
  />
));
