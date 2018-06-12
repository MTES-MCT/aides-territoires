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

/***/ "./components/common/ContactForm.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__services_api__ = __webpack_require__("./services/api.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_graphql_request__ = __webpack_require__("graphql-request");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_graphql_request___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_graphql_request__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_next_config__ = __webpack_require__("next/config");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_next_config___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_next_config__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/common/ContactForm.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }






var _getConfig = __WEBPACK_IMPORTED_MODULE_3_next_config___default()(),
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
      return __WEBPACK_IMPORTED_MODULE_1__services_api__["a" /* default */].request(query, variables);
    }
  }, {
    key: "render",
    value: function render() {
      return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
        "section",
        { id: "contact", className: "section container", __source: {
            fileName: _jsxFileName,
            lineNumber: 60
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 61
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
            className: "text container",
            dangerouslySetInnerHTML: {
              __html: this.props.data.texteduformulairedecontact
            },
            __source: {
              fileName: _jsxFileName,
              lineNumber: 62
            }
          }),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("br", {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 68
            }
          }),
          this.state.emailSendingStatus === EMAIL_SENDING_STATUS_ERROR && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 70
              }
            },
            "D\xE9sol\xE9 nous avons rencontr\xE9 une erreur lors de l'envoi de l'email. Vous pouvez nous contacter \xE0 l'addresse suivante :",
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "strong",
              {
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 73
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
                  lineNumber: 74
                }
              },
              "elise.marion@beta.gouv.fr"
            )
          ),
          this.state.emailSendingStatus === EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "section message is-success", __source: {
                fileName: _jsxFileName,
                lineNumber: 78
              }
            },
            "Merci! Votre message a bien \xE9t\xE9 envoy\xE9."
          ),
          this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_ERROR && this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_SENT && __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "form",
            { id: "contact-form", onSubmit: this.handleSubmit, __source: {
                fileName: _jsxFileName,
                lineNumber: 85
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "field", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 86
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "label",
                { className: "label", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 87
                  }
                },
                "Votre email*"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "control", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 88
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
                    lineNumber: 89
                  }
                })
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "field", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 100
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "label",
                { className: "label", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 101
                  }
                },
                "Votre message"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "control", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 102
                  }
                },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("textarea", {
                  onChange: this.onMessageChange,
                  id: "message",
                  className: "textarea",
                  placeholder: "Votre message",
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 103
                  }
                })
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "field is-grouped is-grouped-right", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 112
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "control", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 113
                  }
                },
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("input", {
                  type: "submit",
                  value: "envoyer",
                  className: "button is-link is-large is-primary",
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 114
                  }
                })
              )
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

/***/ "./components/common/DefaultLayout.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__Navigation__ = __webpack_require__("./components/common/Navigation.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head__ = __webpack_require__("next/head");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_head___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_head__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__PageLoader__ = __webpack_require__("./components/common/PageLoader.js");
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/common/DefaultLayout.js";

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
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", { rel: "icon", type: "image/png", href: "/static/images/favico.png", __source: {
              fileName: _jsxFileName,
              lineNumber: 15
            }
          }),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", { rel: "stylesheet", href: "/static/css/bulma.css", __source: {
              fileName: _jsxFileName,
              lineNumber: 16
            }
          }),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", { rel: "stylesheet", href: "/static/css/style.css", __source: {
              fileName: _jsxFileName,
              lineNumber: 17
            }
          })
        ),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_3__PageLoader__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 19
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_1__Navigation__["a" /* default */], {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 20
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

/***/ "./components/common/Logo.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/common/Logo.js";

var Logo = function Logo() {
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", {
    id: "logo-aides-territoires",
    src: "/static/images/logo-aides-territoires.png",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 3
    }
  });
};

/* harmony default export */ __webpack_exports__["a"] = (Logo);

/***/ }),

/***/ "./components/common/LogoFabNum.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/common/LogoFabNum.js";


var LogoFabNum = function LogoFabNum(props) {
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("img", _extends({
    id: "logo-fabrique-numerique",
    style: { paddingLeft: "1rem" }
  }, props, {
    alt: "logo fabrique num\xE9rique",
    src: "../../static/images/logo-fabnum.svg",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 5
    }
  }));
};

/* harmony default export */ __webpack_exports__["a"] = (LogoFabNum);

/***/ }),

