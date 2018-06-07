import React from "react";
import ImageVilleDurable from "../../components/ui/brand/ImageVilleDurable";
import { storiesOf } from "@storybook/react";
import { action } from "@storybook/addon-actions";
import { withInfo } from "@storybook/addon-info";

storiesOf("brand", module).add(
  "Image Ville durable",
  withInfo()(() => <ImageVilleDurable />)
);
