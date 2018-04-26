const { reduce } = require("lodash");

module.exports = {};

const modules = require("require-dir")(__dirname, { camelcase: true });

Object.assign(
  module.exports,
  reduce(modules, (acc, group) => Object.assign(acc, group), {})
);