/***/ "./components/common/Navigation.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link__ = __webpack_require__("next/link");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__Logo__ = __webpack_require__("./components/common/Logo.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__LogoFabNum__ = __webpack_require__("./components/common/LogoFabNum.js");
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/common/Navigation.js";

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

    _this.handleLinkClick = function () {
      _this.setState({
        mobileMenuIsActive: false
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
            lineNumber: 25
          }
        },
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "div",
          { className: "navbar-brand", __source: {
              fileName: _jsxFileName,
              lineNumber: 30
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            __WEBPACK_IMPORTED_MODULE_1_next_link___default.a,
            { href: "/#aides-territoires", __source: {
                fileName: _jsxFileName,
                lineNumber: 31
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "a",
              { className: "navbar-item", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 32
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_2__Logo__["a" /* default */], {
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 33
                }
              }),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_3__LogoFabNum__["a" /* default */], {
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 34
                }
              })
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
                lineNumber: 38
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 47
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 48
              }
            }),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("span", {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 49
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
              lineNumber: 52
            }
          },
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "navbar-end", __source: {
                fileName: _jsxFileName,
                lineNumber: 60
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              __WEBPACK_IMPORTED_MODULE_1_next_link___default.a,
              { href: "/#aides-territoires", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 61
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "a",
                { className: "navbar-item", onClick: this.handleLinkClick, __source: {
                    fileName: _jsxFileName,
                    lineNumber: 62
                  }
                },
                "Aides-territoires"
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              __WEBPACK_IMPORTED_MODULE_1_next_link___default.a,
              { href: "/#comment-ca-marche", onClick: this.handleLinkClick, __source: {
                  fileName: _jsxFileName,
                  lineNumber: 66
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "a",
                { className: "navbar-item js-scrollTo", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 67
                  }
                },
                "Service"
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              __WEBPACK_IMPORTED_MODULE_1_next_link___default.a,
              { href: "/#inscription", onClick: this.handleLinkClick, __source: {
                  fileName: _jsxFileName,
                  lineNumber: 69
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "a",
                { className: "navbar-item js-scrollTo", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 70
                  }
                },
                "Inscription"
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              __WEBPACK_IMPORTED_MODULE_1_next_link___default.a,
              { href: "/porteurs-aides", onClick: this.handleLinkClick, __source: {
                  fileName: _jsxFileName,
                  lineNumber: 72
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "a",
                { className: "navbar-item js-scrollTo", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 73
                  }
                },
                "Porteurs d'aides"
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              __WEBPACK_IMPORTED_MODULE_1_next_link___default.a,
              { href: "/a-propos", onClick: this.handleLinkClick, __source: {
                  fileName: _jsxFileName,
                  lineNumber: 75
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "a",
                { className: "navbar-item js-scrollTo", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 76
                  }
                },
                "\xC0 propos"
              )
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              __WEBPACK_IMPORTED_MODULE_1_next_link___default.a,
              { href: "/#contact", onClick: this.handleLinkClick, __source: {
                  fileName: _jsxFileName,
                  lineNumber: 78
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "a",
                { className: "navbar-item", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 79
                  }
                },
                "Contact"
              )
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

/***/ "./components/common/PageLoader.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_head__ = __webpack_require__("next/head");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_next_head___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_next_head__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_link__ = __webpack_require__("next/link");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_next_link___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_next_link__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_nprogress__ = __webpack_require__("nprogress");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_nprogress___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3_nprogress__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_next_router__ = __webpack_require__("next/router");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_next_router___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_next_router__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/common/PageLoader.js";






__WEBPACK_IMPORTED_MODULE_4_next_router___default.a.onRouteChangeStart = function (url) {
  console.log("Loading: " + url);
  __WEBPACK_IMPORTED_MODULE_3_nprogress___default.a.start();
};
__WEBPACK_IMPORTED_MODULE_4_next_router___default.a.onRouteChangeComplete = function () {
  return __WEBPACK_IMPORTED_MODULE_3_nprogress___default.a.done();
};
__WEBPACK_IMPORTED_MODULE_4_next_router___default.a.onRouteChangeError = function () {
  return __WEBPACK_IMPORTED_MODULE_3_nprogress___default.a.done();
};

var linkStyle = {
  margin: "0 10px 0 0"
};

/* harmony default export */ __webpack_exports__["a"] = (function () {
  return __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
    "div",
    { style: { marginBottom: 20 }, __source: {
        fileName: _jsxFileName,
        lineNumber: 19
      }
    },
    __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
      __WEBPACK_IMPORTED_MODULE_1_next_head___default.a,
      {
        __source: {
          fileName: _jsxFileName,
          lineNumber: 20
        }
      },
      __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("link", {
        rel: "stylesheet",
        type: "text/css",
        href: "/static/css/ngprogress.css",
        __source: {
          fileName: _jsxFileName,
          lineNumber: 22
        }
      })
    )
  );
});

/***/ }),

/***/ "./components/index/Benefices.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/index/Benefices.js";

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
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
            className: "content",
            dangerouslySetInnerHTML: {
              __html: this.props.data.benefices
            },
            __source: {
              fileName: _jsxFileName,
              lineNumber: 8
            }
          })
        )
      );
    }
  }]);

  return SectionBenefices;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionBenefices);

