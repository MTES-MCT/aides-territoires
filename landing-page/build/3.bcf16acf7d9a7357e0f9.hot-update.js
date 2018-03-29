webpackHotUpdate(3,{

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
        __WEBPACK_IMPORTED_MODULE_0_react___default.a.createElement(
          "p",
          { className: "text", __source: {
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

/***/ })

})
//# sourceMappingURL=3.bcf16acf7d9a7357e0f9.hot-update.js.map