import React from "react";
import TextArea from "../../components/ui/finalForm/TextArea";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { Form, Field } from "react-final-form";

storiesOf("Final form", module).add("TextArea", () => (
  <Form
    onSubmit={() => {
      action("submitted");
    }}
    render={({ handleSubmit, submitting, pristine, values, errors, form }) => (
      <form onSubmit={handleSubmit}>
        <Field name="TextArea" component={TextArea} label="TextArea" />
      </form>
    )}
  />
));
