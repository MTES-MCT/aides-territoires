webpackHotUpdate(5,{

/***/ "./components/ui/ButtonLink.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react_jss__ = __webpack_require__("./node_modules/react-jss/lib/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_react_jss__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ui_config__ = __webpack_require__("./ui.config.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_next_link__ = __webpack_require__("./node_modules/next/link.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_prop_types__ = __webpack_require__("./node_modules/next/node_modules/prop-types/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_prop_types__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/ButtonLink.js";

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }







var ButtonLink = function ButtonLink(_ref) {
  var classes = _ref.classes,
      children = _ref.children,
      href = _ref.href;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_3_next_link___default.a, {
    href: href,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 9
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("a", {
    className: classes.a,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 10
    }
  }, children));
};

ButtonLink.propTypes = {
  href: __WEBPACK_IMPORTED_MODULE_4_prop_types___default.a.string.isRequired,
  type: __WEBPACK_IMPORTED_MODULE_4_prop_types___default.a.oneOf(["primary", "secondary"])
};
var styles = {
  a: _defineProperty({
    textDecoration: "none",
    borderRadius: "5px",
    color: "white",
    fontSize: "24px",
    display: "inline-block",
    padding: "1.5rem 1.5rem",
    background: function background(_ref2) {
      var type = _ref2.type;
      var color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.primaryLight;

      if (type === "secondary") {
        color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.secondary;
      }

      return color;
    }
  }, "color", function color(_ref3) {
    var type = _ref3.type;
    var color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.primary;

    if (type === "primary") {
      color = __WEBPACK_IMPORTED_MODULE_2__ui_config__["a" /* default */].colors.secondary;
    }

    return color;
  })
};

var _default = __WEBPACK_IMPORTED_MODULE_1_react_jss___default()(styles)(ButtonLink);

/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(ButtonLink, "ButtonLink", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/ButtonLink.js");
  reactHotLoader.register(styles, "styles", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/ButtonLink.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/ButtonLink.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ })

})
//# sourceMappingURL=5.e9cf93d645e1dace7261.hot-update.js.map