module.exports =

        __NEXT_REGISTER_PAGE('/', function() {
          var comp = 
      webpackJsonp([3],{

/***/ "./components/DefaultLayout.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__Navigation__ = __webpack_require__("./components/Navigation.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head__ = __webpack_require__("./node_modules/next/head.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_head__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__Header__ = __webpack_require__("./components/Header.js");
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/DefaultLayout.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }






var DefaultLayout = function (_React$Component) {
  _inherits(DefaultLayout, _React$Component);

  function DefaultLayout() {
    _classCallCheck(this, DefaultLayout);

    return _possibleConstructorReturn(this, (DefaultLayout.__proto__ || Object.getPrototypeOf(DefaultLayout)).apply(this, arguments));
  }

  _createClass(DefaultLayout, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "div",
        { className: "default-layout", __source: {
            fileName: _jsxFileName,
            lineNumber: 9
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          __WEBPACK_IMPORTED_MODULE_2_next_head___default.a,
          {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 10
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("meta", {
            name: "viewport",
            content: "initial-scale=1.0, width=device-width",
            __source: {
              fileName: _jsxFileName,
              lineNumber: 11
            }
          }),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", { rel: "stylesheet", href: "/static/css/bulma.css", __source: {
              fileName: _jsxFileName,
              lineNumber: 15
            }
          }),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", { rel: "stylesheet", href: "/static/css/style.css", __source: {
              fileName: _jsxFileName,
              lineNumber: 16
            }
          })
        ),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_1__Navigation__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 18
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_3__Header__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 19
          }
        }),
        this.props.children
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return DefaultLayout;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = DefaultLayout;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(DefaultLayout, "DefaultLayout", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/DefaultLayout.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/DefaultLayout.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/Header.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Header.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var Header = function (_React$Component) {
  _inherits(Header, _React$Component);

  function Header() {
    _classCallCheck(this, Header);

    return _possibleConstructorReturn(this, (Header.__proto__ || Object.getPrototypeOf(Header)).apply(this, arguments));
  }

  _createClass(Header, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "aides-territoires", className: "hero ", __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "header",
          { className: "header ", __source: {
              fileName: _jsxFileName,
              lineNumber: 7
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "header-overlay ", __source: {
                fileName: _jsxFileName,
                lineNumber: 8
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "hero-body ", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 9
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "container ", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 10
                  }
                },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h1",
                  { className: "title ", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 11
                    }
                  },
                  "UN OUTIL POUR LES COLLECTIVIT\xC9S"
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "subtitle ", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 12
                    }
                  },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                    "p",
                    {
                      __source: {
                        fileName: _jsxFileName,
                        lineNumber: 13
                      }
                    },
                    "Identifiez en quelques clics toutes les aides disponibles sur votre territoire pour vos projets d'am\xE9nagements durables.",
                    __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", {
                      __source: {
                        fileName: _jsxFileName,
                        lineNumber: 17
                      }
                    }),
                    __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", {
                      __source: {
                        fileName: _jsxFileName,
                        lineNumber: 18
                      }
                    }),
                    " Un service actuellement exp\xE9riment\xE9 pour les projets de quartiers durables, dont les EcoQuartiers."
                  )
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "button is-large is-primary ", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 22
                    }
                  },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                    "a",
                    {
                      className: "button-lancez-la-recherche js-scrollTo ",
                      href: "#inscription",
                      __source: {
                        fileName: _jsxFileName,
                        lineNumber: 23
                      }
                    },
                    "Lancez votre recherche"
                  )
                )
              )
            )
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return Header;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = Header;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(Header, "Header", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Header.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Header.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/Navigation.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Navigation.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var Navigation = function (_React$Component) {
  _inherits(Navigation, _React$Component);

  function Navigation() {
    _classCallCheck(this, Navigation);

    return _possibleConstructorReturn(this, (Navigation.__proto__ || Object.getPrototypeOf(Navigation)).apply(this, arguments));
  }

  _createClass(Navigation, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "nav",
        {
          className: "navbar is-fixed-top app-main-menu",
          role: "navigation",
          "aria-label": "main navigation",
          __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "navbar-brand", __source: {
              fileName: _jsxFileName,
              lineNumber: 11
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "a",
            { className: "navbar-item js-scrollTo", href: "#aides-territoires", __source: {
                fileName: _jsxFileName,
                lineNumber: 12
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/logo.png ", __source: {
                fileName: _jsxFileName,
                lineNumber: 13
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "p",
              { className: "app-name ", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 14
                }
              },
              "Aides-territoires"
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "navbar-burger", "data-target": "navMenu ", __source: {
                fileName: _jsxFileName,
                lineNumber: 16
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 17
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 18
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 19
              }
            })
          )
        ),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "navbar-menu", id: "navMenu ", __source: {
              fileName: _jsxFileName,
              lineNumber: 22
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "navbar-end", __source: {
                fileName: _jsxFileName,
                lineNumber: 23
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#aides-territoires", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 24
                }
              },
              "Aides-territoires"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#comment-ca-marche", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 27
                }
              },
              "Le service"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#inscription", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 30
                }
              },
              "Inscription"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#contact", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 33
                }
              },
              "Contact"
            )
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return Navigation;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = Navigation;


