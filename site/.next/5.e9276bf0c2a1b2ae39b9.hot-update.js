webpackHotUpdate(5,{

/***/ "./components/ui/Header.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link__ = __webpack_require__("./node_modules/next/link.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__ui_ButtonLink__ = __webpack_require__("./components/ui/ButtonLink.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types__ = __webpack_require__("./node_modules/next/node_modules/prop-types/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_prop_types___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_prop_types__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_react_jss__ = __webpack_require__("./node_modules/react-jss/lib/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_react_jss___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_react_jss__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Header.js";

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();







var Header = function Header(_ref) {
  var classes = _ref.classes,
      title = _ref.title,
      subtitle = _ref.subtitle,
      callToActionText = _ref.callToActionText,
      callToActionLink = _ref.callToActionLink;
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("header", {
    className: classes.header,
    id: "aides-territoires",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 15
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    className: classes.headerOverlay,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 16
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
    className: classes.content,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 17
    }
  }, __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("h1", {
    className: classes.title,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 18
    }
  }, title), __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("h2", {
    className: classes.subtitle,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 19
    }
  }, subtitle), callToActionText && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_2__ui_ButtonLink__["a" /* default */], {
    href: callToActionLink,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 21
    }
  }, callToActionText))));
};

Header.propTypes = {
  title: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string.isRequired,
  backgroundImageUrl: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string,
  subtitle: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.oneOfType([__WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string, __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.element]),
  callToActionText: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string,
  callToActionLink: __WEBPACK_IMPORTED_MODULE_3_prop_types___default.a.string
};
var styles = {
  header: {
    color: "white",
    position: "relative",
    backgroundImage: function backgroundImage(_ref2) {
      var backgroundImageUrl = _ref2.backgroundImageUrl;
      return "url(".concat(backgroundImageUrl, ")");
    },
    backgroundSize: "cover",
    backgroundPosition: "bottom",
    textAlign: "center",
    height: "400px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
  title: {
    color: "white"
  },
  headerOverlay: {
    paddingBottom: "5rem",
    display: "flex",
    flexDirection: "column",
    position: "absolute",
    justifyContent: "center",
    alignItems: "center",
    top: 0,
    left: 0,
    height: "100%",
    width: "100%",
    background: "rgba(20, 20, 20, 0.4)"
    /*
    subtitle: { color: "white", fontSize: "1rem" },
    button: { color: "white" }
    */

  }
};

var _default = __WEBPACK_IMPORTED_MODULE_4_react_jss___default()(styles)(Header);

/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(Header, "Header", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Header.js");
  reactHotLoader.register(styles, "styles", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Header.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/site/components/ui/Header.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ })

})
//# sourceMappingURL=5.e9276bf0c2a1b2ae39b9.hot-update.js.map