/***/ }),

/***/ "./components/index/Chronophage.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/index/Chronophage.js";

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
        { id: "chronophage", className: "section has-primary-background", __source: {
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
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
            dangerouslySetInnerHTML: {
              __html: this.props.data.probleme
            },
            __source: {
              fileName: _jsxFileName,
              lineNumber: 8
            }
          })
        )
      );
    }
  }]);

  return SectionChronophage;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SectionChronophage);

/***/ }),

/***/ "./components/index/CommentCaMarche.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/index/CommentCaMarche.js";

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
            this.props.data.commentcamarchetitre
          ),
          __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
            "div",
            { className: "columns", __source: {
                fileName: _jsxFileName,
                lineNumber: 11
              }
            },
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 12
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 13
                  }
                },
                "1"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 14
                  }
                },
                this.props.data.commentcamarchebloc1titre
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
                dangerouslySetInnerHTML: {
                  __html: this.props.data.commentcamarchebloc1
                },
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 17
                }
              })
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
                "2"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 25
                  }
                },
                this.props.data.commentcamarchebloc2titre
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
                dangerouslySetInnerHTML: {
                  __html: this.props.data.commentcamarchebloc2
                },
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 28
                }
              })
            ),
            __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
              "div",
              { className: "column", __source: {
                  fileName: _jsxFileName,
                  lineNumber: 34
                }
              },
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "div",
                { className: "numero", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 35
                  }
                },
                "3"
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                "h3",
                { className: "title is-4", __source: {
                    fileName: _jsxFileName,
                    lineNumber: 36
                  }
                },
                this.props.data.commentcamarchebloc3titre
              ),
              __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
                dangerouslySetInnerHTML: {
                  __html: this.props.data.commentcamarchebloc3
                },
                __source: {
                  fileName: _jsxFileName,
                  lineNumber: 39
                }
              })
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

/***/ "./components/index/FormPorteurProjetQuartierDurable.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/index/FormPorteurProjetQuartierDurable.js";

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
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
          className: "text container",
          dangerouslySetInnerHTML: {
            __html: this.props.data.texteduformulaireaideecoquartiers
          },
          __source: {
            fileName: _jsxFileName,
            lineNumber: 7
          }
        }),
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("iframe", {
          width: "100%",
          height: "850",
          src: "https://my.sendinblue.com/users/subscribe/js_id/35zg8/id/1",
          frameBorder: "0",
          scrolling: "auto",
          allowFullScreen: true,
          style: {
            background: "transparent",
            display: "block",
            marginLeft: "auto",
            marginRight: "auto",
            maxWidth: "100%"
          },
          __source: {
            fileName: _jsxFileName,
            lineNumber: 13
          }
        })
      );
    }
  }]);

  return SendInBlueInscrivezVous;
}(__WEBPACK_IMPORTED_MODULE_0_react___default.a.Component);

/* harmony default export */ __webpack_exports__["a"] = (SendInBlueInscrivezVous);

/***/ }),