/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(Navigation, "Navigation", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Navigation.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Navigation.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/SectionBenefices.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionBenefices.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionBenefices = function (_React$Component) {
  _inherits(SectionBenefices, _React$Component);

  function SectionBenefices() {
    _classCallCheck(this, SectionBenefices);

    return _possibleConstructorReturn(this, (SectionBenefices.__proto__ || Object.getPrototypeOf(SectionBenefices)).apply(this, arguments));
  }

  _createClass(SectionBenefices, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "benefices", className: "section ", __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container", __source: {
              fileName: _jsxFileName,
              lineNumber: 7
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "content ", __source: {
                fileName: _jsxFileName,
                lineNumber: 8
              }
            },
            "Avec Aides-territoires :",
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "ul",
              {
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 10
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "li",
                {
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 11
                  }
                },
                " ",
                "Gagnez du temps dans votre recherche d'aides, de l'accompagnement au financement"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "li",
                {
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 16
                  }
                },
                " ",
                "Ne passez plus \xE0 c\xF4t\xE9 des aides qui correspondent \xE0 votre projet"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "li",
                {
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 20
                  }
                },
                "B\xE9n\xE9ficiez d'une s\xE9lection pertinente \xE0 chaque \xE9tape de votre projet"
              )
            )
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return SectionBenefices;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = SectionBenefices;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(SectionBenefices, "SectionBenefices", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionBenefices.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionBenefices.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/SectionChronophage.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionChronophage.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionChronophage = function (_React$Component) {
  _inherits(SectionChronophage, _React$Component);

  function SectionChronophage() {
    _classCallCheck(this, SectionChronophage);

    return _possibleConstructorReturn(this, (SectionChronophage.__proto__ || Object.getPrototypeOf(SectionChronophage)).apply(this, arguments));
  }

  _createClass(SectionChronophage, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "chronophage", className: "section ", __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container ", __source: {
              fileName: _jsxFileName,
              lineNumber: 7
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "p",
            {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 8
              }
            },
            "L'acc\xE8s aux aides publiques disponibles et pertinentes pour vos projets est trop souvent synonyme de veille chronophage au d\xE9triment du temps pass\xE9 sur le projet en lui-m\xEAme."
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return SectionChronophage;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = SectionChronophage;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(SectionChronophage, "SectionChronophage", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionChronophage.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionChronophage.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/SectionCommentCaMarche.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionCommentCaMarche.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionCommentCaMarche = function (_React$Component) {
  _inherits(SectionCommentCaMarche, _React$Component);

  function SectionCommentCaMarche() {
    _classCallCheck(this, SectionCommentCaMarche);

    return _possibleConstructorReturn(this, (SectionCommentCaMarche.__proto__ || Object.getPrototypeOf(SectionCommentCaMarche)).apply(this, arguments));
  }

  _createClass(SectionCommentCaMarche, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "comment-ca-marche", className: "section", __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container ", __source: {
              fileName: _jsxFileName,
              lineNumber: 7
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "h2",
            { className: "section-title title is-3", __source: {
                fileName: _jsxFileName,
                lineNumber: 8
              }
            },
            "Comment \xE7a marche ?"
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "columns", __source: {
                fileName: _jsxFileName,
                lineNumber: 9
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 10
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 11
                  }
                },
                "1"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 12
                  }
                },
                "Un territoire, un projet"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "p",
                {
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 13
                  }
                },
                "Donnez nous votre localisation et votre projet "
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 15
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 16
                  }
                },
                "2"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 17
                  }
                },
                "Des aides"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "p",
                {
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 18
                  }
                },
                "Nous vous aidons \xE0 identifier les meilleures aides publiques mobilisables"
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 23
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 24
                  }
                },
                "3"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 25
                  }
                },
                "Du temps gagn\xE9"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "p",
                {
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 26
                  }
                },
                "passez plus de temps sur votre projet en activant les aides pertinentes au bon moment"
              )
            )
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return SectionCommentCaMarche;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = SectionCommentCaMarche;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(SectionCommentCaMarche, "SectionCommentCaMarche", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionCommentCaMarche.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionCommentCaMarche.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/SectionTypesAides.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionTypesAides.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SectionTypeAides = function (_React$Component) {
  _inherits(SectionTypeAides, _React$Component);

  function SectionTypeAides() {
    _classCallCheck(this, SectionTypeAides);

    return _possibleConstructorReturn(this, (SectionTypeAides.__proto__ || Object.getPrototypeOf(SectionTypeAides)).apply(this, arguments));
  }

  _createClass(SectionTypeAides, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "types-aides", className: "section", __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "container", __source: {
              fileName: _jsxFileName,
              lineNumber: 7
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "p",
            { className: "text", __source: {
                fileName: _jsxFileName,
                lineNumber: 8
              }
            },
            "Quelque soit le stade d'avancement de votre projet d'\xC9coQuartier, Aides-territoires vous permet d'identifier les aides pertinentes:"
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "content ", __source: {
                fileName: _jsxFileName,
                lineNumber: 12
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "columns", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 13
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "column", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 14
                  }
                },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "aides-icon", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 15
                    }
                  },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/icon-compas.png", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 16
                    }
                  })
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "title is-4", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 18
                    }
                  },
                  "Ing\xE9nierie"
                )
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "column", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 20
                  }
                },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "aides-icon", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 21
                    }
                  },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/icon-financement.png", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 22
                    }
                  })
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "title is-4", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 24
                    }
                  },
                  "Financement"
                )
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "column", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 26
                  }
                },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "aides-icon", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 27
                    }
                  },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/icon-journal.png", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 28
                    }
                  })
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "title is-4", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 30
                    }
                  },
                  "Appels \xE0 projet"
                )
              )
            )
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return SectionTypeAides;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = SectionTypeAides;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(SectionTypeAides, "SectionTypeAides", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionTypesAides.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionTypesAides.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/SendInBlueContactForm.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request__ = __webpack_require__("./node_modules/graphql-request/dist/src/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_graphql_request__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_config__ = __webpack_require__("./node_modules/next/config.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_config___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_config__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }





var _getConfig = __WEBPACK_IMPORTED_MODULE_2_next_config___default()(),
    publicRuntimeConfig = _getConfig.publicRuntimeConfig;

var EMAIL_SENDING_STATUS_NOT_STARTED = "not_started";
var EMAIL_SENDING_STATUS_PENDING = "pending";
var EMAIL_SENDING_STATUS_SENT = "sent";
var EMAIL_SENDING_STATUS_ERROR = "error";

var ContactForm = function (_React$Component) {
  _inherits(ContactForm, _React$Component);

  function ContactForm(props) {
    _classCallCheck(this, ContactForm);

    var _this = _possibleConstructorReturn(this, (ContactForm.__proto__ || Object.getPrototypeOf(ContactForm)).call(this, props));

    _this.handleSubmit = function (event) {
      event.preventDefault();
      _this.setState({
        emailSendingStatus: EMAIL_SENDING_STATUS_PENDING
      });
      _this.sendEmail().then(function (r) {
        _this.setState({
          emailSendingStatus: EMAIL_SENDING_STATUS_SENT
        });
      }).catch(function (e) {
        _this.setState({
          emailSendingStatus: EMAIL_SENDING_STATUS_ERROR
        });
      });
    };

    _this.onEmailChange = function (event) {
      _this.setState({ email: event.target.value });
    };

    _this.onMessageChange = function (event) {
      _this.setState({ message: event.target.value });
    };

    _this.state = {
      email: "",
      message: "",
      emailSendingStatus: EMAIL_SENDING_STATUS_NOT_STARTED
    };
    return _this;
  }

  _createClass(ContactForm, [{
    key: "sendEmail",
    value: function sendEmail() {
      var query = "\n    mutation sendContactFormEmail($from:String!,$text:String!) {\n      sendContactFormEmail(from: $from, text:$text) {\n        from\n        text\n      }\n    }";
      var variables = {
        from: this.state.email,
        text: this.state.message
      };
      return Object(__WEBPACK_IMPORTED_MODULE_1_graphql_request__["request"])(publicRuntimeConfig.GRAPHQL_URL, query, variables);
    }
  }, {
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "div",
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 59
          }
        },
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_ERROR && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 61
            }
          },
          "D\xE9sol\xE9 nous avons rencontr\xE9 une erreur lors de l'envoi de l'email. Vous pouvez nous contacter \xE0 l'addresse suivante :",
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "strong",
            {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 64
              }
            },
            "contact@aides-territoires.beta.gouv.fr"
          ),
          " ou",
          " ",
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "strong",
            {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 65
              }
            },
            "elise.marion@beta.gouv.fr"
          )
        ),
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "section message is-success", __source: {
              fileName: _jsxFileName,
              lineNumber: 69
            }
          },
          "Merci! Votre message a bien \xE9t\xE9 envoy\xE9."
        ),
        this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_ERROR && this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "form",
          { id: "contact-form", onSubmit: this.handleSubmit, __source: {
              fileName: _jsxFileName,
              lineNumber: 76
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field", __source: {
                fileName: _jsxFileName,
                lineNumber: 77
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "label",
              { className: "label", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 78
                }
              },
              "Votre email*"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 79
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("input", {
                id: "email",
                onChange: this.onEmailChange,
                className: "input is-large",
                type: "text",
                placeholder: "Email",
                required: true,
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 80
                }
              })
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field", __source: {
                fileName: _jsxFileName,
                lineNumber: 91
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "label",
              { className: "label", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 92
                }
              },
              "Votre message"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 93
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("textarea", {
                onChange: this.onMessageChange,
                id: "message",
                className: "textarea",
                placeholder: "Votre message",
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 94
                }
              })
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field is-grouped is-grouped-right", __source: {
                fileName: _jsxFileName,
                lineNumber: 103
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 104
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("input", {
                type: "submit",
                value: "envoyer",
                className: "button is-link is-large is-primary",
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 105
                }
              })
            )
          )
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return ContactForm;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = ContactForm;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(publicRuntimeConfig, "publicRuntimeConfig", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js");
  reactHotLoader.register(EMAIL_SENDING_STATUS_NOT_STARTED, "EMAIL_SENDING_STATUS_NOT_STARTED", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js");
  reactHotLoader.register(EMAIL_SENDING_STATUS_PENDING, "EMAIL_SENDING_STATUS_PENDING", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js");
  reactHotLoader.register(EMAIL_SENDING_STATUS_SENT, "EMAIL_SENDING_STATUS_SENT", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js");
  reactHotLoader.register(EMAIL_SENDING_STATUS_ERROR, "EMAIL_SENDING_STATUS_ERROR", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js");
  reactHotLoader.register(ContactForm, "ContactForm", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./components/SendInBlueInscrivezVous.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueInscrivezVous.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var SendInBlueInscrivezVous = function (_React$Component) {
  _inherits(SendInBlueInscrivezVous, _React$Component);

  function SendInBlueInscrivezVous() {
    _classCallCheck(this, SendInBlueInscrivezVous);

    return _possibleConstructorReturn(this, (SendInBlueInscrivezVous.__proto__ || Object.getPrototypeOf(SendInBlueInscrivezVous)).apply(this, arguments));
  }

  _createClass(SendInBlueInscrivezVous, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "inscription", className: "section lancez-votre-recherche", __source: {
            fileName: _jsxFileName,
            lineNumber: 6
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("iframe", {
          width: "540",
          height: "723",
          src: "https://my.sendinblue.com/users/subscribe/js_id/35zg8/id/1",
          frameBorder: "0",
          scrolling: "auto",
          allowFullScreen: true,
          style: {
            background: "transparent",
            display: "block",
            marginLeft: "auto",
            marginRight: "auto",
            maXidth: "100%"
          },
          __source: {
            fileName: _jsxFileName,
            lineNumber: 7
          }
        })
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return SendInBlueInscrivezVous;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = SendInBlueInscrivezVous;
/* harmony default export */ __webpack_exports__["a"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(SendInBlueInscrivezVous, "SendInBlueInscrivezVous", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueInscrivezVous.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueInscrivezVous.js");
  leaveModule(module);
})();

;
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ "./node_modules/cross-fetch/dist/browser-polyfill.js":
/***/ (function(module, exports) {

(function(self) {

  if (self.fetch) {
    return
  }

  var support = {
    searchParams: 'URLSearchParams' in self,
    iterable: 'Symbol' in self && 'iterator' in Symbol,
    blob: 'FileReader' in self && 'Blob' in self && (function() {
      try {
        new Blob();
        return true
      } catch(e) {
        return false
      }
    })(),
    formData: 'FormData' in self,
    arrayBuffer: 'ArrayBuffer' in self
  };

  if (support.arrayBuffer) {
    var viewClasses = [
      '[object Int8Array]',
      '[object Uint8Array]',
      '[object Uint8ClampedArray]',
      '[object Int16Array]',
      '[object Uint16Array]',
      '[object Int32Array]',
      '[object Uint32Array]',
      '[object Float32Array]',
      '[object Float64Array]'
    ];

    var isDataView = function(obj) {
      return obj && DataView.prototype.isPrototypeOf(obj)
    };

    var isArrayBufferView = ArrayBuffer.isView || function(obj) {
      return obj && viewClasses.indexOf(Object.prototype.toString.call(obj)) > -1
    };
  }

  function normalizeName(name) {
    if (typeof name !== 'string') {
      name = String(name);
    }
    if (/[^a-z0-9\-#$%&'*+.\^_`|~]/i.test(name)) {
      throw new TypeError('Invalid character in header field name')
    }
    return name.toLowerCase()
  }

  function normalizeValue(value) {
    if (typeof value !== 'string') {
      value = String(value);
    }
    return value
  }

  // Build a destructive iterator for the value list
  function iteratorFor(items) {
    var iterator = {
      next: function() {
        var value = items.shift();
        return {done: value === undefined, value: value}
      }
    };

    if (support.iterable) {
      iterator[Symbol.iterator] = function() {
        return iterator
      };
    }

    return iterator
  }

  function Headers(headers) {
    this.map = {};

    if (headers instanceof Headers) {
      headers.forEach(function(value, name) {
        this.append(name, value);
      }, this);
    } else if (Array.isArray(headers)) {
      headers.forEach(function(header) {
        this.append(header[0], header[1]);
      }, this);
    } else if (headers) {
      Object.getOwnPropertyNames(headers).forEach(function(name) {
        this.append(name, headers[name]);
      }, this);
    }
  }

  Headers.prototype.append = function(name, value) {
    name = normalizeName(name);
    value = normalizeValue(value);
    var oldValue = this.map[name];
    this.map[name] = oldValue ? oldValue+','+value : value;
  };

  Headers.prototype['delete'] = function(name) {
    delete this.map[normalizeName(name)];
  };

  Headers.prototype.get = function(name) {
    name = normalizeName(name);
    return this.has(name) ? this.map[name] : null
  };

  Headers.prototype.has = function(name) {
    return this.map.hasOwnProperty(normalizeName(name))
  };

  Headers.prototype.set = function(name, value) {
    this.map[normalizeName(name)] = normalizeValue(value);
  };

  Headers.prototype.forEach = function(callback, thisArg) {
    for (var name in this.map) {
      if (this.map.hasOwnProperty(name)) {
        callback.call(thisArg, this.map[name], name, this);
      }
    }
  };

  Headers.prototype.keys = function() {
    var items = [];
    this.forEach(function(value, name) { items.push(name); });
    return iteratorFor(items)
  };

  Headers.prototype.values = function() {
    var items = [];
    this.forEach(function(value) { items.push(value); });
    return iteratorFor(items)
  };

  Headers.prototype.entries = function() {
    var items = [];
    this.forEach(function(value, name) { items.push([name, value]); });
    return iteratorFor(items)
  };

  if (support.iterable) {
    Headers.prototype[Symbol.iterator] = Headers.prototype.entries;
  }

  function consumed(body) {
    if (body.bodyUsed) {
      return Promise.reject(new TypeError('Already read'))
    }
    body.bodyUsed = true;
  }

  function fileReaderReady(reader) {
    return new Promise(function(resolve, reject) {
      reader.onload = function() {
        resolve(reader.result);
      };
      reader.onerror = function() {
        reject(reader.error);
      };
    })
  }

  function readBlobAsArrayBuffer(blob) {
    var reader = new FileReader();
    var promise = fileReaderReady(reader);
    reader.readAsArrayBuffer(blob);
    return promise
  }

  function readBlobAsText(blob) {
    var reader = new FileReader();
    var promise = fileReaderReady(reader);
    reader.readAsText(blob);
    return promise
  }

  function readArrayBufferAsText(buf) {
    var view = new Uint8Array(buf);
    var chars = new Array(view.length);

    for (var i = 0; i < view.length; i++) {
      chars[i] = String.fromCharCode(view[i]);
    }
    return chars.join('')
  }

  function bufferClone(buf) {
    if (buf.slice) {
      return buf.slice(0)
    } else {
      var view = new Uint8Array(buf.byteLength);
      view.set(new Uint8Array(buf));
      return view.buffer
    }
  }

  function Body() {
    this.bodyUsed = false;

    this._initBody = function(body) {
      this._bodyInit = body;
      if (!body) {
        this._bodyText = '';
      } else if (typeof body === 'string') {
        this._bodyText = body;
      } else if (support.blob && Blob.prototype.isPrototypeOf(body)) {
        this._bodyBlob = body;
      } else if (support.formData && FormData.prototype.isPrototypeOf(body)) {
        this._bodyFormData = body;
      } else if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
        this._bodyText = body.toString();
      } else if (support.arrayBuffer && support.blob && isDataView(body)) {
        this._bodyArrayBuffer = bufferClone(body.buffer);
        // IE 10-11 can't handle a DataView body.
        this._bodyInit = new Blob([this._bodyArrayBuffer]);
      } else if (support.arrayBuffer && (ArrayBuffer.prototype.isPrototypeOf(body) || isArrayBufferView(body))) {
        this._bodyArrayBuffer = bufferClone(body);
      } else {
        throw new Error('unsupported BodyInit type')
      }

      if (!this.headers.get('content-type')) {
        if (typeof body === 'string') {
          this.headers.set('content-type', 'text/plain;charset=UTF-8');
        } else if (this._bodyBlob && this._bodyBlob.type) {
          this.headers.set('content-type', this._bodyBlob.type);
        } else if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
          this.headers.set('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        }
      }
    };

    if (support.blob) {
      this.blob = function() {
        var rejected = consumed(this);
        if (rejected) {
          return rejected
        }

        if (this._bodyBlob) {
          return Promise.resolve(this._bodyBlob)
        } else if (this._bodyArrayBuffer) {
          return Promise.resolve(new Blob([this._bodyArrayBuffer]))
        } else if (this._bodyFormData) {
          throw new Error('could not read FormData body as blob')
        } else {
          return Promise.resolve(new Blob([this._bodyText]))
        }
      };

      this.arrayBuffer = function() {
        if (this._bodyArrayBuffer) {
          return consumed(this) || Promise.resolve(this._bodyArrayBuffer)
        } else {
          return this.blob().then(readBlobAsArrayBuffer)
        }
      };
    }

    this.text = function() {
      var rejected = consumed(this);
      if (rejected) {
        return rejected
      }

      if (this._bodyBlob) {
        return readBlobAsText(this._bodyBlob)
      } else if (this._bodyArrayBuffer) {
        return Promise.resolve(readArrayBufferAsText(this._bodyArrayBuffer))
      } else if (this._bodyFormData) {
        throw new Error('could not read FormData body as text')
      } else {
        return Promise.resolve(this._bodyText)
      }
    };

    if (support.formData) {
      this.formData = function() {
        return this.text().then(decode)
      };
    }

    this.json = function() {
      return this.text().then(JSON.parse)
    };

    return this
  }

  // HTTP methods whose capitalization should be normalized
  var methods = ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST', 'PUT'];

  function normalizeMethod(method) {
    var upcased = method.toUpperCase();
    return (methods.indexOf(upcased) > -1) ? upcased : method
  }

  function Request(input, options) {
    options = options || {};
    var body = options.body;

    if (input instanceof Request) {
      if (input.bodyUsed) {
        throw new TypeError('Already read')
      }
      this.url = input.url;
      this.credentials = input.credentials;
      if (!options.headers) {
        this.headers = new Headers(input.headers);
      }
      this.method = input.method;
      this.mode = input.mode;
      if (!body && input._bodyInit != null) {
        body = input._bodyInit;
        input.bodyUsed = true;
      }
    } else {
      this.url = String(input);
    }

    this.credentials = options.credentials || this.credentials || 'omit';
    if (options.headers || !this.headers) {
      this.headers = new Headers(options.headers);
    }
    this.method = normalizeMethod(options.method || this.method || 'GET');
    this.mode = options.mode || this.mode || null;
    this.referrer = null;

    if ((this.method === 'GET' || this.method === 'HEAD') && body) {
      throw new TypeError('Body not allowed for GET or HEAD requests')
    }
    this._initBody(body);
  }

  Request.prototype.clone = function() {
    return new Request(this, { body: this._bodyInit })
  };

  function decode(body) {
    var form = new FormData();
    body.trim().split('&').forEach(function(bytes) {
      if (bytes) {
        var split = bytes.split('=');
        var name = split.shift().replace(/\+/g, ' ');
        var value = split.join('=').replace(/\+/g, ' ');
        form.append(decodeURIComponent(name), decodeURIComponent(value));
      }
    });
    return form
  }

  function parseHeaders(rawHeaders) {
    var headers = new Headers();
    rawHeaders.split(/\r?\n/).forEach(function(line) {
      var parts = line.split(':');
      var key = parts.shift().trim();
      if (key) {
        var value = parts.join(':').trim();
        headers.append(key, value);
      }
    });
    return headers
  }

  Body.call(Request.prototype);

  function Response(bodyInit, options) {
    if (!options) {
      options = {};
    }

    this.type = 'default';
    this.status = 'status' in options ? options.status : 200;
    this.ok = this.status >= 200 && this.status < 300;
    this.statusText = 'statusText' in options ? options.statusText : 'OK';
    this.headers = new Headers(options.headers);
    this.url = options.url || '';
    this._initBody(bodyInit);
  }

  Body.call(Response.prototype);

  Response.prototype.clone = function() {
    return new Response(this._bodyInit, {
      status: this.status,
      statusText: this.statusText,
      headers: new Headers(this.headers),
      url: this.url
    })
  };

  Response.error = function() {
    var response = new Response(null, {status: 0, statusText: ''});
    response.type = 'error';
    return response
  };

  var redirectStatuses = [301, 302, 303, 307, 308];

  Response.redirect = function(url, status) {
    if (redirectStatuses.indexOf(status) === -1) {
      throw new RangeError('Invalid status code')
    }

    return new Response(null, {status: status, headers: {location: url}})
  };

  self.Headers = Headers;
  self.Request = Request;
  self.Response = Response;

  self.fetch = function(input, init) {
    return new Promise(function(resolve, reject) {
      var request = new Request(input, init);
      var xhr = new XMLHttpRequest();

      xhr.onload = function() {
        var options = {
          status: xhr.status,
          statusText: xhr.statusText,
          headers: parseHeaders(xhr.getAllResponseHeaders() || '')
        };
        options.url = 'responseURL' in xhr ? xhr.responseURL : options.headers.get('X-Request-URL');
        var body = 'response' in xhr ? xhr.response : xhr.responseText;
        resolve(new Response(body, options));
      };

      xhr.onerror = function() {
        reject(new TypeError('Network request failed'));
      };

      xhr.ontimeout = function() {
        reject(new TypeError('Network request failed'));
      };

      xhr.open(request.method, request.url, true);

      if (request.credentials === 'include') {
        xhr.withCredentials = true;
      }

      if ('responseType' in xhr && support.blob) {
        xhr.responseType = 'blob';
      }

      request.headers.forEach(function(value, name) {
        xhr.setRequestHeader(name, value);
      });

      xhr.send(typeof request._bodyInit === 'undefined' ? null : request._bodyInit);
    })
  };
  self.fetch.polyfill = true;
})(typeof self !== 'undefined' ? self : this);


/***/ }),

/***/ "./node_modules/graphql-request/dist/src/index.js":
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) if (e.indexOf(p[i]) < 0)
            t[p[i]] = s[p[i]];
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var types_1 = __webpack_require__("./node_modules/graphql-request/dist/src/types.js");
var types_2 = __webpack_require__("./node_modules/graphql-request/dist/src/types.js");
exports.ClientError = types_2.ClientError;
__webpack_require__("./node_modules/cross-fetch/dist/browser-polyfill.js");
var GraphQLClient = /** @class */ (function () {
    function GraphQLClient(url, options) {
        this.url = url;
        this.options = options || {};
    }
    GraphQLClient.prototype.rawRequest = function (query, variables) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, headers, others, body, response, result, errorResult;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.options, headers = _a.headers, others = __rest(_a, ["headers"]);
                        body = JSON.stringify({
                            query: query,
                            variables: variables ? variables : undefined,
                        });
                        return [4 /*yield*/, fetch(this.url, __assign({ method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, headers), body: body }, others))];
                    case 1:
                        response = _b.sent();
                        return [4 /*yield*/, getResult(response)];
                    case 2:
                        result = _b.sent();
                        if (response.ok && !result.errors && result.data) {
                            return [2 /*return*/, result];
                        }
                        else {
                            errorResult = typeof result === 'string' ? { error: result } : result;
                            throw new types_1.ClientError(__assign({}, errorResult, { status: response.status }), { query: query, variables: variables });
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    GraphQLClient.prototype.request = function (query, variables) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, headers, others, body, response, result, errorResult;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.options, headers = _a.headers, others = __rest(_a, ["headers"]);
                        body = JSON.stringify({
                            query: query,
                            variables: variables ? variables : undefined,
                        });
                        return [4 /*yield*/, fetch(this.url, __assign({ method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, headers), body: body }, others))];
                    case 1:
                        response = _b.sent();
                        return [4 /*yield*/, getResult(response)];
                    case 2:
                        result = _b.sent();
                        if (response.ok && !result.errors && result.data) {
                            return [2 /*return*/, result.data];
                        }
                        else {
                            errorResult = typeof result === 'string' ? { error: result } : result;
                            throw new types_1.ClientError(__assign({}, errorResult, { status: response.status }), { query: query, variables: variables });
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    GraphQLClient.prototype.setHeaders = function (headers) {
        this.options.headers = headers;
        return this;
    };
    GraphQLClient.prototype.setHeader = function (key, value) {
        var headers = this.options.headers;
        if (headers) {
            headers[key] = value;
        }
        else {
            this.options.headers = (_a = {}, _a[key] = value, _a);
        }
        return this;
        var _a;
    };
    return GraphQLClient;
}());
exports.GraphQLClient = GraphQLClient;
function rawRequest(url, query, variables) {
    return __awaiter(this, void 0, void 0, function () {
        var client;
        return __generator(this, function (_a) {
            client = new GraphQLClient(url);
            return [2 /*return*/, client.rawRequest(query, variables)];
        });
    });
}
exports.rawRequest = rawRequest;
function request(url, query, variables) {
    return __awaiter(this, void 0, void 0, function () {
        var client;
        return __generator(this, function (_a) {
            client = new GraphQLClient(url);
            return [2 /*return*/, client.request(query, variables)];
        });
    });
}
exports.request = request;
exports.default = request;
function getResult(response) {
    return __awaiter(this, void 0, void 0, function () {
        var contentType;
        return __generator(this, function (_a) {
            contentType = response.headers.get('Content-Type');
            if (contentType && contentType.startsWith('application/json')) {
                return [2 /*return*/, response.json()];
            }
            else {
                return [2 /*return*/, response.text()];
            }
            return [2 /*return*/];
        });
    });
}
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./node_modules/graphql-request/dist/src/types.js":
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var ClientError = /** @class */ (function (_super) {
    __extends(ClientError, _super);
    function ClientError(response, request) {
        var _this = this;
        var message = ClientError.extractMessage(response) + ": " + JSON.stringify({ response: response, request: request });
        _this = _super.call(this, message) || this;
        _this.response = response;
        _this.request = request;
        // this is needed as Safari doesn't support .captureStackTrace
        /* tslint:disable-next-line */
        if (typeof Error.captureStackTrace === 'function') {
            Error.captureStackTrace(_this, ClientError);
        }
        return _this;
    }
    ClientError.extractMessage = function (response) {
        try {
            return response.errors[0].message;
        }
        catch (e) {
            return "GraphQL Error (Code: " + response.status + ")";
        }
    };
    return ClientError;
}(Error));
exports.ClientError = ClientError;
//# sourceMappingURL=types.js.map

/***/ }),

/***/ "./node_modules/next/config.js":
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("./node_modules/next/dist/lib/runtime-config.js")


/***/ }),

/***/ "./node_modules/next/head.js":
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("./node_modules/next/dist/lib/head.js")


/***/ }),

/***/ "./node_modules/webpack/buildin/harmony-module.js":
/***/ (function(module, exports) {

module.exports = function(originalModule) {
	if(!originalModule.webpackPolyfill) {
		var module = Object.create(originalModule);
		// module.parent = undefined by default
		if(!module.children) module.children = [];
		Object.defineProperty(module, "loaded", {
			enumerable: true,
			get: function() {
				return module.l;
			}
		});
		Object.defineProperty(module, "id", {
			enumerable: true,
			get: function() {
				return module.i;
			}
		});
		Object.defineProperty(module, "exports", {
			enumerable: true,
		});
		module.webpackPolyfill = 1;
	}
	return module;
};


/***/ }),

/***/ "./pages/index.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* WEBPACK VAR INJECTION */(function(module) {/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("./node_modules/react/cjs/react.development.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__components_DefaultLayout__ = __webpack_require__("./components/DefaultLayout.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__components_SectionCommentCaMarche__ = __webpack_require__("./components/SectionCommentCaMarche.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__components_SectionChronophage__ = __webpack_require__("./components/SectionChronophage.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__components_SectionBenefices__ = __webpack_require__("./components/SectionBenefices.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__components_SectionTypesAides__ = __webpack_require__("./components/SectionTypesAides.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__components_SendInBlueInscrivezVous__ = __webpack_require__("./components/SendInBlueInscrivezVous.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__components_SendInBlueContactForm__ = __webpack_require__("./components/SendInBlueContactForm.js");
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/pages/index.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

(function () {
  var enterModule = __webpack_require__("./node_modules/react-hot-loader/index.js").enterModule;

  enterModule && enterModule(module);
})();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }










var HomePage = function (_React$Component) {
  _inherits(HomePage, _React$Component);

  function HomePage() {
    _classCallCheck(this, HomePage);

    return _possibleConstructorReturn(this, (HomePage.__proto__ || Object.getPrototypeOf(HomePage)).apply(this, arguments));
  }

  _createClass(HomePage, [{
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        __WEBPACK_IMPORTED_MODULE_1__components_DefaultLayout__["a" /* default */],
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 13
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_2__components_SectionCommentCaMarche__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 14
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_3__components_SectionChronophage__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 15
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_4__components_SectionBenefices__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 16
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("hr", {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 17
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_5__components_SectionTypesAides__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 18
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_6__components_SendInBlueInscrivezVous__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 19
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "section",
          { id: "contact", className: "section container", __source: {
              fileName: _jsxFileName,
              lineNumber: 20
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_7__components_SendInBlueContactForm__["a" /* default */], {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 21
            }
          })
        )
      );
    }
  }, {
    key: "__reactstandin__regenerateByEval",
    value: function __reactstandin__regenerateByEval(key, code) {
      this[key] = eval(code);
    }
  }]);

  return HomePage;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

var _default = HomePage;


/* harmony default export */ __webpack_exports__["default"] = (_default);
;

(function () {
  var reactHotLoader = __webpack_require__("./node_modules/react-hot-loader/index.js").default;

  var leaveModule = __webpack_require__("./node_modules/react-hot-loader/index.js").leaveModule;

  if (!reactHotLoader) {
    return;
  }

  reactHotLoader.register(HomePage, "HomePage", "/Applications/MAMP/htdocs/aides-territoires/landing-page/pages/index.js");
  reactHotLoader.register(_default, "default", "/Applications/MAMP/htdocs/aides-territoires/landing-page/pages/index.js");
  leaveModule(module);
})();

;
    (function (Component, route) {
      if(!Component) return
      if (false) return
      module.hot.accept()
      Component.__route = route

      if (module.hot.status() === 'idle') return

      var components = next.router.components
      for (var r in components) {
        if (!components.hasOwnProperty(r)) continue

        if (components[r].Component.__route === route) {
          next.router.update(r, Component)
        }
      }
    })(typeof __webpack_exports__ !== 'undefined' ? __webpack_exports__.default : (module.exports.default || module.exports), "/")
  
/* WEBPACK VAR INJECTION */}.call(__webpack_exports__, __webpack_require__("./node_modules/webpack/buildin/harmony-module.js")(module)))

/***/ }),

/***/ 2:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("./pages/index.js");


/***/ })

},[2])
          return { page: comp.default }
        })
      ;
//# sourceMappingURL=index.js.map