module.exports =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		var threw = true;
/******/ 		try {
/******/ 			modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 			threw = false;
/******/ 		} finally {
/******/ 			if(threw) delete installedModules[moduleId];
/******/ 		}
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 2);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./components/DefaultLayout.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__Navigation__ = __webpack_require__("./components/Navigation.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head__ = __webpack_require__("next/head");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_head__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__Header__ = __webpack_require__("./components/Header.js");
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/DefaultLayout.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
  }]);

  return DefaultLayout;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (DefaultLayout);

/***/ }),

/***/ "./components/Header.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Header.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
  }]);

  return Header;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (Header);

/***/ }),

/***/ "./components/Navigation.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/Navigation.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }



var Navigation = function (_React$Component) {
  _inherits(Navigation, _React$Component);

  function Navigation(props) {
    _classCallCheck(this, Navigation);

    var _this = _possibleConstructorReturn(this, (Navigation.__proto__ || Object.getPrototypeOf(Navigation)).call(this, props));

    _this.handleClick = function () {
      _this.setState({
        mobileMenuIsActive: !_this.state.mobileMenuIsActive
      });
    };

    _this.state = {
      mobileMenuIsActive: false
    };
    return _this;
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
            lineNumber: 17
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "navbar-brand", __source: {
              fileName: _jsxFileName,
              lineNumber: 22
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "a",
            { className: "navbar-item js-scrollTo", href: "#aides-territoires", __source: {
                fileName: _jsxFileName,
                lineNumber: 23
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", { src: "/static/images/logo.png ", __source: {
                fileName: _jsxFileName,
                lineNumber: 24
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "p",
              { className: "app-name ", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 25
                }
              },
              "Aides-territoires"
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            {
              className: this.state.mobileMenuIsActive ? "navbar-burger is-active" : "navbar-burger",
              "data-target": "navMenu",
              onClick: this.handleClick,
              __source: {
                fileName: _jsxFileName,
                lineNumber: 27
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 36
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 37
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 38
              }
            })
          )
        ),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          {
            className: this.state.mobileMenuIsActive ? "navbar-menu is-active" : "navbar-menu",
            id: "navMenu ",
            __source: {
              fileName: _jsxFileName,
              lineNumber: 41
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "navbar-end", __source: {
                fileName: _jsxFileName,
                lineNumber: 49
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#aides-territoires", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 50
                }
              },
              "Aides-territoires"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#comment-ca-marche", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 53
                }
              },
              "Le service"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#inscription", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 56
                }
              },
              "Inscription"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item js-scrollTo", href: "/#contact", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 59
                }
              },
              "Contact"
            )
          )
        )
      );
    }
  }]);

  return Navigation;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (Navigation);

/***/ }),

/***/ "./components/SectionBenefices.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionBenefices.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
  }]);

  return SectionBenefices;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionBenefices);

/***/ }),

/***/ "./components/SectionChronophage.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionChronophage.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
  }]);

  return SectionChronophage;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionChronophage);

/***/ }),

/***/ "./components/SectionCommentCaMarche.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionCommentCaMarche.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
  }]);

  return SectionCommentCaMarche;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionCommentCaMarche);

/***/ }),

/***/ "./components/SectionTypesAides.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SectionTypesAides.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
  }]);

  return SectionTypeAides;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionTypeAides);

/***/ }),

/***/ "./components/SendInBlueContactForm.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request__ = __webpack_require__("graphql-request");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_graphql_request__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_config__ = __webpack_require__("next/config");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_config___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_config__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueContactForm.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "p",
          { "class": "text", __source: {
              fileName: _jsxFileName,
              lineNumber: 60
            }
          },
          "Vous avez encore des questions ? des suggestions ? N'h\xE9sitez pas, nous sommes \xE0 votre disposition et serons ravis d'\xE9changer avec vous : laissez-nous un message !",
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 63
            }
          }),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 64
            }
          })
        ),
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_ERROR && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 67
            }
          },
          "D\xE9sol\xE9 nous avons rencontr\xE9 une erreur lors de l'envoi de l'email. Vous pouvez nous contacter \xE0 l'addresse suivante :",
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "strong",
            {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 70
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
                lineNumber: 71
              }
            },
            "elise.marion@beta.gouv.fr"
          )
        ),
        this.state.emailSendingStatus === EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "section message is-success", __source: {
              fileName: _jsxFileName,
              lineNumber: 75
            }
          },
          "Merci! Votre message a bien \xE9t\xE9 envoy\xE9."
        ),
        this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_ERROR && this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "form",
          { id: "contact-form", onSubmit: this.handleSubmit, __source: {
              fileName: _jsxFileName,
              lineNumber: 82
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field", __source: {
                fileName: _jsxFileName,
                lineNumber: 83
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "label",
              { className: "label", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 84
                }
              },
              "Votre email*"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 85
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
                  lineNumber: 86
                }
              })
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field", __source: {
                fileName: _jsxFileName,
                lineNumber: 97
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "label",
              { className: "label", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 98
                }
              },
              "Votre message"
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 99
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("textarea", {
                onChange: this.onMessageChange,
                id: "message",
                className: "textarea",
                placeholder: "Votre message",
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 100
                }
              })
            )
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "field is-grouped is-grouped-right", __source: {
                fileName: _jsxFileName,
                lineNumber: 109
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "control", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 110
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("input", {
                type: "submit",
                value: "envoyer",
                className: "button is-link is-large is-primary",
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 111
                }
              })
            )
          )
        )
      );
    }
  }]);

  return ContactForm;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (ContactForm);

/***/ }),

/***/ "./components/SendInBlueInscrivezVous.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/aides-territoires/landing-page/components/SendInBlueInscrivezVous.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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
  }]);

  return SendInBlueInscrivezVous;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SendInBlueInscrivezVous);

/***/ }),

/***/ "./pages/index.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
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
  }]);

  return HomePage;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["default"] = (HomePage);

/***/ }),

/***/ 2:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("./pages/index.js");


/***/ }),

/***/ "graphql-request":
/***/ (function(module, exports) {

module.exports = require("graphql-request");

/***/ }),

/***/ "next/config":
/***/ (function(module, exports) {

module.exports = require("next/config");

/***/ }),

/***/ "next/head":
/***/ (function(module, exports) {

module.exports = require("next/head");

/***/ }),

/***/ "react":
/***/ (function(module, exports) {

module.exports = require("react");

/***/ })

/******/ });
//# sourceMappingURL=index.js.map