/***/ "./components/index/Header.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/index/Header.js";

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
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("h1", {
                  className: "title",
                  dangerouslySetInnerHTML: {
                    __html: this.props.data.headertitre
                  },
                  __source: {
                    fileName: _jsxFileName,
                    lineNumber: 11
                  }
                }),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "h2",
                  { className: "subtitle ", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 17
                    }
                  },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("div", {
                    dangerouslySetInnerHTML: { __html: this.props.data.header },
                    __source: {
                      fileName: _jsxFileName,
                      lineNumber: 18
                    }
                  }),
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement("p", {
                    __source: {
                      fileName: _jsxFileName,
                      lineNumber: 21
                    }
                  })
                ),
                __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                  "div",
                  { className: "button is-large is-primary", __source: {
                      fileName: _jsxFileName,
                      lineNumber: 34
                    }
                  },
                  __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
                    "a",
                    {
                      className: "button-lancez-la-recherche js-scrollTo ",
                      href: "#inscription",
                      __source: {
                        fileName: _jsxFileName,
                        lineNumber: 35
                      }
                    },
                    this.props.data.headercalltoaction
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

/***/ "./components/index/TypesAides.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_react__);
var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/components/index/TypesAides.js";

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

/* unused harmony default export */ var _unused_webpack_default_export = (SectionTypeAides);

/***/ }),

/***/ "./pages/index.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_babel_runtime_regenerator__ = __webpack_require__("babel-runtime/regenerator");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_babel_runtime_regenerator___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_babel_runtime_regenerator__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react__ = __webpack_require__("react");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_react___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_react__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__components_common_DefaultLayout__ = __webpack_require__("./components/common/DefaultLayout.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__components_index_Header__ = __webpack_require__("./components/index/Header.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__components_index_CommentCaMarche__ = __webpack_require__("./components/index/CommentCaMarche.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__components_index_Chronophage__ = __webpack_require__("./components/index/Chronophage.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__components_index_Benefices__ = __webpack_require__("./components/index/Benefices.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__components_index_TypesAides__ = __webpack_require__("./components/index/TypesAides.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__components_index_FormPorteurProjetQuartierDurable__ = __webpack_require__("./components/index/FormPorteurProjetQuartierDurable.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__components_common_ContactForm__ = __webpack_require__("./components/common/ContactForm.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__services_graphcms__ = __webpack_require__("./services/graphcms.js");

var _jsxFileName = "/Applications/MAMP/htdocs/PRODUCTION/aides-territoires/landing-page/pages/index.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _asyncToGenerator(fn) { return function () { var gen = fn.apply(this, arguments); return new Promise(function (resolve, reject) { function step(key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { return Promise.resolve(value).then(function (value) { step("next", value); }, function (err) { step("throw", err); }); } } return step("next"); }); }; }

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
      return __WEBPACK_IMPORTED_MODULE_1_react___default.a.createElement(
        __WEBPACK_IMPORTED_MODULE_2__components_common_DefaultLayout__["a" /* default */],
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 37
          }
        },
        __WEBPACK_IMPORTED_MODULE_1_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_3__components_index_Header__["a" /* default */], { data: this.props.Pagedaccueil, __source: {
            fileName: _jsxFileName,
            lineNumber: 38
          }
        }),
        __WEBPACK_IMPORTED_MODULE_1_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_4__components_index_CommentCaMarche__["a" /* default */], { data: this.props.Pagedaccueil, __source: {
            fileName: _jsxFileName,
            lineNumber: 39
          }
        }),
        __WEBPACK_IMPORTED_MODULE_1_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_5__components_index_Chronophage__["a" /* default */], { data: this.props.Pagedaccueil, __source: {
            fileName: _jsxFileName,
            lineNumber: 40
          }
        }),
        __WEBPACK_IMPORTED_MODULE_1_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_6__components_index_Benefices__["a" /* default */], { data: this.props.Pagedaccueil, __source: {
            fileName: _jsxFileName,
            lineNumber: 41
          }
        }),
        __WEBPACK_IMPORTED_MODULE_1_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_8__components_index_FormPorteurProjetQuartierDurable__["a" /* default */], { data: this.props.Pagedaccueil, __source: {
            fileName: _jsxFileName,
            lineNumber: 43
          }
        }),
        __WEBPACK_IMPORTED_MODULE_1_react___default.a.createElement(__WEBPACK_IMPORTED_MODULE_9__components_common_ContactForm__["a" /* default */], { data: this.props.Pagedaccueil, __source: {
            fileName: _jsxFileName,
            lineNumber: 44
          }
        })
      );
    }
  }], [{
    key: "getInitialProps",
    value: function () {
      var _ref2 = _asyncToGenerator( /*#__PURE__*/__WEBPACK_IMPORTED_MODULE_0_babel_runtime_regenerator___default.a.mark(function _callee(_ref) {
        var req = _ref.req;
        var query;
        return __WEBPACK_IMPORTED_MODULE_0_babel_runtime_regenerator___default.a.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                query = "{\n      Pagedaccueil(id:\"cjfdxk4tpcy3v016424h68se6\") {\n        commentcamarchetitre\n        commentcamarchebloc1\n        commentcamarchebloc2\n        commentcamarchebloc3\n        commentcamarchebloc1titre\n        commentcamarchebloc2titre\n        commentcamarchebloc3titre\n        header\n        headercalltoaction\n        headertitre\n        probleme\n        benefices\n        texteduformulaireaideecoquartiers\n        texteduformulairedecontact\n      }\n    }\n    ";
                return _context.abrupt("return", __WEBPACK_IMPORTED_MODULE_10__services_graphcms__["a" /* default */].requestWithCache("Pagedaccueil", query));

              case 2:
              case "end":
                return _context.stop();
            }
          }
        }, _callee, this);
      }));

      function getInitialProps(_x) {
        return _ref2.apply(this, arguments);
      }

      return getInitialProps;
    }()
  }]);

  return HomePage;
}(__WEBPACK_IMPORTED_MODULE_1_react___default.a.Component);

/* harmony default export */ __webpack_exports__["default"] = (HomePage);

/***/ }),

/***/ "./services/api.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_next_config__ = __webpack_require__("next/config");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_next_config___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_next_config__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request__ = __webpack_require__("graphql-request");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_graphql_request__);



var _getConfig = __WEBPACK_IMPORTED_MODULE_0_next_config___default()(),
    publicRuntimeConfig = _getConfig.publicRuntimeConfig;

var client = new __WEBPACK_IMPORTED_MODULE_1_graphql_request__["GraphQLClient"](publicRuntimeConfig.GRAPHQL_URL);
/* harmony default export */ __webpack_exports__["a"] = (client);

/***/ }),

/***/ "./services/cache.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
var NodeCache = __webpack_require__("node-cache");
var myCache = new NodeCache();
/* harmony default export */ __webpack_exports__["a"] = (myCache);

/***/ }),

/***/ "./services/graphcms.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_next_config__ = __webpack_require__("next/config");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_next_config___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_next_config__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request__ = __webpack_require__("graphql-request");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_graphql_request___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_graphql_request__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__services_cache__ = __webpack_require__("./services/cache.js");




var _getConfig = __WEBPACK_IMPORTED_MODULE_0_next_config___default()(),
    publicRuntimeConfig = _getConfig.publicRuntimeConfig;

var client = new __WEBPACK_IMPORTED_MODULE_1_graphql_request__["GraphQLClient"](publicRuntimeConfig.GRAPHCMS_API_URL);
var cacheTime = 10000;
// helper to cache result for 10 minutes
client.requestWithCache = function (cacheId, query) {
  var variables = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

  if (__WEBPACK_IMPORTED_MODULE_2__services_cache__["a" /* default */].get(cacheId)) {
    return __WEBPACK_IMPORTED_MODULE_2__services_cache__["a" /* default */].get(cacheId);
  }
  return client.request(query, variables).then(function (data) {
    __WEBPACK_IMPORTED_MODULE_2__services_cache__["a" /* default */].set(cacheId, data, cacheTime);
    return data;
  });
};
/* harmony default export */ __webpack_exports__["a"] = (client);

/***/ }),

/***/ 2:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("./pages/index.js");


/***/ }),

/***/ "babel-runtime/regenerator":
/***/ (function(module, exports) {

module.exports = require("babel-runtime/regenerator");

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

/***/ "next/link":
/***/ (function(module, exports) {

module.exports = require("next/link");

/***/ }),

/***/ "next/router":
/***/ (function(module, exports) {

module.exports = require("next/router");

/***/ }),

/***/ "node-cache":
/***/ (function(module, exports) {

module.exports = require("node-cache");

/***/ }),

/***/ "nprogress":
/***/ (function(module, exports) {

module.exports = require("nprogress");

/***/ }),

/***/ "react":
/***/ (function(module, exports) {

module.exports = require("react");

/***/ })

/******/ });
//# sourceMappingURL=index.js.map